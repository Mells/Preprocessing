import nltk
from nltk import word_tokenize


points = 100

# Sentence length: a sentence between 10 and 25 words long was preferred, with longer and shorter ones penalized.
def sentence_length(sentence, points):
    sentLength = len(nltk.word_tokenize(sentence))
    if sentLength >= 10 and sentLength <= 25:
        pass
    else:
        # todo penalize
        if sentLength < 10:
            points -= (10-sentLength)

    return points

# Word frequencies: a sentence was penalized for each word that was not amongst the commonest 17,000 words in the
# language, with a further penalty applied for rare words.

# Sentences containing pronouns and anaphors like this that it or one often fail to present a self-contained piece of
# language which makes sense without further context, so sentences containing these words were penalized.
def contain_pronouns_anaphors(sentence, points):
    tokenized = word_tokenize(sentence)
    tagged = nltk.pos_tag(tokenized)
    if ["PRP", "PRP$"] in tagged:
        points -= tagged.count("PRP")
        points -= tagged.count("PRP$")

    return points

# Sentences where the target collocation is in the main clause were preferred (using heuristics to guess where the
# main clause begins and ends, as we do not yet use a parser).

# Whole sentenceidentified as beginning with a capital letter and ending with a full step, exclamation mark, or
# question mark, were preferred.
def whole_sentence(sentence, points):
    punctuation = ["!", "\"", ".", "?"]
    if sentence[0].isupper():
        if sentence[len(sentence)] in punctuation:
            pass
        else:
            points -= 10
    else:
        if sentence[len(sentence)] in punctuation:
            points -= 10
        else:
            points -= 20

    return points

# Sentences with third collocates, that is, words that occurred with high salience in sentences containing the
# node and primary collocate, were preferred.

# We note that good examples often first introduce a context, and then contain the collocation which, to speak
# figuratively, fits into the space that the context has created for it: this is helpful as a user who is unsure of
# the meaning of the collocation will be able to make inferences about what it must be from the context in which it
# appears. In sentences having this structure, the collocation is likely to be towards the end of the sentence.
# Sentences with the target collocation towards the end were given credit.