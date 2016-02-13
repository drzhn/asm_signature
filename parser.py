import sys


def extract_commant(line):
    for word in line:
        if len(word) == 2:
            try:
                d = int(word, base=16)
                # print word,
            except ValueError:
                # print word
                return word
        else:
            # print word
            return word


def parse_file(filename, programname):
    f = open("asm.txt", "r")
    d = open("sample/" + programname + "/" + filename, "w")
    for line in f:
        line = line.split()
        # print line

        if len(line) >= 3:
            if line[0][-1] == ":":
                try:
                    word = int(line[1], base=16)
                except ValueError:
                    pass
                else:
                    try:
                        d.write(extract_commant(line[2:]) + "\n")
                        # print extract_commant(line[2:])+"\n"
                    except TypeError:
                        pass

    d.close()
    f.close()
    # command = {}
    # for line in f:
    #     if len(line) > 8 and line[8] == ':':
    #         if len(line) > 31:
    #             if len(line) > 39:
    #                 command[''.join(line[:8].split())] = line[32:39]
    #             else:
    #                 command[''.join(line[:8].split())] = line[32:len(line) - 1]
    #         else:
    #             command[line[2:8]] = ""
    # f.close()
    # print command
    #
    # d = open("instructions.txt", "r")
    # instructions = {}
    # for line in d:
    #     instructions[line[:-1]] = 0
    # d.close()
    #
    # for key in command.keys():
    #     command[key] = command[key].split(" ", 2)[0]
    #     if command[key] in instructions.keys():
    #         instructions[command[key]] += 1
    #
    # # for key,value in command.iteritems():
    # #     print(key,value)
    #

    # for key in sorted(instructions.keys()):
    #     d.write(key + " " + str(instructions[key]) + '\n')
    # d.close()


# parse_file()
