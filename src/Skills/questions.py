

class questions():

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
        tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
        df = CHATBOT.data_prepare(dataset)
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
        clf,count_vect= CHATBOT.naive_algo(dataset)
        intent = clf.predict(count_vect.transform([question]))
        # intent = str(intent).strip("['']")
        return intent

    def run(data):
        return data