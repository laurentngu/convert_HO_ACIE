import re,time

def vlookup(dict,targetcellref):
    for z in dict.keys():
        if (z == str(targetcellref)):
            return str(dict[z])
    return

def deltaho(y1,y2,pathfile):
    diff1=eval(y1)-eval(y2)
    display_diff1=repr(diff1)
    print ("diff length deleted=",len(display_diff1))
    f1=open(pathfile,'w')
    f1.write(display_diff1)
    f1.close()


def replaceci_new(acie1):
    i = 0
    resultat = ''
    f1 = open(acie1, 'r')

    dict = {}
    table = []

    for k in f1:
        if (i==1):
            if (k.split(";")[201]=="CellGlobalIdentity" and k.split(";")[340]=="RnlAdjWhereTarget"):
                acie_status="new"

            else:
                if (k.split(";")[192]=="CellGlobalIdentity" and k.split(";")[330]=="RnlAdjWhereTarget"):
                    acie_status="old"

        if (i > 1):
            # new format
            if (acie_status=="new"):
                CellGlobalIdentity = k.split(";")[201]
                RnlAdjWhereTarget = k.split(";")[340]

            if (acie_status=="old"):
                CellGlobalIdentity = k.split(";")[192]
                RnlAdjWhereTarget = k.split(";")[330]

            k = k.split(";")[1] + ";" + CellGlobalIdentity + ";" + RnlAdjWhereTarget + "\n"
            table.append(k)
            b = k.split(";")[0]
            b = b.replace('{ applicationID "A1353RA_17ac0122", cellRef ', "").replace('}', '')
            c = k.split(";")[1].split(",")[3].replace("ci ", "").replace("}", "").replace(" ", "")
            dict[b] = c
        i = i + 1

    f1.close()


    for k in table:
        c = k.split(";")[1]
        c = c.split(",")[3].replace('ci ', '').replace('}', '').replace(" ", "")
        d = k.split(";")[2].replace("},", " ,").replace("}}\n", "").replace("cellRef", "").replace(" ", "").split(",")

        for n in d:
            if (n.isdigit()):
                # n  #####  list of target cellref
                resultat = resultat + "(" + c + "," + vlookup(dict,n) + "),"


    resultat = re.sub("\),$", ")}", resultat)
    resultat = re.sub("^\(", "{(", resultat)
    return resultat

# MAIN
start_time=time.time()
y1=replaceci_new('E:\\SWAP_PART2\\OCA\\YOUSSEF\\Cell_0303.csv')
y2=replaceci_new('E:\\SWAP_PART2\\OCA\\YOUSSEF\\Cell_2607.csv')

deltaho(y1,y2,'E:\\SWAP_PART2\\OCA\\YOUSSEF\\DELETED.csv')
deltaho(y2,y1,'E:\\SWAP_PART2\\OCA\\YOUSSEF\\ADDED.csv')

print ("%f seconds" % (time.time() - start_time))