# -*- coding: utf-8 -*-
class SAMPLE:
    m = 0
    files_frequency = {}
    S = {}

    #считаем выборку из файла
    def __init__(self):
        try:
            file=open("AC","r")
        except IOError:
            file = open("AC","w")
            file.write("0")
            file.close()
        file = open("AC", "r")
        lines = file.readlines()
        self.m = int(lines[0])
        name = ""
        # if self.m == 0:
        #     return
        next = 1
        for i in range(self.m):
            line = lines[next].split(" ")
            name = line[0]
            n = int(line[1])
            self.files_frequency[name] = [n, []]
            for j in range(n):
                self.files_frequency[name][1].append([])
                line = lines[j+next+1].split(" ",118)
                for k in range(118):
                    self.files_frequency[name][1][j].append(int(line[k]))
            next = next+n + 1
        for i in range(self.m):
            line = lines[next + i].split(" ", 119)
            # print line
            name = line[0]
            self.S[name] = []
            for j in range(1, 119):
                self.S[name].append(int(line[j]))
        file.close()


    def save(self):
        file = open("AC", "w")
        file.write(str(self.m)+"\n")
        for key in sorted(self.files_frequency.keys()):
            file.write(key+" ")
            file.write(str(self.files_frequency[key][0])+"\n")
            for i in range(len(self.files_frequency[key][1])):
                for j in range(117):
                    file.write(str(self.files_frequency[key][1][i][j])+" ")
                file.write(str(self.files_frequency[key][1][i][117])+"\n")
        for key in sorted(self.S.keys()):
            file.write(key+" ")
            for i in range(117):
                file.write(str(self.S[key][i])+" ")
            file.write(str(self.S[key][117])+"\n")
        file.close()

    def add_file(self, path, name, k, s):
        file = open(path, "r")
        L = []
        for line in file:
            line = line.split(" ")
            L.append(int(line[1]))
        if not name in self.S.keys():
            self.m += 1
            self.files_frequency[name] = [1, []]
            self.files_frequency[name][1].append(L)
            self.S[name] = L
        else:
            L_average = []
            self.files_frequency[name][0] += 1
            self.files_frequency[name][1].append(L)

            n = self.files_frequency[name][0]
            for i in range(118):
                temp = 0
                for j in range(n):
                    temp += self.files_frequency[name][1][j][i]
                temp = temp/n
                L_average.append(temp)

            Mf = []
            for i in range(n):
                Mf.append([])
                for j in range(118):
                    if abs(L_average[j]-self.files_frequency[name][1][i][j]) <= k * L_average[j]:
                        Mf[i].append(1)
                    else:
                        Mf[i].append(0)
            Mv = []
            for i in range(118):
                number = 0
                for j in range(n):
                    number += Mf[j][i]
                if number >= s * n:
                    Mv.append(L_average[i])
                else:
                    Mv.append(0)
            self.S[name] = Mv
        file.close()

    def check_file(self, path, percent):
        file = open(path,"r")
        L = []
        for line in file:
            line = line.split(" ")
            L.append(int(line[1]))
        found = 0
        for name in sorted(self.S.keys()):
            d_positive = 0
            d_negative = 0
            for j in range(118):
                if abs(L[j]-self.S[name][j]) <= 0.2*self.S[name][j]:
                    d_positive += 1
                else:
                    d_negative += 1
            print name+": "+str(d_positive - d_negative),
            if d_positive-d_negative > 0:
                print "<-MATCH!"
                found += 1
            else:
                print ""
        if found == 0:
            print "Can't identify\n"
        file.close()

    def check_pearson(self, path):
        file_check = open(path,"r")
        L = []
        for line in file_check:
            line = line.split(" ")
            L.append(int(line[1]))
        name = "aircrack"
        if name in self.S.keys():
        # for name in sorted(self.S.keys()):
            template = []
            file = []
            template_plus_file = []
            sum_template = 0
            sum_file = 0
            sum_template_plus_file = 0
            for i in range(len(self.S[name])):
                if self.S[name][i] != 0:
                    template.append(self.S[name][i])
                    file.append(L[i])
                    template_plus_file.append(L[i] + self.S[name][i])

                    sum_template += self.S[name][i]
                    sum_file += L[i]
                    sum_template_plus_file += L[i] + self.S[name][i]
            print "template", template
            print "file    ", file
            print "temp+fil", template_plus_file

            print "sum temp", sum_template
            print "sum file", sum_file
            print "sum gene", sum_template_plus_file
            theoretical_template = []
            theoretical_file = []
            for i in range(len(template)):
                theoretical_template.append(template_plus_file[i] * sum_template / float(sum_template_plus_file))
                theoretical_file.append(template_plus_file[i] * sum_file / float(sum_template_plus_file))
            percentage = []
            accumulation = []
            for i in range(len(template)):
                percentage.append(abs(template[i] - theoretical_template[i]) / theoretical_template[i])
            print percentage[0]
            accumulation.append(percentage[0])
            for i in range(1, len(template)):
                accumulation.append(percentage[i] + accumulation[i-1])

            print path.split("/")[-1], " - ", name, " - ",accumulation[-1]
        file_check.close()

TS = SAMPLE()
TS.check_pearson("aircrack-ng3")
TS.save()


#
# file = open("file","r")
# m = file.read()
# print m