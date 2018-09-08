import sys

def main(argv):
    buf = open(argv[0]).read().split('\n')
    print len(buf)
    j = 0
    vmbuf = range(len(buf))
    conbuf = range(len(buf))
    for i in range(len(buf)-1):
        #print i
        if not buf[i]:
            continue
        new = buf[i].split(' ')
        #print new
        #newbuf[j] = buf[i]
        vmbuf[j] = new[0]
        conbuf[j] = buf[i]
        #print vmbuf[j]
        j = j + 1
  
    if j < len(vmbuf):
       for x in range (j, len(vmbuf)):
           vmbuf[x] = '\n'
    #for i in range(j):
    #    print "VM:", vmbuf[i]
    vmset = set(vmbuf)
    #print j
    vmlist = list(vmset)
    print "Number of VMs", len(vmlist)

    if j < len(conbuf):
       for x in range (j, len(conbuf)):
           conbuf[x] = '\n'
    conset = set(conbuf)
    conlist = list(conset)
    print "Number of Containers", len(conlist)
    #for i in range(len(conlist)):
    #    print "Container:", conlist[i]
    #if j < len(newbuf):
    #    for x in range (j, len(newbuf)):
    #        newbuf[x] = '\n'
    #print len(myset)
    #mylist = list(myset)
    #for i in range(j):
    #   print i, newbuf[i]
    #print "unique:",len(set(newbuf))
if __name__ == "__main__":
   main(sys.argv[1:])