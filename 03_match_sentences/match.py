import csv
import ast

no_plural = ['(', 'no', 'pl', ')']
plural = ['(', 'pl', ')']
irregular = ['(', 'irr', ')']
informal = ['(', 'informal', ')']


def trim_vocabulary(voc_list):
    voc_list2 = None
    second_voc_list = False

    # ignore the verb marker 'to' in the beginning
    if voc_list[0] == 'to' and len(voc_list) > 1:
        voc_list = voc_list[1:len(voc_list)]

    # ignore 'no plural' markers
    if set(no_plural) < set(voc_list):
        voc_list = [x for x in voc_list if x not in no_plural]

    # ignore plural markers
    if set(plural) < set(voc_list):
        voc_list = [x for x in voc_list if x not in plural]

    # ignore irregular markers
    if set(irregular) < set(voc_list):
        voc_list = [x for x in voc_list if x not in irregular]

    # ignore informal markers
    if set(informal) < set(voc_list):
        voc_list = [x for x in voc_list if x not in informal]

    # split in short and longer form
    if set(['(', '=']) < set(voc_list):
        voc_list2 = voc_list[voc_list.index('(') + 2:len(voc_list) - 1]
        voc_list = voc_list[0:voc_list.index('(')]
        second_voc_list = True

    # ignore additional information (after/between voc)
    if '(' in voc_list and '(' != voc_list[0]:
        voc_list = voc_list[0:voc_list.index('(')] + voc_list[voc_list.index(')') + 1:]

    # ignore additional information (before the voc)
    if '(' in voc_list and '(' == voc_list[0]:
        voc_list = voc_list[voc_list.index(')') + 1:]

    # ignore all small dots
    if '…' in voc_list:
        voc_list = list(filter(lambda a: a != '…', voc_list))

    # ignore all normal dots
    if '...' in voc_list:
        voc_list = list(filter(lambda a: a != '...', voc_list))

    # split the voc
    if '/' in voc_list:
        voc_list2 = voc_list[voc_list.index('/') + 1:]
        voc_list = voc_list[:voc_list.index('/')]
        second_voc_list = True

    # split the voc
    if any("/" in s for s in voc_list):     # split the voc
        word_index = [voc for voc, strng in enumerate(voc_list) if '/' in strng]
        word = voc_list[word_index[0]].split('/')
        if word[0] == '':
            voc_list2 = [word[1]]
            voc_list = voc_list[:word_index[0]]
        else:
            voc_list2 = voc_list[:word_index[0]] + [word[1]] + voc_list[word_index[0] + 1:]
            voc_list = voc_list[:word_index[0]] + [word[0]] + voc_list[word_index[0] + 1:]
        second_voc_list = True

    # todo evtl ignoriere Satzzeichen

    # todo evtl ignoriere 'be' am Anfang

    return voc_list, voc_list2, second_voc_list

with open("../02_tokenize/sentences_all_test_map.csv", 'r') as sentin, open('../02_tokenize/new_Vokabelliste.csv', 'r') as vocin:
    with open('map_test_matched_' + "vocabulary.csv", 'w') as vocout, open("test_not_matched.csv", 'w') as nmatched:

        sentreader = csv.reader(sentin, delimiter=';')
        vocreader = csv.reader(vocin, delimiter=';')
        vocwriter = csv.writer(vocout, delimiter=';')
        no_matched = csv.writer(nmatched, delimiter=';')
        # TODO change here
        #vocwriter.writerow(next(vocreader) + ["SentId"] + ["0"])
        sth = next(vocreader) # delete
        vocwriter.writerow([sth[0]] + [sth[1]] + ["VocLemma"] + sth[2:] + ["SentId"] + ["Tested"]) # delete
        next(sentreader)

        voc_matched = 0

        for v_row in vocreader:
            v_list = v_row[10]  # Lemma
            v_list = ast.literal_eval(v_list)
            index_list = []
            if len(v_list) == 0:
                continue

            v_list1, v_list2, second_list = trim_vocabulary(v_list)

            # start matching to sentences

            for s_row in sentreader:
                s_list = s_row[6]  # Lemma
                s_list = ast.literal_eval(s_list)

                if second_list:
                    #print(v_list1, v_list2)
                    if set(v_list1) < set(s_list) or set(v_list2) < set(s_list):
                        # delete the exercise number if present so that it matches the sentences
                        if len(v_row[4]) == 4:
                            chapter = v_row[4][: len(v_row[4]) - 1]
                        else:
                            chapter = v_row[4]
                        # match book and chapter
                        if v_row[5] == s_row[2] and chapter == s_row[1]:
                            index_list.append(s_row[0])
                else:
                    if set(v_list1) < set(s_list):
                        # delete the exercise number if present so that it matches the sentences
                        if len(v_row[4]) == 4:
                            chapter = v_row[4][: len(v_row[4]) - 1]
                        else:
                            chapter = v_row[4]
                        # match book and chapter
                        if v_row[5] == s_row[2] and chapter == s_row[1]:
                            index_list.append(s_row[0])

            sentin.seek(0)
            next(sentreader)
            if len(index_list) > 0:
                #print(v_row[1], "\t\t", v_row[5], v_row[4], index_list)
                voc_matched += 1
                # TODO
                #vocwriter.writerow(v_row + [index_list] + ["0"])
                if (second_list):
                    vocwriter.writerow([v_row[0]] + [v_row[1]] + [[v_list1] + [v_list2]] + v_row[2:] + [index_list] + ["0"])
                else:
                    vocwriter.writerow([v_row[0]] + [v_row[1]] + [v_list1] + v_row[2:] + [index_list] + ["0"])
            else:
                # TODO
                #vocwriter.writerow(v_row + ["None"] + ["0"])
                if (second_list):
                    vocwriter.writerow([v_row[0]] + [v_row[1]] + [[v_list1] + [v_list2]] + v_row[2:] + ["None"] + ["0"])
                else:
                    vocwriter.writerow([v_row[0]] + [v_row[1]] + [v_list1] + v_row[2:] + ["None"] + ["0"])
                # print(v_row[1], v_list)
                no_matched.writerow([v_row[4], v_row[5], v_row[1], v_list1])
                # for x in (voc for voc in s_list if voc not in string.punctuation):
                #    print(x)


print(voc_matched)

sentin.close()
vocin.close()
vocout.close()
nmatched.close()
