from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import numpy as np

# Download NLTK data
import nltk
nltk.download("punkt")
nltk.download("stopwords")

def preprocess_text(text: str) -> str:
    """
    Preprocess text by removing punctuation and lowercasing.
    """
    # Remove punctuation and lowercase
    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    print(f"Processed text: {text}")  # Debug print
    return text

def compute_tfidf(corpus: list[str], query: str) -> np.ndarray:
    """
    Compute TF-IDF scores for a query against a corpus.
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    query_vector = vectorizer.transform([query])
    scores = (tfidf_matrix * query_vector.T).toarray().flatten()
    return scores