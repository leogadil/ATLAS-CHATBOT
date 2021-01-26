import spacy
import pandas as pd
import sys, traceback
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from datetime import datetime
from src._Util import Util

class Gquestion():

    def get_data(dataset):
        df = pd.read_csv(dataset)
        return df
    
    def data_prepare(dataset):
        col = ['class', 'question']
        y= Gquestion.get_data(dataset)
        y = y[col]
        y = y[pd.notnull(y['question'])]
        y.columns = ['class', 'question']
        y['category_id'] = y['class'].factorize()[0]
        category_id_df = y[['class', 'category_id']].drop_duplicates().sort_values('category_id')
        category_to_id = dict(category_id_df.values)
        id_to_category = dict(category_id_df[['category_id', 'class']].values)
        return y

    def naive_algo(dataset):
        tfidf = TfidfVectorizer(sublinear_tf=True, min_df=1, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
        df = Gquestion.data_prepare(dataset)
        features = tfidf.fit_transform(df.question).toarray()
        labels = df.category_id
        features.shape
        X_train, X_test, y_train, y_test = train_test_split(df['question'], df['class'], random_state = 0)
        count_vect = CountVectorizer()
        X_train_counts = count_vect.fit_transform(X_train)
        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
        clf = MultinomialNB().fit(X_train_tfidf, y_train)
        return clf,count_vect

    def GetIntent(question, dataset):
        clf,count_vect = Gquestion.naive_algo(dataset)
        intent = clf.predict(count_vect.transform([question]))
        # intent = str(intent).strip("['']")
        return intent

    def getAnswers(intent, data):
        try:
            switcher = {
                'open_hours': lambda: Gquestion.open_hours(data),
                'ask_boss': lambda: Gquestion.ask_boss(data),
                'ask_about_creator': lambda: Gquestion.ask_about_creator(data),
                'ask_time': lambda: Gquestion.ask_time(data),
                'ask_about_me': lambda: Gquestion.ask_about_me(data),
                'ask_about_name': lambda: Gquestion.ask_about_name(data)
            }
            switch_answer = switcher[intent]()
            return data
        except Exception as e:
            print(e)
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            print(traceback_str)
            switch_answer = data
            return switch_answer

    def run(data):
        query = data['input']['query']
        intent = Gquestion.GetIntent(query, "Datasets/general_questions_dataset.csv")
        data = Gquestion.getAnswers(intent[0], data)
        return data

    def open_hours(data):
        weekdays = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        isOpen = ['open','open','open','open','open','open','closed']
        hours = ['9-6pm','9-6pm','9-6pm','9-6pm','9-6pm','9-8pm','-']
        reply = ""

        reply += "Here is our schedule\n\n"
        for x in range(7):
            reply += "\t{} | {}\t{}\n".format(weekdays[x],isOpen[x],hours[x])

        data['output']['reply_template'] = reply
        data['output']['stopatpunct'] = False
        
        return data
    
    def ask_boss(data):
        reply = ""
        reply = "$ASKBOSS$"
        data['output']['reply_template'] = reply
        return data

    def ask_about_creator(data):
        reply = ""
        reply = "$ABOUTCREATOR$"
        data['output']['reply_template'] = reply
        return data

    def ask_time(data):
        reply = Util.ReplaceTags("$TIME$")
        month = [
                'January','February',
                'March','April',
                'May','June',
                'July','August',
                'September','October',
                'November','December'
            ]
        now = datetime.now()
        
        tuple = now.timetuple()
        amorpm = "am"
        y, m, d, h, min, sec, wd, yd, i = tuple
        month_text = month[m-1]
        if h > 12:
            h -= 12
            amorpm = "pm"
        reply = reply.format(hour=h, minute=min, month=month_text, day=d, year=y, ampm=amorpm)
        data['output']['reply_template'] = reply
        data['output']['stopatpunct'] = False
        return data

    def ask_about_me(data):
        reply = ""
        reply = "$ABOUTME$"
        data['output']['reply_template'] = reply
        return data

    def ask_about_name(data):
        reply = ""
        reply = "$TELL_NAME$"
        reply = Util.ReplaceVars(Util.ReplaceTags(reply))
        data['output']['reply_template'] = reply
        return data