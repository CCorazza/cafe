""" Serge

Parce que j'avais la flemme.

"""

from datetime import datetime, timedelta
import json
import re
import time



GROVE = "G03CCAS2U"


outputs = []

def out(msg):
    outputs.append([GROVE, msg])


def pattern(_pattern):
    def pattern_wrapper(func):
        func.pattern = re.compile(_pattern)
        return func
    return pattern_wrapper


@pattern(r":coffee: ?\?")
def cmd_list(**kwargs):
    """usage: list
    """
    output = []
    for num, brek in enumerate(get_breaks()):
        date = datetime.strptime(brek['time'], "%Y-%m-%d %H:%M:%S.%f")
        output.append("[{num}] {date:%m/%d %H:%M}".format(**locals()))
    if output:
        out("\n".join(output))
    else:
        out("Il n'y a pas de pauses enregistrees :(")


@pattern(r":coffee: ?\[(-?\d+)\]")
def cmd_info(args, **kwargs):
    """usage: info <id>
    """
    if len(args) != 1:
        return out("Mauvais nombre d'arguments :( `{}`".format(args))
    try:
        index = int(args[0])
    except ValueError:
        return out("Valeur incorrecte :( `{}`".format(args[0]))
    breaks = get_breaks()
    try:
        brek = breaks[index]
    except IndexError:
        return out("Valeur n'est pas associable a une pause :( `{}`".format(args[0]))
    date = datetime.strptime(brek['time'], "%Y-%m-%d %H:%M:%S.%f")
    users = ", ".join("<@{user}>".format(user=user) for user in brek['users'])
    out("[{index}], {date:%m/%d %H:%M}, {users}".format(**locals()))


@pattern(r":coffee: ?@(\d+)[:h](\d+)")
def cmd_create(args, user, **kwargs):
    """usage: create <hour> <minutes>
    """
    if len(args) != 2:
        return out("Nombre d'arguments non valide :( `{}`".format(args))
    try:
        hour, minute = int(args[0]), int(args[1])
        assert 0 <= hour < 24 and 0 <= minute < 60
    except (ValueError, AssertionError):
        return out("Heures et minutes sont invalides :( `{}` `{}`".format(*args))
    dt = datetime.now().replace(hour=hour, minute=minute)
    newbrek = { "users": [user], "time": str(dt) }
    breaks = get_breaks() + [newbrek]
    set_breaks(breaks)
    out("oklm, cyu l8r")


@pattern(r":coffee: ?\+(-?\d+)")
def cmd_join(args, user, **kwargs):
    """usage: join <id>
    """
    if len(args) != 1:
        return out("Mauvais nombre d'arguments :( `{}`".format(args))
    try:
        index = int(args[0])
    except ValueError:
        return out("Valeur incorrecte :( `{}`".format(args[0]))
    breaks = get_breaks()
    try:
        brek = breaks[index]
    except IndexError:
        return out("Valeur n'est pas associable a une pause :( `{}`".format(args[0]))
    if user not in breaks[index]['users']:
        breaks[index]['users'].append(user)
    set_breaks(breaks)
    out("C'est tout bon, vous serez notifie en temps voulu :)")


@pattern(r":coffee: ?-(-?\d+)")
def cmd_leave(args, user, **kwargs):
    """usage: leave <id>
    """
    if len(args) != 1:
        return out("Mauvais nombre d'arguments :( `{}`".format(args))
    try:
        index = int(args[0])
    except ValueError:
        return out("Valeur incorrecte :( `{}`".format(args[0]))
    breaks = get_breaks()
    try:
        brek = breaks[index]
    except IndexError:
        return out("Valeur n'est pas associable a une pause :( `{}`".format(args[0]))
    if user in breaks[index]['users']:
        breaks[index]['users'].remove(user)
    if not breaks[index]['users']:
        del breaks[index]
    set_breaks(breaks)
    out("C'est tout bon, vous ne serez pas notifie :)")


@pattern(r":coffee:$")
def cmd_help(args, **kwargs):
    """usage: help [command]
    """
    out("euhh... go lire https://github.com/ldesgoui/cafe")



shortcmds = {
    "list": cmd_list,
    "info": cmd_info,
    "create": cmd_create,
    "join": cmd_join,
    "leave": cmd_leave,
    "help": cmd_help,
}


def process_message(data):
    if 'subtype' in data:
        return
    if data['channel'] != GROVE:
        return
    if data['text'].startswith("serge: coffee"):
        text = data['text'][13:].split()
        if not len(text):
            command, args = "help", []
        else:
            command, args = text[0], text[1:]
        return get_cmd(command)(args=args, **data)
    elif data['text'].startswith("serge: :coffee:"):
        text = data['text'][15:].split()
        command, args = text[0], text[1:]
        return get_cmd(command)(args=args, **data)
    elif ':coffee:' in data['text']:
        for command, func in shortcmds.items():
            for match in func.pattern.finditer(data['text']):
                args = list(match.groups())
                func(args=args, **data)


def get_cmd(command):
    if command not in shortcmds:
        def cmd_invalid(*args, **kwargs):
            out("La commande n'est pas valide :( `{}`".format(command))
        return cmd_invalid
    return shortcmds[command]


def set_breaks(breaks):
    with open('breaks.json', 'w') as f:
        f.write(json.dumps(list(sorted(breaks))))

def get_breaks():
    try:
        return json.loads(open('breaks.json', 'r').read())
    except ValueError:
        return []


def warn_on_time():
    now = datetime.now()
    breaks = get_breaks()
    oneminute = timedelta(minutes=1)
    changed = False
    for n, brek in enumerate(breaks[:]):
        dt = datetime.strptime(brek['time'], "%Y-%m-%d %H:%M:%S.%f")
        if now < dt < now + oneminute:
            out("PAUSE! :coffee: %s" % ", ".join("<@{user}>".format(user=user) for user in brek['users']))
        if dt < now:
            del breaks[breaks.index(brek)]
            changed = True
        if now + oneminute < dt:
            break
    if changed:
        set_breaks(breaks)

crontable = [[60, 'warn_on_time']]
