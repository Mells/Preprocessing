with open("../corpora/xaa.xml", 'r', encoding='unicode') as xmlin:
    lnr = 1
    print_line = [714, 715, 716]
    for line in xmlin:
        if lnr in print_line:
            print(line)
            if lnr == print_line[len(print_line)-1]:
                break
        lnr += 1

xmlin.close()