import csv
import ast
import operator
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

with open("../03_match_vocabulary_to_sentences/matched_vocabulary.csv", 'r') as v_read, \
        open("../GDEX/output/sentences_parts.txt", 'r') as s_read, \
        open("new_sentences.csv", 'w') as s_write, \
        open("new_voc_index.csv", 'w') as v_write:

    vocreader = csv.reader(v_read, delimiter=';')
    sentwriter = csv.writer(s_write, delimiter=';')
    vocwriter = csv.writer(v_write, delimiter=';')
    
    vocwriter.writerow(["Lemma"] + ["GDEX"] + ["Learner"])
    sentwriter.writerow(["_id"] + ["Chapter"] + ["Book"] + ["Page"] + ["Sentence"] + ["Tagged"] + ["Lemma"])

    all_sentences = []
    all_used_sentences = []

    for sentence in s_read:
        all_sentences.append(ast.literal_eval(sentence))

    # for every vocable get the 5(?) best gdex and learner sentences
    next(vocreader)
    for v_row in vocreader:
        v_list = v_row[2]  # Lemma
        print(v_list)
        v_list = ast.literal_eval(v_list)

        found_sentences = []
        for sent in all_sentences:
            if sent[2] == v_list:
                found_sentences.append(sent)
        sorted_gdex_sentences = sorted(found_sentences, key=operator.itemgetter(0), reverse=True)
        sorted_learner_sentences = sorted(found_sentences, key=operator.itemgetter(1), reverse=True)

        #take the best 5 (or less) sentences
        if len(sorted_gdex_sentences) > 5:
            primed_gdex_sentences = [sorted_gdex_sentences[0], sorted_gdex_sentences[1], sorted_gdex_sentences[2],
                                 sorted_gdex_sentences[3] ,sorted_gdex_sentences[4]]
        else:
            primed_gdex_sentences = sorted_learner_sentences

        if len(sorted_learner_sentences) > 5:
            primed_learner_sentences = [sorted_learner_sentences[0], sorted_learner_sentences[1], sorted_learner_sentences[2],
                                        sorted_learner_sentences[3], sorted_learner_sentences[4]]
        else:
            primed_learner_sentences = sorted_learner_sentences

        # add the sentences to the overall list of all used sentences
        for s in primed_gdex_sentences:
            if s not in all_used_sentences:
                all_used_sentences.append(s)

        for s in primed_learner_sentences:
            if s not in all_used_sentences:
                all_used_sentences.append(s)

        # reference the vocabulary to the index of the sentence
        gdex_list = []
        learner_list = []

        for s in primed_gdex_sentences:
            index = all_used_sentences.index(s)
            gdex_list.append(index + 1)

        for s in primed_learner_sentences:
            index = all_used_sentences.index(s)
            learner_list.append(index + 1)

        # write the vocabulary with the lists to a file
        vocwriter.writerow([v_list, gdex_list, learner_list])

    # write the sentences to a csv file
    # ["_id"] + ["Chapter"] + ["Book"] + ["Page"] + ["Sentence"] + ["Tagged"] + ["Lemma"]
    id = 1
    for s in all_used_sentences:
        tokenized = word_tokenize(s[5])
        # tagged
        tagged = nltk.pos_tag(tokenized)
        # lemma
        lemma = []
        for item in tokenized:
            lemma.append(lemmatizer.lemmatize(item))
        sentwriter.writerow([id, "xxx", "xxx", "x", s[5], tagged, lemma])
        id += 1
