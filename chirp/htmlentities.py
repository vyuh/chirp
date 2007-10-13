import htmlentitydefs
import re

def substitute(match):
    ent = match.group(2)
    if match.group(1) == "#":
        return unichr(int(ent))
    else:
        cp = htmlentitydefs.name2codepoint.get(ent)

        if cp:
            return unichr(cp)
        else:
            return match.group()

def decode(string):
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")
    return entity_re.subn(substitute, string)[0]

