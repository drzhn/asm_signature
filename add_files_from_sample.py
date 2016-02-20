import os
from sample_class import SAMPLE

dir = os.listdir("sample")
path = os.path.abspath("sample")+"/"
TS = SAMPLE()
for i in range(len(dir)):
    name = dir[i]
    fullpath = path+dir[i]
    samples = os.listdir(fullpath)
    print(name)
    for j in range(len(samples)):
        TS.add_file(fullpath+"/"+samples[j], name, 0.2, 0.8)
        print("    "+fullpath+"/"+samples[j])

TS.save()