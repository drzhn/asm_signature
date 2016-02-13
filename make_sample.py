import os, subprocess
from parser import parse_file

listdir = os.listdir("sample_bin")
# print(dir)
# print(os.listdir("sample/"+dir[0]))
path = os.path.abspath("sample_bin") + "/"

if not os.path.exists("sample"):
    os.makedirs("sample")
outpath = os.path.abspath("sample") + "/"
# print path, outpath

for i in range(len(listdir)):
    name = listdir[i]
    fullpath = path + listdir[i] + "/"
    samples = os.listdir(fullpath)
    print(name)
    if not os.path.exists(outpath+name):
        os.makedirs(outpath+name)

    for j in range(len(samples)):
        devnull = open("/dev/null", "w")
        retcode = subprocess.call(
            ["objdump -D -M intel " + fullpath + samples[j] + " > asm.txt"],
            shell=True, stderr=devnull)
        parse_file(samples[j],name)
        devnull.close()
        # print("     objdump -D -M intel "+fullpath+"/"+samples[j]+" > /home/klever/Projects/python/asm_signature/asm.txt")
        print("    " + fullpath + "/" + samples[j])