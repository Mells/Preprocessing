from lxml import etree as et
import nltk
import xml.etree.cElementTree as ET
import csv
import ast


def create_text():
    parser = et.XMLParser(encoding='iso-8859-5', recover = True)
    tree = et.parse("xaa.xml", parser)

    root = tree.getroot()

    with open("xml_as_text.txt", "w") as txtout:

        for txt in root.findall('text'):
            for sentence in txt.findall('s'):
                sent = ""

                is_single_open = False

                line = sentence.text.split('\n')

                for word, next_word in zip(line, line[1:] + [line[0]]):
                    if word == '' :
                        continue

                    word = word.split('\t')
                    next_word = next_word.split('\t')

                    if next_word[0] in [",", ".", "'", ")"]:
                        sent += word[0]
                    elif next_word[0] == "n't":
                        sent += word[0]
                    elif next_word[0] == "'re":
                        sent += word[0]
                    elif next_word[0] == "'s":
                        sent += word[0]
                    elif next_word[0] == "'ll":
                        sent += word[0]
                    elif next_word[0] == ":":
                        sent += word[0]
                    elif word[0] == "(":
                        sent += word[0]
                    elif word[0] == "'":
                        if is_single_open:
                            sent += word[0] + " "
                            is_single_open = False
                        else:
                            sent += word[0]
                            is_single_open = True
                    else:
                        sent += word[0] + " "
                txtout.write(sent+"\n")


def create_NER():
    f = open('xml_as_text.txt')
    document = f.read()

    with open("NER.txt", "w") as txtout:
        sentences = nltk.sent_tokenize(document)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]

        continuous_chunk = []
        for item in sentences:
            #print(nltk.ne_chunk(item, binary=True))
            chunked = nltk.ne_chunk(item, binary=True)
            prev = None

            current_chunk = []
            for i in chunked:
                if type(i) == nltk.Tree:
                    current_chunk.append(" ".join([token for token, pos in i.leaves()]))
                elif current_chunk:
                    named_entity = " ".join(current_chunk)
                    if named_entity not in continuous_chunk:
                        more_words = named_entity.split(" ")
                        print(len(more_words))
                        if len(more_words) > 1:
                            continuous_chunk.append(named_entity)
                            for word in more_words:
                                if word not in continuous_chunk:
                                    continuous_chunk.append(word)
                        else:
                            continuous_chunk.append(named_entity)
                        current_chunk = []
                    else:
                        continue
        for ne in continuous_chunk:
            txtout.write(ne+"\n")

def create_vocabulary_xml():
    with open("matched_vocabulary.csv", 'r') as vocin:
        sentreader = csv.reader(vocin, delimiter=';')
        next(sentreader)

        root = ET.Element("root")

        for v_row in sentreader:
            toList = ast.literal_eval(v_row[2])
            if len(toList) == 1:
                doc = ET.SubElement(root, "vocable", name=toList[0])
                ET.SubElement(doc, "chapter", name=v_row[5])
                ET.SubElement(doc, "book", name=v_row[6])


    tree = ET.ElementTree(root)
    tree.write("voc_1word.xml")


if __name__ == "__main__":
    #create_text()
    #create_NER()
    create_vocabulary_xml()