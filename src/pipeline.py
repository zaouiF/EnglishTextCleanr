import re
import string
from collections import Counter
import os
import unicodedata
from spellchecker import SpellChecker



spell = SpellChecker()

def correct_spellings(line):
    corrected_text = []
    misspelled_words = spell.unknown(line.split())
    for word in line.split():
        if word in misspelled_words:
            corrected_text.append(spell.correction(word))
        else:
            corrected_text.append(word)
    return " ".join(corrected_text)

def acronyms_correct(line):
        """
            Other manual text cleaning techniques
        """
        # Typos, slang and other
        sample_typos_slang = {
                                "w/e": "whatever",
                                "usagov": "usa government",
                                "recentlu": "recently",
                                "ph0tos": "photos",
                                "amirite": "am i right",
                                "exp0sed": "exposed",
                                "<3": "love",
                                "luv": "love",
                                "amageddon": "armageddon",
                                "trfc": "traffic",
                                "16yr": "16 year"
                                }

       
        # Acronyms
        sample_acronyms =  { 
                            "mh370": "malaysia airlines flight 370",
                            "okwx": "oklahoma city weather",
                            "arwx": "arkansas weather",    
                            "gawx": "georgia weather",  
                            "scwx": "south carolina weather",  
                            "cawx": "california weather",
                            "tnwx": "tennessee weather",
                            "azwx": "arizona weather",  
                            "alwx": "alabama weather",
                            "usnwsgov": "united states national weather service",
                            "2mw": "tomorrow"
                            }

        
        # Some common abbreviations 
        sample_abbr = {
                        "$" : " dollar ",
                        "€" : " euro ",
                        "4ao" : "for adults only",
                        "a.m" : "before midday",
                        "lov" : "love",
                        "a3" : "anytime anywhere anyplace",
                        "aamof" : "as a matter of fact",
                        "acct" : "account",
                        "adih" : "another day in hell",
                        "afaic" : "as far as i am concerned",
                        "afaict" : "as far as i can tell",
                        "afaik" : "as far as i know",
                        "afair" : "as far as i remember",
                        "afk" : "away from keyboard",
                        "app" : "application",
                        "approx" : "approximately",
                        "apps" : "applications",
                        "asap" : "as soon as possible",
                        "asl" : "age, sex, location",
                        "atk" : "at the keyboard",
                        "ave." : "avenue",
                        "aymm" : "are you my mother",
                        "ayor" : "at your own risk", 
                        "b&b" : "bed and breakfast",
                        "b+b" : "bed and breakfast",
                        "b.c" : "before christ",
                        "b2b" : "business to business",
                        "b2c" : "business to customer",
                        "b4" : "before",
                        "b4n" : "bye for now",
                        "b@u" : "back at you",
                        "bae" : "before anyone else",
                        "bak" : "back at keyboard",
                        "bbbg" : "bye bye be good",
                        "bbc" : "british broadcasting corporation",
                        "bbias" : "be back in a second",
                        "bbl" : "be back later",
                        "bbs" : "be back soon",
                        "be4" : "before",
                        "bfn" : "bye for now",
                        "blvd" : "boulevard",
                        "bout" : "about",
                        "brb" : "be right back",
                        "bros" : "brothers",
                        "brt" : "be right there",
                        "bsaaw" : "big smile and a wink",
                        "btw" : "by the way",
                        "bwl" : "bursting with laughter",
                        "c/o" : "care of",
                        "cet" : "central european time",
                        "cf" : "compare",
                        "cia" : "central intelligence agency",
                        "csl" : "can not stop laughing",
                        "cu" : "see you",
                        "cul8r" : "see you later",
                        "cv" : "curriculum vitae",
                        "cwot" : "complete waste of time",
                        "cya" : "see you",
                        "cyt" : "see you tomorrow",
                        "dae" : "does anyone else",
                        "dbmib" : "do not bother me i am busy",
                        "diy" : "do it yourself",
                        "dm" : "direct message",
                        "dwh" : "during work hours",
                        "e123" : "easy as one two three",
                        "eet" : "eastern european time",
                        "eg" : "example",
                        "embm" : "early morning business meeting",
                        "encl" : "enclosed",
                        "encl." : "enclosed",
                        "etc" : "and so on",
                        "faq" : "frequently asked questions",
                        "fawc" : "for anyone who cares",
                        "fb" : "facebook",
                        "fc" : "fingers crossed",
                        "fig" : "figure",
                        "fimh" : "forever in my heart", 
                        "ft." : "feet",
                        "ft" : "featuring",
                        "ftl" : "for the loss",
                        "ftw" : "for the win",
                        "fwiw" : "for what it is worth",
                        "fyi" : "for your information",
                        "g9" : "genius",
                        "gahoy" : "get a hold of yourself",
                        "gal" : "get a life",
                        "gcse" : "general certificate of secondary education",
                        "gfn" : "gone for now",
                        "gg" : "good game",
                        "gl" : "good luck",
                        "glhf" : "good luck have fun",
                        "gmt" : "greenwich mean time",
                        "gmta" : "great minds think alike",
                        "gn" : "good night",
                        "g.o.a.t" : "greatest of all time",
                        "goat" : "greatest of all time",
                        "goi" : "get over it",
                        "gps" : "global positioning system",
                        "gr8" : "great",
                        "gratz" : "congratulations",
                        "gyal" : "girl",
                        "h&c" : "hot and cold",
                        "hp" : "horsepower",
                        "hr" : "hour",
                        "hrh" : "his royal highness",
                        "ht" : "height",
                        "ibrb" : "i will be right back",
                        "ic" : "i see",
                        "icq" : "i seek you",
                        "icymi" : "in case you missed it",
                        "idc" : "i do not care",
                        "idgadf" : "i do not give a damn fuck",
                        "idgaf" : "i do not give a fuck",
                        "idk" : "i do not know",
                        "ie" : "that is",
                        "i.e" : "that is",
                        "ifyp" : "i feel your pain",
                        "IG" : "instagram",
                        "iirc" : "if i remember correctly",
                        "ilu" : "i love you",
                        "ily" : "i love you",
                        "imho" : "in my humble opinion",
                        "imo" : "in my opinion",
                        "imu" : "i miss you",
                        "iow" : "in other words",
                        "irl" : "in real life",
                        "j4f" : "just for fun",
                        "jic" : "just in case",
                        "jk" : "just kidding",
                        "jsyk" : "just so you know",
                        "l8r" : "later",
                        "lb" : "pound",
                        "lbs" : "pounds",
                        "ldr" : "long distance relationship",
                        "lmao" : "laugh my ass off",
                        "lmfao" : "laugh my fucking ass off",
                        "lol" : "laughing out loud",
                        "ltd" : "limited",
                        "ltns" : "long time no see",
                        "m8" : "mate",
                        "mf" : "motherfucker",
                        "mfs" : "motherfuckers",
                        "mfw" : "my face when",
                        "mofo" : "motherfucker",
                        "mph" : "miles per hour",
                        "mr" : "mister",
                        "mrw" : "my reaction when",
                        "ms" : "miss",
                        "mte" : "my thoughts exactly",
                        "nagi" : "not a good idea",
                        "nbc" : "national broadcasting company",
                        "nbd" : "not big deal",
                        "nfs" : "not for sale",
                        "ngl" : "not going to lie",
                        "nhs" : "national health service",
                        "nrn" : "no reply necessary",
                        "nsfl" : "not safe for life",
                        "nsfw" : "not safe for work",
                        "nth" : "nice to have",
                        "nvr" : "never",
                        "nyc" : "new york city",
                        "oc" : "original content",
                        "og" : "original",
                        "ohp" : "overhead projector",
                        "oic" : "oh i see",
                        "omdb" : "over my dead body",
                        "omg" : "oh my god",
                        "omw" : "on my way",
                        "p.a" : "per annum",
                        "p.m" : "after midday",
                        "pm" : "prime minister",
                        "poc" : "people of color",
                        "pov" : "point of view",
                        "pp" : "pages",
                        "ppl" : "people",
                        "prw" : "parents are watching",
                        "ps" : "postscript",
                        "pt" : "point",
                        "ptb" : "please text back",
                        "pto" : "please turn over",
                        "qpsa" : "what happens", #"que pasa",
                        "ratchet" : "rude",
                        "rbtl" : "read between the lines",
                        "rlrt" : "real life retweet", 
                        "rofl" : "rolling on the floor laughing",
                        "roflol" : "rolling on the floor laughing out loud",
                        "rotflmao" : "rolling on the floor laughing my ass off",
                        "rt" : "retweet",
                        "ruok" : "are you ok",
                        "sfw" : "safe for work",
                        "sk8" : "skate",
                        "smh" : "shake my head",
                        "sq" : "square",
                        "srsly" : "seriously", 
                        "ssdd" : "same stuff different day",
                        "tbh" : "to be honest",
                        "tbs" : "tablespooful",
                        "tbsp" : "tablespooful",
                        "tfw" : "that feeling when",
                        "thks" : "thank you",
                        "tho" : "though",
                        "thx" : "thank you",
                        "tia" : "thanks in advance",
                        "til" : "today i learned",
                        "tl;dr" : "too long i did not read",
                        "tldr" : "too long i did not read",
                        "tmb" : "tweet me back",
                        "tntl" : "trying not to laugh",
                        "ttyl" : "talk to you later",
                        "u" : "you",
                        "u2" : "you too",
                        "u4e" : "yours for ever",
                        "utc" : "coordinated universal time",
                        "w/" : "with",
                        "w/o" : "without",
                        "w8" : "wait",
                        "wassup" : "what is up",
                        "wb" : "welcome back",
                        "wtf" : "what the fuck",
                        "wtg" : "way to go",
                        "wtpa" : "where the party at",
                        "wuf" : "where are you from",
                        "wuzup" : "what is up",
                        "wywh" : "wish you were here",
                        "yd" : "yard",
                        "ygtr" : "you got that right",
                        "ynk" : "you never know",
                        "zzz" : "sleeping bored and tired"
                        }
            
        sample_typos_slang_pattern = re.compile(r'(?<!\w)(' + '|'.join(re.escape(key) for key in sample_typos_slang.keys()) + r')(?!\w)')
        sample_acronyms_pattern = re.compile(r'(?<!\w)(' + '|'.join(re.escape(key) for key in sample_acronyms.keys()) + r')(?!\w)')
        sample_abbr_pattern = re.compile(r'(?<!\w)(' + '|'.join(re.escape(key) for key in sample_abbr.keys()) + r')(?!\w)')
        
        line = sample_typos_slang_pattern.sub(lambda x: sample_typos_slang[x.group()], line)
        line = sample_acronyms_pattern.sub(lambda x: sample_acronyms[x.group()], line)
        line = sample_abbr_pattern.sub(lambda x: sample_abbr[x.group()], line)   
