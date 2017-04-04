import csv
import ast
import timeit
import codecs
#from lxml import etree as et
import xml.etree.cElementTree as ET


book1 = []
book2 = []
book3 = []
freq_most_common = []
freq_common = []
named_enteties = []

# ------------------------------------- GDEX POINTS -----------------------------------------------------

# Sentence length: a sentence between 10 and 25 words long was preferred, with longer and shorter ones penalized.
# max Points = 2
def sentence_length(sentence):
    ignore = False
    points = 25
    sentLength = len(sentence)
    if sentLength >= 10 and sentLength <= 25:
        pass
    else:
        if sentLength < 10:
            points = 25 + (sentLength/10)
        if sentLength > 25:
            ignore = True
    return points, ignore

# Word frequencies: a sentence was penalized for each word that was not amongst the commonest 17,000 words in the
# language, with a further penalty applied for rare words.
# max Points = 3
def common_words(sentence):
    points = 0
    x = 100 / len(sentence)
    for word in sentence:
        if word == ['        ']:
            continue
        if word[1] in freq_most_common:
            points += x
        elif word[1] in freq_common:
            points += x/2

    #print("% 100/", points)
    points = 40 * (points/100)
    #print("40/", points)

    return points

# Sentences containing pronouns and anaphors like this that it or one often fail to present a self-contained piece of
# language which makes sense without further context, so sentences containing these words were penalized.
# max Points = 1
def contain_pronouns_anaphors(sentence):
    x = len(sentence)
    found = 0
    for word in sentence:
        if word == ['        ']:
            continue
        if word[3] in ["PP", "PP$"]:
            found += 1

    points = 25 * (found/x)
    return points

# Whole sentenceidentified as beginning with a capital letter and ending with a full step, exclamation mark, or
# question mark, were preferred.
# max Points = 2
def whole_sentence(sentence):
    points = 10
    punctuation = ["!", "\"", ".", "?"]
    first_word = sentence[0]
    last_word = sentence[len(sentence)-1]

    if first_word[0].isupper():
        if last_word[0] in punctuation:
            pass # is upper and has punctuation
        else:
            points -= 5 # is upper and has no punctuation
    else:
        if last_word[0] in punctuation:
            points -= 5 # is not upper and has punctuation
        else:
            points -= 10 # is not upper and has no punctuation

    return points

# ------------------------------------- LEARNER COMPREHENSION POINTS -------------------------------------

def contains_learned_words(s, voc, chapter, book):
    points = 3
    # --------------- Parser ---------------
    #dvoc_parser = et.XMLParser()
    #dvoc_tree = et.parse("../GDEX/voc_1word.xml", dvoc_parser)

    dvoc_tree = ET.ElementTree(file='../voc_1word.xml')

    dvoc_root = dvoc_tree.getroot()

    # --------------- End ---------------
    # In this case words that appear in the book and better yet chapter (or earlier #) of the word
    base_chapter = chapter
    base_book = convertStringtoInt(book)

    len_sent = len(s)
    no_match = len(s)

    for word in s:
        if word == ['        ']:
            continue
        # todo ignore numbers and named enteties
        #current_voc = voc_root.find("vocable[@name='"+word[1]+"']")
        w = word[1].replace("'", "&apos").lower()
        #current_voc = dvoc_tree.xpath("./vocable[@name='" + w + "']")
        current_voc = dvoc_tree.findall("./vocable[@name='"+w+"']")
        #print("voc", current_voc)
        #print(len(current_voc))
        if len(current_voc) == 0:
            #print("no match for: " + word[1])
            no_match -= 1
        else:
            #print(w)
            if base_book >= convertStringtoInt(current_voc[0].find("book").get('name')):
                # is in the same book or earlier
                if base_chapter == 'Welcome':
                    b_chapter = ["0","A"]
                else:
                    b_chapter = base_chapter.split("/")

                if current_voc[0].find("chapter").get('name') == 'Welcome':
                    c = ["0", "A"]
                else:
                    c = current_voc[0].find("chapter").get('name').split("/")

                if int(b_chapter[0]) == int(c[0]):
                    # is in the same chapter
                    if b_chapter[1][:1] < c[1][:1]:
                        no_match -= 0.5

                elif int(b_chapter[0]) < int(c[0]):
                    no_match -= 1

    matched_points = no_match/len_sent
    #print(matched_points, "(",no_match,"/",len_sent,")" )

    return matched_points

def convertStringtoInt(book):
    if book == "I":
        base_book = 1
    if book == "II":
        base_book = 2
    if book == "III":
        base_book = 3

    return base_book

# ------------------------------------- COMPUTE GDEX AND LC POINTS ----------------------------------------

def compute_points(s, voc, chapter, book):
    # ---- GDEX ----
    points1, ignore = sentence_length(s)  # 2p
    if not ignore:
        points2 = common_words(s)  # 3p
        points3 = contain_pronouns_anaphors(s)  # 1p
        points5 = whole_sentence(s)  # 2p

        gdex_points = points1 + points2 + points3 + points5

    else:
        gdex_points = 0

    # ---- LC ----
    learner_points = contains_learned_words(s, voc, chapter, book)

    return round(gdex_points, 1), round(learner_points, 2)

# ------------------------------------- LOAD VOCABULARY ---------------------------------------------------

def load_books():
    with open("matched_vocabulary.csv", 'r') as sentin:
        sentreader = csv.reader(sentin, delimiter=';')
        next(sentreader)

        for v_row in sentreader:
            if v_row[6] == "I":
                #book1.append(ast.literal_eval(v_row[2])) # voc lemma
                book1.append(v_row)
            elif v_row[6] == "II":
                #book2.append(ast.literal_eval(v_row[2])) # voc lemma
                book2.append(v_row)
            elif v_row[6] == "III":
                #book3.append(ast.literal_eval(v_row[2]))  # voc lemma
                book3.append(v_row)
    sentin.close()

