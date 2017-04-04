with open("xaa_groß.xml", 'r', encoding='iso-8859-5') as xmlin, open('xaa_fixed.xml', 'w', encoding='iso-8859-5') as xmlout:
    xmlout.write("<start>\n")
    for line in xmlin:
        if line.startswith("<text"):
            xmlout.write("<text>\n")
        elif  "&" in line:
            xmlout.write(line.replace("&", "and"))
        #elif "@" in line:
        #    xmlout.write(line.replace("@", "_at_"))
        else:
            xmlout.write(line)

    xmlout.write("</start>")

xmlout.close()
xmlin.close()