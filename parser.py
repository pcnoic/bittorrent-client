import re
import sys

def tokenize(text, match=re.compile("([idel])|(\d+):|(-?\d+)").match):
    i = 0
    while i < len(text):
        m = match(text, i)
        s = m.group(m.lastindex)
        i = m.end()
        if m.lastindex == 2:
            yield "s"
            yield text[i:i+int(s)]
            i = i + int(s)
        else:
            yield s

#decoding the bencoded object
def decode_item(next, token):
    if token == "i":
        #value is integer
        data = int(next())
        if next() != "e":
            raise ValueError
    elif token == "s":
        #value is string
        data = next() #no need to parse them with converting function
    elif token == "l" or token == "d":
        data = [] #either a dict or a list so needs to be stored that way
        tok = next()
        while tok != "e":
            data.append(decode_item(next, tok))
            tok = next()
        if token == "d":
            data = dict(zip(data[0::2], data[1::2]))
    else:
        raise ValueError
    return data

def decode(text):
    try:
        src = tokenize(text)
        data = decode_item(src.next, src.next())
        for token in src: #looking for more tokens
            raise SyntaxError('junk on the end of string')
    except (AttributeError, ValueError, StopIteration):
        raise SyntaxError("syntax error")
    return data


def translate(tFile):
    data = open(tFile, "rb").read()

    torrent = decode(data)

    for file in torrent["info"]["files"]:
        return "%r - %d bytes" % ("/".join(file["path"]), file["length"])
