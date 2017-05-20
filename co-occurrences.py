import operator 
import json
from text_preprocessing import preprocess
from collections import Counter
from nltk.corpus import stopwords
from nltk import bigrams,ngrams 
from collections import defaultdict
import string
import sys
 
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']

search_word = sys.argv[1] # pass a term as a command-line argument
 
fname = 'python.json'
com = defaultdict(lambda : defaultdict(int))
with open(fname, 'r') as f:
    count_all = Counter()
    count_single = Counter()
    count_hash = Counter()
    count_terms = Counter()
    count_bigram = Counter()
    count_search = Counter()

    for line in f:
        tweet = json.loads(line)
        # Create a list with all the terms
        terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]# Update the counter
        # Count terms only once, equivalent to Document Frequency
        terms_single = set(terms_stop)
        # Count hashtags only
        terms_hash = [term for term in preprocess(tweet['text'],lowercase=True) if term.startswith('#')] # Count terms only (no hashtags, no mentions)
        terms_only = [term for term in preprocess(tweet['text']) if term not in stop and not term.startswith(('#', '@'))] 
        terms_bigram = bigrams(terms_only)
        
        for i in range(len(terms_only)-1):            
            for j in range(i+1, len(terms_only)):
                w1, w2 = sorted([terms_only[i], terms_only[j]])                
                if w1 != w2:
                    com[w1][w2] += 1

        count_all.update(terms_stop)
        count_terms.update(terms_only)
        count_hash.update(terms_hash)
        count_single.update(terms_single)
        count_bigram.update(terms_bigram)

        if search_word in terms_only:
            count_search.update(terms_only)

    com_max = []
    # For each term, look for the most common co-occurrent terms
    for t1 in com:
        t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
        for t2, t2_count in t1_max_terms:
            com_max.append(((t1, t2), t2_count))
    # Get the most frequent co-occurrences
    terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
    # print(terms_max[:5])
    #Print the first 5 most frequent words
    print("ALL words:")
    print(count_all.most_common(5))
    print ("_______________________________")
    print("single words:")
    print(count_single.most_common(5))
    print ("_______________________________")
    print("Hash words:")
    print(count_hash.most_common(5))
    print ("_______________________________")
    print("Terms only:")
    print(count_terms.most_common(5))
    print ("_______________________________")
    print("bigrams:")
    print(count_bigram.most_common(5))
    print ("_______________________________")
    print("Co-occurrence for %s:" % search_word)
    print(count_search.most_common(20))




    