def remove_URL(line):
    url = r'https?://\S+|www\.\S+'
    without_urls = re.sub(pattern= url, repl= '', string= line)
    return without_urls

def remove_html(line):
    html=re.compile(r'<.*?>')
    return html.sub(r'', line)

def remove_numbers(line):
    line = ''.join([i for i in line if not i.isdigit()])
    return line

def num_to_words(line):
    # splitting text into words with space
    after_spliting = line.split()
    for index in range(len(after_spliting)):
        if after_spliting[index].isdigit():
            after_spliting[index] = num2words(after_spliting[index])
    # joining list into string with space
    numbers_to_words = ' '.join(after_spliting)
    return numbers_to_words

def remove_duplicated_letter(line):

    result = []
    for w in line.split(' '):
        try:
            count = Counter(w).most_common()[0][1]
            if count > 2:
                result.append(re.sub(r'(\w)\1+', r'\1\1', w))
            else:
                result.append(w)
        except:
            result.append(w)

    return ' '.join(result)


def remove_white_spaces(line):
    return " ".join(line.split())


def emoji_translate(line):
    # Defining dictionary containing all emojis with their meanings.
    emojis = {':)': 'smile', ':-)': 'smile', ';d': 'wink', ':-E': 'vampire', ':(': 'sad',
              ':-(': 'sad', ':-<': 'sad', ':P': 'raspberry', ':O': 'surprised',
              ':-@': 'shocked', ':@': 'shocked', ':-$': 'confused', ':\\': 'annoyed',
              ':#': 'mute', ':X': 'mute', ':^)': 'smile', ':-&': 'confused', '$_$': 'greedy',
              '@@': 'eyeroll', ':-!': 'confused', ':-D': 'smile', ':-0': 'yell', 'O.o': 'confused',
              '<(-_-)>': 'robot', 'd[-_-]b': 'dj', ":'-)": 'sadsmile', ';)': 'wink',
              ';-)': 'wink', 'O:-)': 'angel', 'O*-)': 'angel', '(:-D': 'gossip', '=^.^=': 'cat'}
    for emoji in emojis.keys():
        line = line.replace(emoji, emojis[emoji])
    return line

