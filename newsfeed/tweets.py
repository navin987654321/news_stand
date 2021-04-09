import twint
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from gensim import corpora
from gensim import models
import re
def search(query=None):
    c = twint.Config()
    c.Search = "" if query is None else query
    c.Limit = 2000
    c.Lang = 'en'
    c.Pandas = True
    c.Hide_output = True

    twint.run.Search(c)
    data = {
        "tweets": twint.output.panda.Tweets_df[['id', 'username', 'photos', 'tweet', 'date', 'link']],
        "topics": [],
    }
    data["tweets"]["cleaned_tweet"] = data["tweets"]["tweet"].apply(lambda x:process_text(x))
    topicList = [x.split() for x in data["tweets"]['cleaned_tweet'].tolist()]
    dictionary = corpora.Dictionary(topicList)
    corpus = [dictionary.doc2bow(topic) for topic in topicList]
    model = models.ldamodel.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=10)
    topics = model.print_topics(num_words=5)
    data["tweets"] = data["tweets"].to_dict(orient='index').values()
    for topic in topics:
        data["topics"].append(process_text(topic[1]))
    return data

def process_text(text):
    text = re.sub(r"http\S+", "", text) #Removing URLs
    text = re.sub(r"\S+\.com\S+", "", text) #Removing URLs
    text = re.sub(r"\@\w+", "", text) #Removing mentions
    text = re.sub(r"\#\w+", "", text) #Removing hashtags
    text = re.sub("[^A-Za-z]", " ", text.lower()) #Removing non-alphabets
    tokenized_text = word_tokenize(text)
    stop_words = stopwords.words('english')
    clean_text = [word for word in tokenized_text if word not in stop_words]
    text = " ".join(clean_text)
    return text