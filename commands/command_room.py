"""
All commands related to getting or altering information about rooms.
"""

# Blackbirds modules.
from commands.command import Command
from typeclasses.environments import Environment
from typeclasses.zones import Zone
from typeclasses.exits import Exit
from utilities.utils_display import Line
from utilities.utils_string import jleft, jright
import utilities.utils_directions as dirs

def DescribeRoom(ply, room, description):
    room.db.desc = description
    ply.echo(f"|xRoom description changed. The room will now be described as:|n\n{room.db.desc}")

def roominfo_entry(attr_name, nice_value, var_name, type_reminder, cust_str_color = "W"):
    translated_value = "|c---|n"

    if type(nice_value) is bool:
        if nice_value == True:
            translated_value = "|YYes|n"
        elif nice_value == False:
            translated_value = "|rNo|n"
    elif type(nice_value) is int:
        if nice_value >= 0:
            translated_value = "|W" + str(nice_value) +"|n"
        elif nice_value == 0:
            translated_value = "|x0|n"
    elif type(nice_value) is str:
        translated_value = f"|{cust_str_color}{nice_value}|n"

    string = "\n%s" % (jright(attr_name, 16))
    string += " |c|||n "
    string += "%s" % (jleft(translated_value, 24))
    string += "|x%s|n" % var_name
    string += " |x[%s]|n" % type_reminder
    return string

def RoomInfo(ply, tar_room = None):
    # add logic to search for and get info on tar_room instead here
    r_name = tar_room.name
    r_id = tar_room.id
    r_id_str = "#" + str(tar_room.id)

    zone = Zone()
    r_zone = zone.name(tar_room.db.zone)

    env = Environment()
    env_name = env.name(tar_room.db.environment)
    env_color = env.color(tar_room.db.environment)

    string = Line(80, "|y", f"{r_id_str}, {r_name}", "|W")

    string += roominfo_entry("Name", r_name, "name", "str")
    string += roominfo_entry("Zone", r_zone, "zone", "id")
    string += roominfo_entry("Environment", env_name, "environment", "id", env_color)
    string += roominfo_entry("Temperature", tar_room.db.temperature, "temperature", "num")
    string += roominfo_entry("Indoors", tar_room.db.indoors, "indoors", "bool")
    string += roominfo_entry("Illumination", tar_room.db.illumination, "illumination", "0-15")
    string += roominfo_entry("Water Level", tar_room.db.water_level, "water_level", "0-15")

    string += "\n"

    string += roominfo_entry("Darkness", tar_room.db.darkness, "darkness", "bool")
    string += roominfo_entry("Natural", tar_room.db.natural, "natural", "bool")
    string += roominfo_entry("Public", tar_room.db.public, "public", "bool")
    string += roominfo_entry("Shop", tar_room.db.shop, "shop", "bool")
    string += roominfo_entry("House", tar_room.db.house, "house", "bool")
    string += roominfo_entry("Battleground", tar_room.db.battleground, "battleground", "bool")
    string += roominfo_entry("Craft Hall", tar_room.db.craft_hall, "craft_hall", "bool")
    string += roominfo_entry("Chapel", tar_room.db.chapel, "chapel", "bool")
    string += roominfo_entry("Bank", tar_room.db.bank, "bank", "bool")

    string += "\n"

    string += roominfo_entry("Powered", tar_room.db.powered, "powered", "bool")
    string += roominfo_entry("Power Sink", tar_room.db.power_sink, "power_sink", "bool")
    string += roominfo_entry("Radio Tower", tar_room.db.radio_tower, "radio_tower", "bool")
    string += roominfo_entry("Neon Well", tar_room.db.neon_well, "neon_well", "bool")

    string += "\n"

    string += roominfo_entry("Player Owned", tar_room.db.player_owned, "player_owned", "bool")
    string += roominfo_entry("Owning Player", tar_room.db.player_owner_id, "player_owner_id", "bool")

    string += "\n" + Line(80, "|y")

    ply.echo(string)

def RoomRename(ply, tar_room = None, new_name = None):
    if not new_name or new_name == "":
        ply.echo("You must specify a name for the room.")
        return

    r_id = tar_room.id
    r_id_str = "#" + str(tar_room.id)
    previous_name = tar_room.name
    tar_room.name = new_name
    ply.echo(f"Room {r_id_str}'s name has been changed from {previous_name} to {tar_room.name}.")

