import operator 
import json
from text_preprocessing import preprocess
from collections import Counter
from nltk.corpus import stopwords
from nltk import bigrams 

import string
 
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']
 
fname = 'python.json'
with open(fname, 'r') as f:
    count_all = Counter()
    count_single = Counter()
    count_hash = Counter()
    count_terms = Counter()
    count_bigram = Counter()
    for line in f:
        tweet = json.loads(line)
        # Create a list with all the terms
        terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]# Update the counter
        # Count terms only once, equivalent to Document Frequency
        terms_single = set(terms_stop)
        # Count hashtags only
        terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#')] # Count terms only (no hashtags, no mentions)
        terms_only = [term for term in preprocess(tweet['text']) if term not in stop and not term.startswith(('#', '@'))] 
        terms_bigram = bigrams(terms_stop)
        

        count_all.update(terms_stop)
        count_terms.update(terms_only)
        count_hash.update(terms_hash)
        count_single.update(terms_single)
        count_bigram.update(terms_bigram)
    # Print the first 5 most frequent words
    print(count_all.most_common(5))
    print(count_single.most_common(5))
    print(count_hash.most_common(5))
    print(count_terms.most_common(5))
    print(count_bigram.most_common(5))