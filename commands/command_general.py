import time
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import utils

from commands.command import Command
from utilities.string import (jleft, jright)
from utilities.display import header, divider, color_chart

class CmdLook(Command):
    """
    If entered with no arguments, shows you the current room, vehicle, or container you happen to be in. If used with an argument, will attempt to look at certain specific things.

    |xUsage:|n
      |Rlook|n
      |Rlook <player>|n
      |Rlook <player> <clothing/held item>|n
    """
    key = "look"
    aliases = ["l"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """
        Handle the looking.
        """
        ply = self.caller
        ply_room = self.caller.location

        self.args = self.args.strip()

        # If no target specified, default to looking at the room.
        if not self.args:
            target = ply_room
            # If all else fails and we're somehow neither in a room, nor chargen.
            if not target:
                ply.error_echo("You can see nothing.")
                return

        else:
            if self.args.strip() == "me" or self.args.strip() == "self":
                target = ply
            else:
                target = ply.search(self.args, quiet = True)
            if not target:
                return

        ply.msg((ply.at_look(target = target), {'type': 'look'}), options = None)

class CmdSay(Command):
    """
    Say something aloud for other players to hear.

    |xUsage:|n
      |Rsay <message>|n
      |R'<message>|n
      |R"<message>|n

    You can be heard by almost anyone in the room, as well as people who happen to be nearby and listening in.
    """

    key = "say"
    aliases = ['"', "'"]
    locks = "cmd:all()"

    def func(self):
        ply = self.caller
        speech = self.words(1)

        if not speech:
            ply.error_echo("You must specify something to say!")
            return

        # Call any code that might fire before speaking - e.g. voice disguising, etc.
        speech, proceed = ply.at_before_say(speech)

        if proceed != True:
            # Something is preventing the player from speaking; wrap it up here.
            return

        # Process player speech.
        ply.at_say(speech, msg_self = True)

        # Post-processing for things such as hypnotic suggestion, coded phrases, and more.
        ply.at_after_say(speech)

class CmdSit(Command):
    """
    Cause your character to sit down. Can optionally specify a bit of furniture to sit on.

    |xUsage:|n
      |Rsit|n
      |Rsit <furniture>|n

    Naturally, you cannot move while seated.
    """
    key = "sit"
    locks = "cmd:all()"

    def func(self):
        ply = self.caller

        if ply.db.prone >= 2:
            ply.db.prone = 1
            ply.echo("You shift up into a seated position.")
        elif ply.db.prone == 0:
            ply.db.prone = 1
            ply.echo("You sit down.")
        else:
            ply.echo("You are already seated.")

class CmdStand(Command):
    """
    If seated or lying down, stand up.

    |xUsage:|n
      |Rstand|n
    """
    key = "stand"
    locks = "cmd:all()"

    def func(self):
        ply = self.caller

        if ply.db.prone == 0:
            ply.echo("You are already standing.")
            return

        ply.db.prone = 0
        ply.echo("You stand up.")

class CmdLie(Command):
    """
    Lie down on the ground. Alternatively, you may specify a piece of furniture to lie on.

    |xUsage:|n
      |Rlie|n
      |Rlie <furniture>|n

    Naturally, you cannot move while lying down. Note that in most cases, you will be considered vulnerable while prone!
    """
    key = "lie"
    aliases = ["lay"]
    locks = "cmd:all()"

    def func(self):
        ply, prone = self.caller, self.caller.db.prone

        if prone >= 2:
            ply.echo("You are already lying down.")
            return

        if prone == 1:
            ply.db.prone = 2
            ply.echo("You ease down onto the ground.")
        elif prone == 0:
            ply.db.prone = 2
            ply.echo("You lie down.")

class CmdWho(Command):
    """
    See who's currently online.

    |xUsage:|n
      |Rwho|n

    Note that you may not be able to see certain people who have taken efforts to conceal themselves.
    """

    key = "who"
    locks = "cmd:all()"

    def func(self):
        """
        Get all connected accounts by polling session.
        """

        account = self.account
        session_list = SESSIONS.get_sessions()
        session_list = sorted(session_list, key = lambda o: o.account.key)

        self.msg(header("Currently Online", color = "m"))
        self.msg("  |xNAME|n                         |xONLINE FOR|n   |xIDLE FOR|n")

        for session in session_list:
            if not session.logged_in:
                continue

            puppet = session.get_puppet()
            if not puppet:
                continue

            naccounts = SESSIONS.account_count()

            location = puppet.location.key if puppet and puppet.location else ""
            p_name = puppet.get_display_name(account)
            
            idle = utils.time_format(time.time() - session.cmd_last_visible, 1)
            conn = utils.time_format(time.time() - session.conn_time, 0)

            self.msg("  %s%s    %s" % (jleft(p_name, 32), jright(conn, 7), jright(idle, 7)))
            self.msg("  |c%s|n" % (location))

        self.msg("\n\n  |W%s|n |xunique account%s logged in.|n" % (naccounts, "" if naccounts == 1 else "s"))

        self.msg(divider(color = "m"))

class CmdColors(Command):
    key = "color"
    aliases = ["colors"]

    def func(self):
        ply = self.caller

        ply.echo(color_chart())

class CmdDrop(Command):
    key = "drop"

    def func(self):
        ply = self.caller
        tar = self.words(1)

        obj = ply.search(tar, global_search = False, quiet = True)[0]

        if not obj:
            ply.error_echo(f"You don't seem to have \"{tar}.\"")
            return

        if obj.location != ply:
            ply.error_echo("You aren't carrying that on your person.")
            return

        obj.location = ply.location
        ply.message(self_m = f"You drop {obj.name}.", witness_m = f"PLAYER !drop {obj.name}.", prompt = False)