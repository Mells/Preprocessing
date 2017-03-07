import re
import nltk.data
import csv
from string import digits

PAGE_START = "**************************** Page "
PAGE_END = "****************************"
P_START_TAG1 = "<page id='"
P_START_TAG2 = "'>"
P_END_TAG = "</page>"
CHAPTER_START = "<chapter>"
CHAPTER_END = "</chapter>"
EXERCISE_START = "<exercise>"
EXERCISE_END = "</exercise>"
LISTING_START = "<listing>"
LISTING_END = "</listing>"
FILLIN_START = "<gap>"
FILLIN_END = "</gap>"
SENTENCE_START = "<sentence>"
SENTENCE_END = "</sentence>"
FOOT_START = "<footnote>"
FOOT_END = "</footnote>"

book = "CTG1_Textbuch_un8.txt"
xml_file = 'book_1_old.xml'
chapters = 'Kapitel_B01.csv'

sentences = []

file_xml = open(xml_file, 'w+')

with open(chapters, mode='r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    mydict = {rows[0]:rows[1] for rows in reader}

#print(mydict)

sentences.append("<document>")
file_xml.write("<document>\n")

with open(book) as f:
    atBeginning = True
    for line in f:
        line = line.strip()
        print(type(line), line)
        if line.isdigit():
            print("isdigit")
            nextLine = next(f)
            nextLine = nextLine.strip().strip(" ")
            print(type(nextLine), nextLine)
            if nextLine in mydict:
                print("found")
                if (atBeginning):
                    print("atBeginning")
                    file_xml.write(P_START_TAG1 + line + P_START_TAG2 + "\n")
                    file_xml.write(CHAPTER_START + nextLine + CHAPTER_END  + "\n")
                    atBeginning = False
                else:
                    file_xml.write(P_END_TAG + "\n")
                    file_xml.write(P_START_TAG1 + line + P_START_TAG2 + "\n")
                    file_xml.write(CHAPTER_START + nextLine + CHAPTER_END + "\n")
                continue
            else:
                file_xml.write(EXERCISE_START + line + EXERCISE_END + "\n")
                line = nextLine

        if line in ["Personal Trainer", "Photo page", "Optional"]:
                line = CHAPTER_START + "DELETE" + CHAPTER_END
        elif re.match("[A-Z] [0-9]|[A-Z][0-9]", line) or re.match("[a-z]\)", line) or "∙" in line \
                or line[0].isdigit() or line.startswith(".. WB"):
            #if line.strip().isdigit():
            #    continue
            #line = EXERCISE_START + line + EXERCISE_END
            #file_xml.write(EXERCISE_START + line + EXERCISE_END + "\n")
            pass
        else:
            file_xml.write(SENTENCE_START + line + SENTENCE_END + "\n")

file_xml.write(P_END_TAG  + "\n")
file_xml.write("</document>")
file_xml.close()


#for item in sentences:
    #print(item)
    #if CHAPTER_START in item:
    #   print(item)
