from django.apps import AppConfig
import re, string, pickle
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


class SAModel:
    stemmer = StemmerFactory().create_stemmer()

    def __init__(self, project_dir):
        self.vectorizer_tfidf = pickle.load(
            open(f"{project_dir}/model/[TRAINED] TF-IDF Vectorizer.pickle", "rb")
        )
        self.model = pickle.load(open(f"{project_dir}/model/[TRAINED] SVM.pickle", "rb"))
        self.label = {-1: "Negatif", 0: "Netral", 1: "Positif"}

        with open("setiment_analisis_corona/kamus/stopwords.txt", "r") as f:
            self.stopwords = f.readline().split()

    def preprocessor(self, text):
        text = text.replace("\\n", " ")
        text = text.lower()
        text = text.replace("\\xe2\\x80\\xa6", "")
        text = re.sub("((www\.[^\s]+)|(https?://[^\s]+))", "", text)
        text = re.sub("@[^\s]+", "", text)
        text = re.sub("[\s]+", " ", text)
        text = re.sub(r"#([^\s]+)", r"\1", text)
        text = re.sub(r"\d+", "", text)
        text = text.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
        return text

    def tokenizer(self, text):
        words = text.split()
        tokens = [
            self.stemmer.stem(w.lower()) for w in words if len(w) > 3 and w not in self.stopwords
        ]
        return tokens

    def analyst(self, words):
        words = [self.preprocessor(words)]
        words = self.vectorizer_tfidf.transform(words)

        return self.label[self.model.predict(words)[0]]


class SetimentAnalisisCoronaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "setiment_analisis_corona"
    model = SAModel(name)