def remove_accents(line):
    """Removes common accent characters.
    """

    line = re.sub(u"[àáâãäå]", 'a', line)
    line = re.sub(u"[èéêë]", 'e', line)
    line = re.sub(u"[ìíîï]", 'i', line)
    line = re.sub(u"[òóôõö]", 'o', line)
    line = re.sub(u"[ùúûü]", 'u', line)
    line = re.sub(u"[ýÿ]", 'y', line)
    line = re.sub(u"[ß]", 'ss', line)
    line = re.sub(u"[ñ]", 'n', line)
    line = re.sub(u"[ç]", 'c', line)
    return line
def remove_users(line):
    '''Takes a string and removes retweet and @user information'''
    line = re.sub('(RTs@[A-Za-z]+[A-Za-z0-9-_]+) ', '', line) # remove retweet
    line = re.sub('(rts@[A-Za-z]+[A-Za-z0-9-_]+) ', '', line) # remove retweet
    line = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+) ', '', line) # remove tweeted at
    line = re.sub('(@_[A-Za-z]+[A-Za-z0-9-_]+) ', '', line) # remove tweeted at
    return line

def remove_non_alphanum(line):
    return " ".join(re.compile(r'\W+', re.UNICODE).split(line))



def clean_text(
    text,
    users=True,
    whitespace=True,
    correct_spelling=True,
    accronyms=True,
    url=True,
    html=True,
    number=True,
    translate_number=False,
    translate_emoji=True,
    remove_emoji=False,
    punctuation=True,
    duplicated=True,
    alphnum=True,
    accent=True,
    do_lower=True,
    ascii=False,
    others=[('ə', 'a')]
):

    arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
    english_punctuations = string.punctuation
    arabic = False

    if do_lower:
        text = text.lower()

    if correct_spelling:
        text = correct_spellings(text)

    if accronyms:
        text = acronyms_correct(text)

    if users:
        text = remove_users(text)

    if url:
        text = remove_URL(text)

    if html:
        text = remove_html(text)

    if number:
        text = remove_numbers(text)

    if translate_number:
        text = num_to_words(text)

    if translate_emoji:
        text = translate_emoji(text)

    if punctuation:

        punctuations_list = arabic_punctuations + english_punctuations

        translator = str.maketrans('', '', punctuations_list)
        text = text.translate(translator)

    if whitespace:
        text = remove_white_spaces(text)

    if duplicated:
        text = remove_duplicated_letter(text)

    if accent:
        text = remove_accents(text)

    if alphnum:
        text = remove_non_alphanum(text)

    if ascii:
        text = unicode_to_ascii(text)

    if others is not None:
        for rule in others:
            text = text.replace(rule[0], rule[1])

    return text


