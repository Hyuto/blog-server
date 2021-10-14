from django.apps import AppConfig
import re, string, pickle
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

STEMMER = StemmerFactory().create_stemmer()

with open("setiment_analisis_corona/kamus/stopwords.txt", "r") as f:
    stop_words = f.readline().split()

# Cleanner
def cleaning(text):
    text = text.replace("\\n", " ")
    return text


# Preprocessor
def preprocessor(text):
    text = text.lower()
    text = text.replace("\\xe2\\x80\\xa6", "")
    text = re.sub("((www\.[^\s]+)|(https?://[^\s]+))", "", text)
    text = re.sub("@[^\s]+", "", text)
    text = re.sub("[\s]+", " ", text)
    text = re.sub(r"#([^\s]+)", r"\1", text)
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    return text


def tokenizer(text):
    words = text.split()
    tokens = [STEMMER.stem(w.lower()) for w in words if len(w) > 3 and w not in stop_words]
    return tokens


class SAModel:
    def __init__(self, project_dir):
        self.vectorizer_tfidf = """UPDATING MODEL
        pickle.load(
            open(f"{project_dir}/model/[TRAINED] TF-IDF Vectorizer.pickle", "rb")
        )"""
        self.model = pickle.load(open(f"{project_dir}/model/[TRAINED] SVM.pickle", "rb"))
        self.label = {-1: "Negatif", 0: "Netral", 1: "Positif"}

    def analyst(self, words):
        words = [cleaning(words)]
        words = self.vectorizer_tfidf.transform(words)

        return self.label[self.model.predict(words)[0]]


class SetimentAnalisisCoronaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "setiment_analisis_corona"
    model = SAModel(name)
