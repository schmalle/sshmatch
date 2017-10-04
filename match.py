import hashlib
from enum import Enum

checksums = {'DEADBEEF': 0}
counter, duplicates, uniques = 0,0,0;

class Token(Enum):
    COMMAND = 1
    NONE = 2
    STRING = 3
    NOT_FOUND = 4
    URL = 5




#
# tokens for the parser
#
tokens = {"printf" : Token.STRING, "sh" : Token.COMMAND, "/bin/echo" : Token.STRING, "wget" : Token.URL, "tftp" : Token.URL, "/usr/bin/printf" : Token.STRING, 'shell' : Token.COMMAND, 'system' : Token.COMMAND, '/bin/busybox': Token.COMMAND, "enable" : Token.NONE, "cat": Token.STRING, "cd" : Token.STRING, "echo" : Token.STRING, "cat" : Token.STRING}


def getCommand(block):


    return ""

def normalizedchecksumHash(line, uniques, verbose):

    context = "NONE"
    counter = 0

    line = line.lower()
    blocks = line.split()

    for block in blocks:

        context = tokens.get(block, Token.NOT_FOUND)

        if (block[-1] == ";"):

            if verbose:
                print("Info:: Found ending ; sign, removing temporarily....")

            context = tokens.get(block[0: -1], Token.NOT_FOUND)

            if (context != Token.NOT_FOUND):
                context = Token.NONE


        #
        # kill all strings
        #
        if (context == Token.STRING):
            blocks[counter] = "aaaa"

            if (block.startswith("-")):
                pass
            else:
                context = Token.NONE


        if (context == Token.NOT_FOUND):
            print("Error:: No command found for block " + block + " sanitizing input")
            blocks[counter] = "aaaa"
        elif verbose:
            print("AllOk:: Found command for block: " + block)

        counter = counter + 1;

#
# checksum a given live without any modifications / normalization
#
def checksumHash(line, uniques):
    m = hashlib.sha256()
    m.update(line.lower())

    hash = m.hexdigest()

    counterForHash = checksums.get(hash, 0)
    if (counterForHash == 0):
        uniques += 1
        checksums[hash] = 1
    else:
        checksums[hash] = counterForHash + 1

    print(hash + ", " + str(len(line)))
    return uniques


#
# show statistics of found checksums
#
def statistics():
    pass

line = "enable; system; shell; sh;  /bin/busybox wget; /bin/busybox 81c46036wget; /bin/busybox echo -ne '\\x0181c46036\\x7f'; /bin/busybox printf '\\00281c46036\\177'; /bin/echo -ne '\\x0381c46036\\x7f'; /usr/bin/printf '\\00481c46036\\177'; /bin/busybox tftp; /bin/busybox 81c46036tftp;;  /bin/busybox dd if=/bin/busybox bs=22 count=1 || /bin/busybox cat /bin/busybox"
normalizedchecksumHash(line, 0, False)

    #with open("./samples/all.txt") as fin:
#    for line in fin:
#        line = "enable; system; shell; sh;  /bin/busybox wget; /bin/busybox 81c46036wget; /bin/busybox echo -ne '\\x0181c46036\\x7f'; /bin/busybox printf '\\00281c46036\\177'; /bin/echo -ne '\\x0381c46036\\x7f'; /usr/bin/printf '\\00481c46036\\177'; /bin/busybox tftp; /bin/busybox 81c46036tftp;;  /bin/busybox dd if=/bin/busybox bs=22 count=1 || /bin/busybox cat /bin/busybox"
#        uniques = checksumHash(line.encode("utf-8"), uniques)
#        counter +=1
#        normalizedchecksumHash(line, uniques)

#print ("Analysed lines: " + str(counter))
#print ("Unique lines without normalization: " + str(uniques))