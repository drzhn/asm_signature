import os, subprocess
from sample_class import SAMPLE
dir = os.listdir("sample")
# print(dir)
# print(os.listdir("sample/"+dir[0]))
path = os.path.abspath("sample")+"/"
TS = SAMPLE()
for i in range(len(dir)):
    name = dir[i]
    fullpath = path+dir[i]
    samples = os.listdir(fullpath)
    print(name)
    for j in range(len(samples)):
        TS.add_file(fullpath+"/"+samples[j], name, 0.2, 0.8)
        # devnull = open("/dev/null", "w")
        # retcode = subprocess.call(
        #     ["./asm_signature_core -a "+fullpath+"/"+samples[j]+ " " + name],
        #     shell=True, stderr=devnull)
        # devnull.close()
        print("    "+fullpath+"/"+samples[j])

TS.save()