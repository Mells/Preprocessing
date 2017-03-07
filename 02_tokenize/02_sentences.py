import xml.etree.ElementTree as ET
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import csv

tree = ET.parse('../01_extract_sentences/book_3.xml')
root = tree.getroot()

#print(root.tag)

lemmatizer = WordNetLemmatizer()
book_nr = "III"

with open('sentences_b03.csv', 'w') as outcsv:
    writer = csv.writer(outcsv, delimiter=';')
    writer.writerow(["Id", "Chapter", "Book", "Page", "Sentence", "Tagged", "Lemma"])

    id = 1
    for page in root.findall('page'):
        p = page.get('id')
        chapter = page.find('chapter').text
        sentence = page.findall('sentence')
        #print(p, chapter)
        for s in sentence:
            tokenized = word_tokenize(s.text)
            tagged = nltk.pos_tag(tokenized)
            lemma = []
            for item in tokenized:
                lemma.append(lemmatizer.lemmatize(item))
            #print(s.text, tokenized)
            #print(type(chapter))
            if not chapter == "DELETE":
                writer.writerow([id, chapter, book_nr, p, s.text, tagged, lemma])
                id = id + 1
outcsv.close()