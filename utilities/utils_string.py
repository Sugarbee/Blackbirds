import evennia

def AutoCap(s):
    return "%s%s" % (s[0].upper(), s[1:])

def AutoPunc(s):
    punc = s[-1]
    if not punc in [".", ",", "'", '"', "(", ")", "!", "?", "-"]:
        s += "."

    return s

def RPFormat(s):
    """
    Rudimentary formatting of speech and emoting.

    Capitalizes the first letter of the string, and intelligently auto-punctuates the end.
    """

    s = AutoCap(s)
    s = AutoPunc(s)

    return s