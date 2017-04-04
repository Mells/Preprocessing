with open("xaa_fixed.xml", 'r', encoding='iso-8859-5') as xmlin:
    lnr = 1
    for line in xmlin:
        if lnr in [714, 715, 716]:
            print(line)
        lnr += 1

xmlin.close()