# ------------------------------------- LOAD FREQUENCIES --------------------------------------------------

def load_frequencies():
    with open('../lemma.num.txt', 'r') as freqin:
        f = csv.reader(freqin, delimiter=' ')
        row_number = 1
        for row in f:
            if row_number <= 17000:
                freq_most_common.append(row[2])
            else:
                freq_common.append(row[2])
            row_number += 1
    freqin.close()

# ------------------------------------- LOAD NER ----------------------------------------------------------

def load_ner():
    with open('../NER.txt', 'r') as f:
        for ner in f:
            named_enteties.append(ner)
    f.close()

# ------------------------------------- MAIN --------------------------------------------------------------
if __name__ == "__main__":
    start = timeit.default_timer()

    print("#### starting loading vocabulary ####")
    #load_books()
    # --------------- Parser ---------------
    #voc_parser = et.XMLParser()
    #voc_tree = et.parse("../GDEX/voc.xml", voc_parser)

    voc_tree = ET.ElementTree(file='../voc.xml')

    voc_root = voc_tree.getroot()
    # --------------- End ---------------

    print("#### finished loading vocabulary ####")

    print("#### starting loading frequencies ####")
    load_frequencies()
    print("#### finished loading frequencies ####")

    print("#### starting loading NE ####")
    load_ner()
    print("#### finished loading NE ####")

    print("#### starting loading xml ####")
    # --------------- Parser ---------------
    #sent_parser = et.XMLParser(encoding='iso-8859-5', recover = True)
    #sent_tree = et.parse("../GDEX/corpora/xaa.xml", sent_parser)

    tree = ET.ElementTree(file='../corpora/xaa.xml')
    sent_root = tree.getroot()
    # --------------- End ---------------

    with codecs.open('example_sentences.txt', 'w', 'utf-8') as xmlout:

        #sent_root = sent_tree.getroot()
        all_s = []
        for txt in sent_root.findall('text'):
            for sent in txt.findall('s'):
                sentence = []
                line = ((sent.text).split('\n'))
                for word in line:
                    if isinstance(word, list):
                        continue
                    word = word.split('\t')
                    if word == ['']:
                        pass
                    else:
                        sentence.append(word)
                all_s.append(sentence)
        print("#### finished loading xml ####")

        print("#### starting iterating over books ####")
        b = 1
        vf = []
        for xml_voc in voc_root.findall('vocable'):
            voc = xml_voc.get('name')
            chapter = xml_voc.find("chapter").get('name')
            book = xml_voc.find("book").get('name')
            #print(voc, chapter, book)
            #print(voc)
            voc = ast.literal_eval(voc)
            #print(voc)#, voc[0], type(voc[0]))
            if isinstance(voc[0], list):
                #print(" -- list")
                # eg. [['ca', "n't"], ['can', 'not']]
                for v in voc:
                    voc_len = len(v)
                    for s_sentence in all_s:
                        lemma_found = []
                        for lemma in v:
                            find_voc_only_once = False
                            sent = ""
                            for word in s_sentence:
                                if word == ['        ']:
                                    continue
                                if lemma.lower() == word[1].lower():
                                    if not find_voc_only_once:
                                        lemma_found.append("Y")
                                        find_voc_only_once = True
                                sent += word[0] + " "
                        if voc_len == len(lemma_found):
                            #print("found l", v, sent)
                            gdex_points, learner_points = compute_points(s_sentence, voc, chapter, book)
                            if gdex_points > 60:
                                #print(voc, chapter, book)
                                vf.append([gdex_points, learner_points, voc, sent])
                            elif learner_points > 0.6:
                                vf.append([gdex_points, learner_points, voc, sent])
            elif len(voc) > 1:
                #print(" -- mehrere")
                # eg. ['Welcome', 'to', 'Camden', 'Town', '!']
                for s_sentence in all_s:
                    lemma_found = []
                    voc_len = len(voc)
                    #print(voc_len)
                    for v in voc:
                        find_voc_only_once = False
                        sent = ""
                        for word in s_sentence:
                            if word == ['        ']:
                                continue
                            if v.lower() == word[1].lower():
                                if not find_voc_only_once:
                                    lemma_found.append("Y")
                                    find_voc_only_once = True
                            sent += word[0] + " "
                    if voc_len == len(lemma_found):
                        #print("found m", v, sent)
                        gdex_points, learner_points = compute_points(s_sentence, voc, chapter, book)
                        if gdex_points > 60:
                            #print(voc, chapter, book)
                            vf.append([gdex_points, learner_points, voc, sent])
                        elif learner_points > 0.6:
                            vf.append([gdex_points, learner_points, voc, sent])
            else:
                # ['see']
                #print(" -- einzeln")
                for s_sentence in all_s:
                    sent = ""
                    lemma_found = False
                    for word in s_sentence:
                        if word == ['        ']:
                            continue
                        sent += word[0] + " "
                        if voc[0].lower() == word[1].lower():
                            lemma_found = True
                    if lemma_found:
                        #print("found e", voc, sent)
                        gdex_points, learner_points = compute_points(s_sentence, voc, chapter, book)
                        if gdex_points > 60:
                            #print(voc, chapter, book)
                            vf.append([gdex_points, learner_points, voc, sent])
                        elif learner_points > 0.6:
                            vf.append([gdex_points, learner_points, voc, sent])

        with open("../output/sentences.txt", "w") as s_out:
            for found_s in vf:
                #print(found_s)
                s_out.write(str(found_s)+"\n")
        s_out.close()
