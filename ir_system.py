# -*- coding: utf-8 -*-

import numpy as np

class InformationRetrievalSystem:
    def __init__(self, documents):
        self.documents = documents
        self.doc_ids = list(documents.keys())
        self.processed_docs = list(documents.values())
        self.inverted_index = self.build_inverted_index()
        self.tf_docs = [self.compute_tf(doc) for doc in self.processed_docs]
        self.idf = self.compute_idf()

    def build_inverted_index(self):
        inverted_index = {}
        for doc_id, tokens in self.documents.items():
            for token in tokens:
                if token not in inverted_index:
                    inverted_index[token] = set()
                inverted_index[token].add(doc_id)
        return inverted_index

    def compute_tf(self, doc_tokens):
        """
بيحسب ال Term Frequency TF لكل توكن جوه الدوكمنت
وال TF هو عدد مرات ظهور الكلمة في الدوكمنت مقسوم على عدد كل الكلمات في نفس الدوكمنت
"""
        tf = {}
        total = len(doc_tokens)
        if total == 0:
            return tf
        for t in doc_tokens:
            tf[t] = tf.get(t, 0) + 1
        for t in tf:
            tf[t] /= total
        return tf

    def compute_idf(self):
        """
بيحسب ال Inverse Document Frequency IDF لكل التوكنز الفريدة في كل الكوربس
"""
        idf = {}
        N = len(self.processed_docs)
        for term in self.inverted_index:
            dfreq = len(self.inverted_index[term])
            idf[term] = np.log((N + 1) / (dfreq + 1)) + 1
        return idf

    def cosine_similarity(self, query_vec, doc_vec):
        """
بيحسب ال cosine similarity بين اتنين vectors
"""
        common = set(query_vec) & set(doc_vec)
        num = sum(query_vec[t] * doc_vec[t] for t in common)
        denom = np.sqrt(sum(v*v for v in query_vec.values())) * np.sqrt(sum(v*v for v in doc_vec.values()))
        return num / denom if denom != 0 else 0.0

    def search(self, query, processor, top_k=10):
        q_tokens = processor.text_process(query)
        q_tf = self.compute_tf(q_tokens)
        q_vec = {t: q_tf[t] * self.idf.get(t, 0) for t in q_tf}

        scores = []
        for i, doc_tf in enumerate(self.tf_docs):
            doc_vec = {t: doc_tf[t] * self.idf[t] for t in doc_tf}
            score = self.cosine_similarity(q_vec, doc_vec)
            scores.append((self.doc_ids[i], score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
    
    def boolean_search(self, query, processor, mode="AND"):
     
        tokens = processor.text_process(query)
        if not tokens:
            return []
    
        sets = [self.inverted_index.get(t, set()) for t in tokens]
    
        if mode == "AND":
            result = sets[0]
            for s in sets[1:]:
                result = result & s
        else:  # OR
            result = set()
            for s in sets:
                result = result | s
    
        return list(result)