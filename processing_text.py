# -*- coding: utf-8 -*-

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, SnowballStemmer, WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

class Processing_Text:
    """
بيجهز كلاس Processing_Text بكل حاجات ال NLTK اللي محتاجينها
وبيظبط ال stopwords و Porter Stemmer و Snowball Stemmer و WordNet Lemmatizer
"""

    def __init__(self):
        self.stop_words = set(stopwords.words("english"))
        self.porter = PorterStemmer()
        self.snowball = SnowballStemmer("english")
        self.lemmatizer = WordNetLemmatizer()

    def Tokenze(self, text):
        """
بيقسم النص اللي داخل لكلمات منفصلة وبيستخدم regex علشان يحدد حدود الكلمات
Args
    text  النص اللي هنعمله tokenizing
Returns
    list  ليست بالكلمات اللي اتسحبت من النص
"""
        # بيدور على أي سلسلة حروف او ارقام ويعتبرها توكن
        return re.findall(r"\b\w+\b", text)

    def Normalize(self, tokens):
        """
بيعمل Normalize لل tokens عن طريق انه يحولهم lowercase
ويشيل اي توكن مش عبارة عن حروف بس
Args
    tokens list  ليست التوكنز اللي داخلة
Returns
    list  ليست جديدة فيها بس التوكنز المتظبطة واللي كلها حروف وب lowercase
"""
        return [t.lower() for t in tokens if t.isalpha()]

    def Stop_r_W(self, tokens):
        """
بيشيل ال stopwords الانجليزي المشهورة من ليست التوكنز
Args
    tokens list  ليست التوكنز اللي داخلة
Returns
    list  ليست جديدة من غير ال stopwords
"""
        return [t for t in tokens if t not in self.stop_words]

    def Stm(self, tokens, algorithm='porter'):
        """
بيطبق ال stemming على ليست التوكنز باستخدام ال algorithm اللي انا مختراه Porter او Snowball
وال stemming بيقلل الكلمة لاصلها
Args
    tokens list  ليست التوكنز اللي داخلة
    algorithm str اختياري
Returns
    list  ليست التوكنز بعد ال stemming
"""
        if algorithm == 'Snowball':
            return [self.snowball.stem(t) for t in tokens]
        return [self.porter.stem(t) for t in tokens]

    def lemm(self, tokens):
        """
بيطبق ال lemmatization على ليست التوكنز
وال lemmatization بيرجع الكلمة لاصلها القاموسي
"""
        return [self.lemmatizer.lemmatize(t) for t in tokens]

    def text_process(self, text):
        """
بيعمل بروسسينج كامل للنص اللي داخل
"""
        tokens = self.Tokenze(text)
        norm = self.Normalize(tokens)
        filterd = self.Stop_r_W(norm)
        steemd = self.Stm(filterd)
        lemmatized = self.lemm(steemd)
        return lemmatized
