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

book = "CTG3_Textbuch.txt"
xml_file = 'book_3_edit_wo_delete.xml'
chapters = 'Kapitel_B03.csv'

sentences = []

file_xml = open(xml_file, 'w+')

with open(chapters, mode='r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    mydict = {rows[0]:rows[1] for rows in reader}

#print(mydict)

sentences.append("<document>")
file_xml.write("<document>\n")

with open(book) as f:
    at_beginn = True
    after_page = False
    for line in f:
        line = line.strip()
        if len(line) == 0:
            continue
        elif line.startswith(PAGE_START):
            after_page = True
            if not at_beginn:
                sentences.append(P_END_TAG)
                file_xml.write(P_END_TAG + "\n")
            line = line.replace(PAGE_START, P_START_TAG1)
            line = line.replace(PAGE_END, P_START_TAG2)

            at_beginn = False

        elif after_page:
            remove_digits = str.maketrans('', '', digits)
            res = line.translate(remove_digits).strip()

            if len(res) == 0:
                continue

            if res == "George’s fi rst day at school" or res == "Caroline’s fi rst day at school":
                res = res.replace("fi rst", "first")

            if res in mydict:
                line = CHAPTER_START + mydict[res] + CHAPTER_END
            elif res in ["Personal Trainer", "Photo page", "Optional"]:
                line = CHAPTER_START + "DELETE" + CHAPTER_END
            else:
                line = CHAPTER_START + "FILL IN (" + res + ")" + CHAPTER_END
            after_page = False

        elif re.match("[A-Z] [0-9]|[A-Z][0-9]", line) or re.match("[a-z]\)", line) or "∙" in line or line[0].isdigit():
            if line.strip().isdigit():
                continue
            line = EXERCISE_START + line + EXERCISE_END

        elif " · " in line:
            line = LISTING_START + line + LISTING_END

        elif "…" in line:
            line = FILLIN_START + line + FILLIN_END

        elif line.startswith("A | B | C"):
            line = FOOT_START + line + FOOT_END

        else:
            # possible more than one sentence per line
            tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
            data = tokenizer.tokenize(line)
            for sentence in data:
                sentences.append(SENTENCE_START + sentence + SENTENCE_END)
                file_xml.write(SENTENCE_START + sentence + SENTENCE_END+"\n")
                                #print(sentence)
            continue

        sentences.append(line)
        file_xml.write(line+"\n")

sentences.append(P_END_TAG)
sentences.append("</document>")

file_xml.write(P_END_TAG + "\n")
file_xml.write("</document>")
file_xml.close()


for item in sentences:
    #print(item)
    if CHAPTER_START in item:
        print(item)