def RoomRedescribe(ply, tar_room = None, new_desc = None):
    pass

def RoomTemperature(ply, tar_room = None, new_temp = None):
    pass

def RoomEnvironment(ply, tar_room = None, new_env = None):
    if not new_env:
        ply.echo("You must specify an environment by number. See |Renvironment list|n for all current environments.")
        return

    try:
        eid = int(new_env)
    except ValueError:
        ply.echo("You must enter a number.")
        return

    env = Environment()
    env_name = env.name(eid)
    env_color = env.color(eid)

    r_id = tar_room.id
    r_name = tar_room.name
    tar_room.db.environment = eid
    ply.echo(f"You set room #{r_id}, {r_name}, to use the |{env_color}{env_name}|n environment.")

def RoomCreateExit(ply, tar_room = None, dir = None, dest = None):
    if not dir:
        ply.echo("|xYou must specify a direction.|n")
        return

    if not dirs.valid_direction(dir):
        ply.echo("|xYou must supply a valid direction.|n")
        return

    destination = ply.search(dest, global_search = True)
    if not destination:
        ply.echo("|xThat does not appear to be a valid room.|n")
        return

    full_dir = dirs.valid_direction(dir)
    e, err_msg = tar_room.create_exit(full_dir, destination)
    if not e:
        ply.echo(err_msg)
        return

    ply.echo(f"You create a {full_dir}ward exit to room {dest}, {destination.name}.")

def RoomDeleteExit(ply, tar_room = None, dir = None):
    if not dir:
        ply.echo("|xYou must specify a direction.|n")
        return

    if not dirs.valid_direction(dir):
        ply.echo("|xYou must supply a valid direction.|n")
        return

    full_dir = dirs.valid_direction(dir)
    e, err_msg = tar_room.delete_exit(full_dir)
    if not e:
        ply.echo(err_msg)
        return

    ply.echo(f"You delete the {full_dir}ward exit.")

class CmdRoom(Command):
    """
    The following commands are used to build, edit, or otherwise manipulate rooms. In general, you may type any given subcommand by itself to see help and syntax information for each one.

    |xUsage:|n
      |Rroom info|n
    """
    key = "room"
    locks = "perm(Builder)"
    help_category = "Admin"

    def __init__(self):
        super().__init__()

        self.set_syntax_notes("The |Rroom|w command is a fully-featured suite of commands to make, delete, or otherwise manipulate rooms to your liking. As such, the command by itself does nothing. Refer to each subcommand below for further information.")

        self.set_syntax("info", "Displays a useful breakdown of the current room and its attributes.")
        self.set_syntax("name <room> <name>", "Change the room's name.")
        self.set_syntax("desc <room> <description>", "Change the room's description.")
        self.set_syntax("temp <room> <temperature>", "Change the room's temperature.")
        self.set_syntax("env <room> <environment>", "Change the room's environmental type.")
        self.set_syntax("link <dir> <destination>", "Add a new exit to the desired room.")
        self.set_syntax("unlink <dir>", "Remove an exit from the room.")

        self.set_syntax_notes("At this time, you must specify 'here' to alter the current room.", True)

    def func(self):
        ply = self.caller
        sub = self.word(1)
        tar_room = self.word(2)
        args = self.words(3, self.word_count())

        # Display syntax if used by itself - or if the subcommand isn't found.
        if not sub:
            self.get_syntax()
            return

        # All commands default to current room if none is specified.
        if not tar_room or tar_room == "here":
            tar_room = ply.location

        # Determine valid subcommand by argument.
        if sub == "info":
            RoomInfo(ply, tar_room)
        elif sub == "name" or sub == "rename":
            RoomRename(ply, tar_room, args)
        elif sub == "desc" or sub == "description":
            RoomRedescribe(ply, tar_room, args)
        elif sub == "temp" or sub == "temperature":
            RoomTemperature(ply, tar_room, args)
        elif sub == "env" or sub == "environment":
            RoomEnvironment(ply, tar_room, args)
        elif sub == "link":
            RoomCreateExit(ply, tar_room, self.word(3), self.word(4))
        elif sub == "unlink":
            RoomDeleteExit(ply, tar_room, args)
        else:
            self.get_syntax()