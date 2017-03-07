import xml.etree.ElementTree as ET
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import csv

tree_b1 = ET.parse('../01_extract_sentences/book_1.xml')
root_b1 = tree_b1.getroot()

tree_b2 = ET.parse('../01_extract_sentences/book_2.xml')
root_b2 = tree_b2.getroot()

tree_b3 = ET.parse('../01_extract_sentences/book_3.xml')
root_b3 = tree_b3.getroot()

#print(root.tag)

lemmatizer = WordNetLemmatizer()
id = 1


def extract(root, book_nr, id):
    for page in root.findall('page'):
        p = page.get('id')
        chapter = page.find('chapter').text
        sentence = page.findall('sentence')
        # print(p, chapter)
        for s in sentence:
            tokenized = word_tokenize(s.text)
            # todo tagged
            #tagged = nltk.pos_tag(tokenized)
            # todo string-lemma dict
            map = {}
            lemma = []
            for item in tokenized:
                #print("item", item)
                lemma.append(lemmatizer.lemmatize(item))
                if lemmatizer.lemmatize(item) in map:
                    map[lemmatizer.lemmatize(item)].append(item)
                else:
                    map[lemmatizer.lemmatize(item)] = [item]
            # print(s.text, tokenized)
            # print(type(chapter))
            if not chapter == "DELETE":
                # todo tagged vs dict
                writer.writerow([id, chapter, book_nr, p, s.text, map, lemma])
                id = id + 1
    return id


with open('sentences_all_test_map.csv', 'w') as outcsv:
    writer = csv.writer(outcsv, delimiter=';')
    writer.writerow(["_id", "Chapter", "Book", "Page", "Sentence", "Tagged", "Lemma"])

    id = extract(root_b1, "I", id)
    id = extract(root_b2, "II", id)
    extract(root_b3, "III", id)

outcsv.close()