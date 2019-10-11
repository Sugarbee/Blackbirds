# IRE-like administration commands, aka my effort to get out of MUXland.

from evennia.server.sessionhandler import SESSIONS
from evennia.utils import search

from commands.command import Command
from utilities.utils_display import Notify
from utilities.menu import Menu
from typeclasses.zones import Zone

class CmdReload(Command):
    """
    reload the server

    Usage:
      reload [reason]

    This restarts the server. The Portal is not
    affected. Non-persistent scripts will survive a reload (use
    reset to purge) and at_reload() hooks will be called.
    """
    key = "reload"
    aliases = ['restart']
    locks = "cmd:perm(reload) or perm(Developer)"
    help_category = "System"

    def func(self):
        "Reload the system."
        reason = ""
        if self.args:
            reason = "%s" % self.args.rstrip(".")
        SESSIONS.announce_all(Notify("Game", f"The system is reloading{reason}, please be patient."))
        SESSIONS.portal_restart_server()

class CmdMakeAdmin(Command):
    """
    Gives the targetted account admin privileges.

    |xUsage:|n
      |Rmakeadmin <account>|n
    """
    key = "makeadmin"
    locks = "perm(<Superuser>)"
    def func(self):
        ply = self.caller
        # tar = search.account_search(self.word(1))
        if not self.args:
            ply.echo("You must specify the name of an account.")
            return

        tar = search.account_search(self.word(1))[0]
        if not tar:
            ply.echo("No account by that name could be found.")
            return

        ply.echo(f"Ding! Your target account is: {tar}")
        # tar.cmdset.add(default_cmds.AdminCmdSet, permanent = True)


class CmdTest(Command):
    key = "test"
    locks = "perm(Admin)"

    def func(self):
        # Menu(self.caller, "menus.testmenu", cmdset_mergetype = "Replace", cmd_on_exit = "look", startnode = "node_test", debug = True)
        z = Zone()
        z_rooms = z.rooms(0)
        self.echo(z_rooms)