import vincent


import operator 
import json
from text_preprocessing import preprocess
from collections import Counter
from nltk.corpus import stopwords
from nltk import bigrams 
import pandas

import string
 
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']
 
dates_python,dates_datascience,dates_java,dates_programming = [],[],[],[]
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
        if '#python' in terms_hash:
        	dates_python.append(tweet['created_at'])
        if '#datascience' in terms_hash:
        	dates_datascience.append(tweet['created_at'])
    	if '#java' in terms_hash:
    		dates_java.append(tweet['created_at'])
    	if '#programming' in terms_hash:
    		dates_programming.append(tweet['created_at'])

        terms_only = [term for term in preprocess(tweet['text']) if term not in stop and not term.startswith(('#', '@'))] 
        terms_bigram = bigrams(terms_stop)
        

        count_all.update(terms_stop)
        count_terms.update(terms_only)
        count_hash.update(terms_hash)
        count_single.update(terms_single)
        count_bigram.update(terms_bigram)
    # Print the first 5 most frequent words
    # count_all.most_common(5)
    # print(count_single.most_common(5))
    # print(count_hash.most_common(5))
    word_freq = count_terms.most_common(20)
    
    # a list of "1" to count the hashtags
    ones = [1]*len(dates_python)
    # the index of the series
    idx = pandas.DatetimeIndex(dates_python)
    # the actual series (at series of 1s for the moment)
    pythons = pandas.Series(ones, index=idx)
    # Resampling / bucketing
    per_minute_p = pythons.resample('1Min', how='sum').fillna(0)


    # a list of "1" to count the hashtags
    ones = [1]*len(dates_datascience)
    # the index of the series
    idx = pandas.DatetimeIndex(dates_datascience)
    # the actual series (at series of 1s for the moment)
    datascience = pandas.Series(ones, index=idx)
    # Resampling / bucketing
    per_minute_d = datascience.resample('1Min', how='sum').fillna(0)


    # a list of "1" to count the hashtags
    ones = [1]*len(dates_java)
    # the index of the series
    idx = pandas.DatetimeIndex(dates_java)
    # the actual series (at series of 1s for the moment)
    java = pandas.Series(ones, index=idx)
    # Resampling / bucketing
    per_minute_j = java.resample('1Min', how='sum').fillna(0)

    # a list of "1" to count the hashtags
    ones = [1]*len(dates_programming)
    # the index of the series
    idx = pandas.DatetimeIndex(dates_programming)
    # the actual series (at series of 1s for the moment)
    programming = pandas.Series(ones, index=idx)
    # Resampling / bucketing
    per_minute_pr = programming.resample('1Min', how='sum').fillna(0)


    # all the data together
    hashtags_data= dict(pythons=per_minute_p,datascience=per_minute_d,java=per_minute_j,programming=per_minute_pr)
    # we need a DataFrame, to accommodate multiple series
    all_tages = pandas.DataFrame(data=hashtags_data,index=per_minute_p.index)
    # Resampling as above
    all_tages = all_tages.resample('1Min', how='sum').fillna(0)
 


# labels, freq = zip(*word_freq)
# data = {'data': freq, 'x': labels}
# bar = vincent.Bar(data, iter_idx='x')
# bar.to_json('term_freq.json')

 


# time_chart = vincent.Line(per_minute)
time_chart = vincent.Line(all_tages[['pythons', 'datascience', 'java','programming']])
time_chart.axis_titles(x='Time', y='Freq')
time_chart.legend(title='hashtags')
time_chart.to_json('time_chart.json')