def wc(path, unique=False, both=False):

    file = open(path, mode='r', encoding='utf8')
    data = file.readlines()
    file.close()
    count = 0

    if both:
        clean_data = []
        for x in data:
            x = clean_text(x)
            clean_data.append(x)
            count += len(x.split())

        data = set(clean_data)
        data = [str(x) for x in data]
        return count, len(data)

    if unique:
        clean_data = []
        for x in data:
            x = clean_text(x)
            clean_data.append(x)

        data = set(clean_data)
        data = [str(x) for x in data]
        return len(data)

    for x in data:
        x = clean_text(x)
        count += len(x.split())

    return count


def word_frequency(path, top=100):
    file = open(path, mode='r', encoding='utf8')
    data = file.readlines()
    file.close()

    r = []
    for x in data:
        for y in x.split(' '):
            r.append(y)

    c = Counter(r)
    return c.most_common()[:top]


def unique_chars(path_or_list):
    data = []
    if isinstance(path_or_list, list):
        data = path_or_list
    elif os.path.isfile(path_or_list):
        file = open(path_or_list, mode='r', encoding='utf8')
        data = file.readlines()
        file.close()
    else:
        raise Exception('is not path or list please check your path_or_list')

    chars = set()
    for lines in data:
        for words in lines.split(' '):
            for char in words:
                if char not in chars:
                    chars.add(char)
    chars = sorted(chars)
    return chars


def unicode_to_ascii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )