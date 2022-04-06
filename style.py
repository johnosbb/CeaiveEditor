from statistics import mean
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import cmudict
from nltk.corpus import stopwords
import nltk
import logging


nltk.download('cmudict')
nltk.download('stopwords')

cmuDictionary = None

# ---------------------------------------------------------------------


def syllable_count_Manual(word):
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
            if word.endswith("e"):
                count -= 1
    if count == 0:
        count += 1
    return count


# ---------------------------------------------------------------------
# COUNTS NUMBER OF SYLLABLES

def syllable_count(word):
    global cmuDictionary
    d = cmuDictionary
    try:
        syl = [len(list(y for y in x if y[-1].isdigit()))
               for x in d[word.lower()]][0]
    except:
        syl = syllable_count_Manual(word)
    return syl

    # ----------------------------------------------------------------------------


def calculate_average_syllables_per_word(text):
    # step size must not be greater than winsize
    chunks = create_sliding_window(text, 4, 4)
    totalSyllables = 0
    for chunk in chunks:
        meanSyllable = avg_syllable_per_Word(chunk)
        totalSyllables += meanSyllable
    return totalSyllables/len(chunks)


def calculate_functional_word_count(text):
    # step size must not be greater than winsize
    chunks = create_sliding_window(text, 4, 4)
    totalFunctionalWords = 0
    for chunk in chunks:
        meanFunctionalWords = count_functional_words(chunk)
        totalFunctionalWords += meanFunctionalWords
    return totalFunctionalWords/len(chunks)


# GIVES NUMBER OF SYLLABLES PER WORD
# Return an integer sum of the average syllable count for the text
def avg_syllable_per_Word(text):

    tokens = word_tokenize(text, language='english')
    punctuation = [",", ".", "'", "!", '"', "#", "$", "%", "&", "(", ")", "*", "+", "-", ".", "/", ":", ";", "<", "=", '>', "?",
                   "@", "[", "\\", "]", "^", "_", '`', "{", "|", "}", '~', '\t', '\n']
    # A stop word is a commonly used word (such as “the”, “a”, “an”, “in”) that we may wish to ignore when processing language.
    # NLTK(Natural Language Toolkit) in python has a list of stopwords stored in 16 different languages.
    # We can use these tables to eliminate these stop words and other punctuation when processing text for syllable count purposes.
    # our stop words and other symbols and punctuation
    stop = stopwords.words('english') + punctuation
    words = [word for word in tokens if word not in stop]
    syllabls = [syllable_count(word) for word in words]
    p = (" ".join(words))
    return sum(syllabls) / max(1, len(words))


# ------------------------------------------------------------------------
def RemoveSpecialCHs(text):
    text = word_tokenize(text)
    st = [",", ".", "'", "!", '"', "#", "$", "%", "&", "(", ")", "*", "+", "-", ".", "/", ":", ";", "<", "=", '>', "?",
          "@", "[", "\\", "]", "^", "_", '`', "{", "|", "}", '~', '\t', '\n']

    words = [word for word in text if word not in st]
    return words

# takes a paragraph of text and divides it into chunks of specified number of sentences
# sequence is the input text to chunk
# winSize is the number of sentences to process in a chunk
# Step determines the over lap of those sentences, if we have a winsize of 4 and a step of 2, then the second chunk will start with sentence 2
# If we have a winsize of 4 and a step size of 4, then each chunk has 4 sentences with no overlap.


def create_sliding_window(sequence, winSize, step=1):

    try:
        it = iter(sequence)
    except TypeError:
        raise Exception("**ERROR** sequence must be iterable.")
    if not ((type(winSize) == type(0)) and (type(step) == type(0))):
        raise Exception("**ERROR** type(winSize) and type(step) must be int.")
    if step > winSize:
        raise Exception("**ERROR** step must not be larger than winSize.")
    if winSize > len(sequence):
        raise Exception(
            "**ERROR** winSize must not be larger than sequence length.")

    # sent_tokenize will split text into sentences based on the presence of certain characters like "!”  “.” and “?”.
    sequence = sent_tokenize(sequence)
    sequence_length = len(sequence)  # the number of sentences
    # Pre-compute number of chunks to omit
    numOfChunks = int(((sequence_length - winSize) / step) + 1)
    if numOfChunks == 0:
        numOfChunks = 1
    l = []
    # Do the work
    for i in range(0, numOfChunks * step, step):
        l.append(" ".join(sequence[i:i + winSize]))
    logging.debug("Created Sliding Window - sequence length: %d, number of chunks: %d, window size: %d, step size: %d",
                  sequence_length, numOfChunks, winSize, step)
    return l


# ----------------------------------------------------------------------------
# Normalised count of functional words
# See: https://www.pages.drexel.edu/~jl622/docs/Jounals/Zheng_2006JASIST_AuthorshipIdentification.pdf

def count_functional_words(text):
    functional_words = """a between in nor some upon
    about both including nothing somebody us
    above but inside of someone used
    after by into off something via
    all can is on such we
    although cos it once than what
    am do its one that whatever
    among down latter onto the when
    an each less opposite their where
    and either like or them whether
    another enough little our these which
    any every lots outside they while
    anybody everybody many over this who
    anyone everyone me own those whoever
    anything everything more past though whom
    are few most per through whose
    around following much plenty till will
    as for must plus to with
    at from my regarding toward within
    be have near same towards without
    because he need several under worth
    before her neither she unless would
    behind him no should unlike yes
    below i nobody since until you
    beside if none so up your
    """

    functional_words = functional_words.split()
    words = RemoveSpecialCHs(text)
    count = 0

    for i in text:
        if i in functional_words:
            count += 1

    return count / len(words)
