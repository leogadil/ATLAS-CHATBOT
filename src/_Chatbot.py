# RESTAURANT CHATBOT
# Author: Leo Gadil
# 1/15/21

import spacy
import pandas as pd
from io import StringIO
import json, string, random, time
from src._Order import Order
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from src._SkillManager import SKM
from src._Util import Util


class CHATBOT:

    nlp = spacy.load('MODEL')

    last_query = None

    user = None

    def Type(self, str, waittime=0.02, newline=True, stopatpunct=False):
        if str != "":
            print(Util.ReplaceVars("\nBot_name: "), end = '')
            time.sleep(1)
        for letter in str:
            print(letter, end = '',flush=True)
            if letter != "-":
                time.sleep(random.uniform(0.05, 0.03))
            if letter in string.punctuation and stopatpunct and letter != "'" and letter != "-":
                time.sleep(1)

    def __init__(self):
        intro = ""
        chance = random.random()
        if chance > 0.4:
            intro = Util.ReplaceVars(Util.ReplaceTags("$INTRO$"))
        else:
            intro = ""
        self.Type(intro, stopatpunct=True)

        

    def get_data(dataset):
        df = pd.read_csv(dataset)
        return df
    
    def data_prepare(dataset):
        col = ['class', 'question']
        y= CHATBOT.get_data(dataset)
        y = y[col]
        y = y[pd.notnull(y['question'])]
        y.columns = ['class', 'question']
        y['category_id'] = y['class'].factorize()[0]
        category_id_df = y[['class', 'category_id']].drop_duplicates().sort_values('category_id')
        category_to_id = dict(category_id_df.values)
        id_to_category = dict(category_id_df[['category_id', 'class']].values)
        return y

    def naive_algo(dataset):
        tfidf = TfidfVectorizer(sublinear_tf=True, min_df=3, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
        df = CHATBOT.data_prepare(dataset)
        features = tfidf.fit_transform(df.question).toarray()
        labels = df.category_id
        features.shape
        X_train, X_test, y_train, y_test = train_test_split(df['question'], df['class'], random_state = 0)
        count_vect = CountVectorizer()
        X_train_counts = count_vect.fit_transform(X_train)
        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
        clf = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True).fit(X_train_tfidf, y_train)
        
        return clf,count_vect,X_train_tfidf,y_train

    def GetIntent(question, dataset):
        clf,count_vect,X_train_tfidf,y_train= CHATBOT.naive_algo(dataset)
        intent = clf.predict(count_vect.transform([question]))
        # intent = str(intent).strip("['']")
        return intent
    
    def GetEntities(str):
        doc = CHATBOT.nlp(str)
        return [(ent.text, ent.label_) for ent in doc.ents]
        

    @staticmethod
    def GetReply(str):
        if CHATBOT.user is None:
            CHATBOT.user = Order()

        raw_context = ""
        reply = ""
        isAQuestion = False

        str = "".join(l for l in str if l not in string.punctuation).lower()

        if CHATBOT.last_query is not None:
            if CHATBOT.last_query['context'] is not None:
                isAQuestion = True

        if isAQuestion:
            Intention = CHATBOT.GetIntent(str, 'Datasets/YesNo_intent.csv')
            CHATBOT.last_query['context'] = None
        else:
            Intention = CHATBOT.GetIntent(str, 'Datasets/intent_dataset.csv')

        Entities = CHATBOT.GetEntities(str)

        data = {
            "user": CHATBOT.user,
            "input": {
                "query": str,
                "intent": Intention[0],
                "entities": Entities,
            },
            "end": False,
            "context": CHATBOT.last_query['context'] if CHATBOT.last_query else None,
            "work": None,
            "output": {
                "stopatpunct": True,
                "fast": False,
                "reply_template": "$EMPTY$",
                "reply": ""
            }
        }

        SkillResponse = SKM.findSkill(data)


        if SkillResponse == 'None':
            SkillResponse = data

        reply = Util.ReplaceVars(Util.ReplaceTags(SkillResponse['output']['reply_template']))

        for word in reply.split():
            if word.startswith('#') and word.endswith('#'):
                context = word.replace('#', '')
                SkillResponse['context'] = {
                    "intent": context
                }
                raw_context = word

        SkillResponse['output']['reply'] = reply.replace(raw_context, '')
        CHATBOT.last_query = data

        return data

















