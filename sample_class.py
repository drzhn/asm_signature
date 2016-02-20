# -*- coding: utf-8 -*-
from math import sqrt, asin
from collections import deque


class SAMPLE:
    m = 0
    files_frequency = {}
    S = {}

    # считаем выборку из файла
    def __init__(self):
        try:
            file = open("AC", "r")
        except IOError:
            file = open("AC", "w")
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
                line = lines[j + next + 1].split(" ", 118)
                for k in range(118):
                    self.files_frequency[name][1][j].append(int(line[k]))
            next = next + n + 1
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
        file.write(str(self.m) + "\n")
        for key in sorted(self.files_frequency.keys()):
            file.write(key + " ")
            file.write(str(self.files_frequency[key][0]) + "\n")
            for i in range(len(self.files_frequency[key][1])):
                for j in range(117):
                    file.write(str(self.files_frequency[key][1][i][j]) + " ")
                file.write(str(self.files_frequency[key][1][i][117]) + "\n")
        for key in sorted(self.S.keys()):
            file.write(key + " ")
            for i in range(117):
                file.write(str(self.S[key][i]) + " ")
            file.write(str(self.S[key][117]) + "\n")
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
                temp = temp / n
                L_average.append(temp)

            Mf = []
            for i in range(n):
                Mf.append([])
                for j in range(118):
                    if abs(L_average[j] - self.files_frequency[name][1][i][j]) <= k * L_average[j]:
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
        print path
        file = open(path, "r")
        L = []
        for line in file:
            line = line.split(" ")
            L.append(int(line[1]))
        found = 0
        for name in sorted(self.S.keys()):
            d_positive = 0
            d_negative = 0
            for j in range(118):
                if abs(L[j] - self.S[name][j]) <= 0.2 * self.S[name][j]:
                    d_positive += 1
                else:
                    d_negative += 1
            # print "     ",name + ": " + str(d_positive - d_negative),
            if d_positive - d_negative > 0:
                print "     ", name + ": " + str(d_positive - d_negative),
                print "<-MATCH!"
                found += 1
            else:
                pass
                # print ""
        if found == 0:
            print "Can't identify\n"
        file.close()

    def check_pearson(self, path):
        file_check = open(path, "r")
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
                accumulation.append(percentage[i] + accumulation[i - 1])

            print path.split("/")[-1], " - ", name, " - ", accumulation[-1]
        file_check.close()

        # TS = SAMPLE()
        # TS.check_pearson("aircrack-ng3")
        # TS.save()


        #
        # file = open("file","r")
        # m = file.read()
        # print m

    def check_fisher(self, path):
        # Будем делить пополам
        L = []
        for line in open(path, "r"):
            line = line.split(" ")
            L.append(int(line[1]))
        eff = 0
        noeff = 0
        for i in range(59):
            eff += L[i]
            noeff += L[i + 59]
        eff = eff * 1500 / max(eff, noeff)
        noeff = noeff * 1500 / max(eff, noeff)
        sum_l = eff + noeff
        eff = noeff / float(eff + noeff)
        print "eff:", eff
        for name in sorted(self.S.keys()):
            eff_s = 0
            noeff_s = 0
            for i in range(59):
                eff_s += self.S[name][i]
                noeff_s += self.S[name][i + 59]
            eff_s = eff_s * 1500 / max(eff_s, noeff_s)
            noeff_s = noeff_s * 1500 / max(eff_s, noeff_s)
            sum_s = eff_s + noeff_s
            eff_s = noeff_s / float(eff_s + noeff_s)
            print "eff_s:", eff
            phi1 = asin(sqrt(eff / 100.0))
            phi2 = asin(sqrt(eff_s / 100.0))
            phi_emp = abs(phi1 - phi2) * sqrt(sum_l * sum_s / float(sum_s + sum_l))
            print name, phi_emp
            print "____________________________"

    def check_ks(self, path):
        d = open("instructions.txt", "r")
        instructions = {}
        for line in d:
            instructions[line[:-1]] = 0
        d.close()

        L_dict = {}
        l_max = 0
        L = []
        for line in open(path, "r"):
            line = line.split(" ")
            L.append(int(line[1]))
            if L[-1] > l_max:
                l_max = L[-1]

        # for i in range(118):
        #     L[i] = L[i] * 1500 / float(l_max)

        for name in sorted(self.S.keys()):
            s_max = 0
            for i in range(118):
                L_dict[L[i]] = self.S[name][i]
                if self.S[name][i] > s_max:
                    s_max = self.S[name][i]

            # for key in sorted(L_dict.keys()):
            #     L_dict[key] = L_dict[key] * 1500 / float(s_max)

            sum_s = 0
            sum_l = 0
            for key in sorted(L_dict.keys()):
                if L_dict[key] != 0 and key != 0:
                    sum_s += L_dict[key]
                    sum_l += key

            s = 0.0
            l = 0.0
            d_max = 0.0
            for key in sorted(L_dict.keys()):
                s += L_dict[key] / float(sum_s)
                l += key / float(sum_l)
                if L_dict[key] != 0 and key != 0:
                    if abs(s - l) > d_max:
                        d_max = abs(s - l)
            lambda_emp = d_max * sqrt(sum_l * sum_s / float(sum_l + sum_s))
            print "_____________________"
            print name
            print "lambda =", lambda_emp
            print "n1:", sum_l
            print "n2:", sum_s
            # print "sum S:",sum_s
            print "dmax:", d_max
            print "sqrt:", sqrt(sum_l * sum_s / float(sum_l + sum_s))

    def check_distance(self, path):
        L = []
        for line in open(path, "r"):
            line = line.split(" ")
            L.append(int(line[1]))
        results = []
        for name in sorted(self.S.keys()):
            d = 0.0
            for i in range(118):
                d += (L[i] - self.S[name][i]) ** 2
            results.append([name, sqrt(d)])

        r_index = 0
        r = results[0][1]
        r_max = 0.0
        r_min = results[0][1]
        for i in range(len(results)):
            if results[i][1] < r:
                r_min = r
                r = results[i][1]
                r_index = i
            if results[i][1] > r_max:
                r_max = results[i][1]
        for i in range(len(results)):
            print results[i],
            if i == r_index:
                print "<== MATCH!"
            else:
                print
        print "ratio:", r_min / r  # ((r_max + r_min) / 2.0 - (r_max - r_min)) / r

    def check_potential(self, path):
        L = []
        for line in open(path, "r"):
            line = line.split(" ")
            L.append(int(line[1]))
        results = []
        for name in self.files_frequency.keys():
            n = self.files_frequency[name][0]
            average = []
            for i in range(118):
                sum = 0
                for j in range(n):
                    sum += self.files_frequency[name][1][j][i]
                average.append(sum / float(n))
            d = 0.0
            for i in range(118):
                d += (L[i] - average[i]) ** 2

            try:
                results.append([name, sqrt(d), 1 / (d ** 4)])
            except ZeroDivisionError:
                results.append([name, sqrt(d), float("Inf")])
        r_index = 0
        r = 0.0
        r_max = 0.0
        r_min = results[0][2]
        for i in range(len(results)):
            if results[i][2] > r:
                r_max = r
                r = results[i][2]
                r_index = i
            if results[i][2] < r_min:
                r_min = results[i][2]

        # for i in range(len(results)):
        #     str = ""
        #     if i == r_index:
        #         str = "<== MATCH!"
        #     print "{0:<10} {1:<17} {2}".format(results[i][0], results[i][2], str)
        print path
        path = path[path.rfind("/") + 1:]
        path = path[:path.find("_")] + path[path.rfind("_"):]

        # print "  {0:<10} {1:<17}".format(results[r_index][0], results[r_index][2]),
        for i in range(len(results)):
            str = ""
            if i == r_index:
                str = "<===Match!"
            print "    {0:<24} {1:<17} {2}".format(results[i][0], results[i][2], str)

        if path == results[r_index][0]:
            return 1
        else:
            return 0
            # return 0


            # print "ratio:", r / ((r_max + r_min) / 2.0 + (r_max - r_min))

    def calc_distance(self, a, b):
        d = 0.0
        for i in range(118):
            d += (a[i] - b[i]) ** 2
        return sqrt(d)

    def check_knn(self, path):
        K = 1
        queue = deque([0 for i in range(K)])
        names = deque(["" for i in range(K)])
        L = []
        for line in open(path, "r"):
            line = line.split(" ")
            L.append(int(line[1]))
        results = []
        for name in self.files_frequency.keys():
            n = self.files_frequency[name][0]
            for i in range(n):
                potential = 1 / (self.calc_distance(L, self.files_frequency[name][1][i])) ** 2
                if potential >= queue[-1]:
                    queue.append(potential)
                    queue.popleft()
                    names.append(name)
                    names.popleft()
                if K > n:
                    max_p = 0.0
                    for i in range(n):
                        potential = 1 / (self.calc_distance(L, self.files_frequency[name][1][i])) ** 2
                        if potential > max_p:
                            max_p = potential

                    for i in range(n- K):
                        if max_p >= queue[-1]:
                            queue.append(max_p)
                            queue.popleft()
                            names.append(name)
                            names.popleft()
        sum = 0.0
        namesset = {}
        for i in range(K):
            sum += queue[i]
            if names[i] in namesset.keys():
                namesset[names[i]] += queue[i]
            else:
                namesset[names[i]] = queue[i]

        path = path[path.rfind("/") + 1:]
        path = path[:path.find("_")] + path[path.rfind("_"):]
        print path + ":",

        max = 0.0
        max_name = ""
        for name in namesset.keys():
            print name, namesset[name] / sum * 100,
            if namesset[name] / sum * 100 > max:
                max = namesset[name] / sum * 100
                max_name = name
        if path == max_name:
            print "<===Match!"
            return 1
        else:
            print
            return 0
