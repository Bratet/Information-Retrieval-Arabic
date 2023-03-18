import math
import pandas as pd
from collections import defaultdict
from pyarabic import araby
import pickle

class ArabicTfidfVectorizer:
    def __init__(self):
        self.term_document_frequency = defaultdict(set)
        self.documents = pd.DataFrame(columns=["doc_id", "content"])

    def _calculate_query_tfidf(self, docs, term_document_frequency):
        tfidf_matrix = []

        for doc in docs:
            tfidf_vector = {}
            tokens = araby.tokenize(doc)
            token_count = len(tokens)
            term_counts = defaultdict(int)

            for term in tokens:
                term_counts[term] += 1

            for term, count in term_counts.items():
                if term in term_document_frequency:
                    tf = count / token_count
                    idf = math.log(len(self.documents) / len(term_document_frequency[term]))
                    tfidf = tf * idf
                    tfidf_vector[term] = tfidf

            tfidf_matrix.append(tfidf_vector)

        return tfidf_matrix

    def transform(self, docs):
        return self._calculate_query_tfidf(docs, self.term_document_frequency)
    
    def fit_transform(self, docs):
        self.documents = docs
        self.term_document_frequency = self._calculate_term_document_frequency()
        return self._calculate_tfidf(self.documents, self.term_document_frequency)


    def _calculate_term_document_frequency(self, docs=None):
        if docs is None:
            docs = self.documents
        term_document_frequency = defaultdict(set)
        for doc_id, doc in docs.iterrows():
            tokens = araby.tokenize(doc['content'])
            unique_terms = set(tokens)
            for term in unique_terms:
                term_document_frequency[term].add(doc_id)
        return term_document_frequency

    def _calculate_tfidf(self, docs, term_document_frequency):
        tfidf_matrix = []

        for doc_id, doc in docs.iterrows():
            tfidf_vector = {}
            tokens = araby.tokenize(doc['content'])
            token_count = len(tokens)
            term_counts = defaultdict(int)

            for term in tokens:
                term_counts[term] += 1

            for term, count in term_counts.items():
                tf = count / token_count
                idf = math.log(len(docs) / len(term_document_frequency[term]))
                tfidf = tf * idf
                tfidf_vector[term] = tfidf

            tfidf_matrix.append(tfidf_vector)

        return tfidf_matrix

class ArabicIndexer:
    def __init__(self):
        self.documents = pd.DataFrame(columns=["doc_id", "content"])
        self.index = defaultdict(list)
        self.tfidf_vectorizer = ArabicTfidfVectorizer()

    def add_documents(self, docs):
        for doc_id, content in docs:
            new_doc = pd.DataFrame({"doc_id": [doc_id], "content": [content]})
            self.documents = pd.concat([self.documents, new_doc], ignore_index=True)
        self._create_index()

    def _create_index(self):
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.documents)
        for doc_id, doc_vector in enumerate(tfidf_matrix):
            for term, tfidf_weight in doc_vector.items():
                self.index[term].append((doc_id, tfidf_weight))

    def search(self, query, top_n=10):
        query_vector = self.tfidf_vectorizer.transform([query])[0]
        scores = defaultdict(float)

        for term, query_weight in query_vector.items():
            if term in self.index:
                for doc_id, doc_weight in self.index[term]:
                    scores[doc_id] += query_weight * doc_weight

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores[:top_n]

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
            
    def load(self, filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
        

# indexer = ArabicIndexer().load('indexer/indexer.pkl')

# query = "ما هو العمر القانوني للتصويت في الولايات المتحدة؟"

# from methods import preprocess

# query = preprocess(query)

# results = indexer.search(query)

# print(results)

