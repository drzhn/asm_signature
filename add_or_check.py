import sys
from sample_class import SAMPLE

TS = SAMPLE()
# print len(sys.argv)

if sys.argv[1] == "-a":
    path = sys.argv[2]
    name = sys.argv[3]
    percent  = sys.argv[4]
    TS.add_file(path, name, k=0.2, s=0.8)
    TS.save()
if sys.argv[1] == "-i":
    path = sys.argv[2]
    # percent  = sys.argv[3]
    # TS.check_file(path, percent)
    # TS.check_fisher(path)
    # TS.check_ks(path)
    TS.check_potential(path)
    TS.save()
if sys.argv[1] != "-a" and sys.argv[1] != "-i":
    print "Unknown command\n"
