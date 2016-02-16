import sys


def extract_commant(line):
    for word in line:
        if len(word) == 2:
            try:
                d = int(word, base=16)
            except ValueError:
                return word
        else:
            return word


def parse_file(filename, programname):
    d = open("instructions.txt", "r")
    instructions = {}
    for line in d:
        instructions[line[:-1]] = 0
    d.close()

    for line in open("asm.txt", "r"):
        line = line.split()
        if len(line) >= 3:
            if line[0][-1] == ":":
                try:
                    int(line[1], base=16)
                except ValueError:
                    pass
                else:
                    try:
                        word = extract_commant(line[2:])
                        try:
                            instructions[word] += 1
                        except KeyError:
                            pass
                    except TypeError:
                        pass

    s = open("sample/" + programname + "/" + filename, "w")
    for key in sorted(instructions.keys()):
        s.write(key + " " + str(instructions[key]) + '\n')
        # print key , instructions[key]


# parse_file(123123,12312)
