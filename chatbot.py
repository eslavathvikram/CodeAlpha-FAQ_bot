"""
Pure-Python FAQ chatbot — no scipy/scikit-learn required.
Uses TF-IDF + cosine similarity implemented from scratch.
"""
import json
import re
import math

try:
    import nltk
    from nltk.corpus import stopwords
    STOP_WORDS = set(stopwords.words("english"))
except Exception:
    try:
        import nltk
        nltk.download("stopwords", quiet=True)
        from nltk.corpus import stopwords
        STOP_WORDS = set(stopwords.words("english"))
    except Exception:
        # Fallback minimal stop-word list (no NLTK needed)
        STOP_WORDS = {
            "i","me","my","we","our","you","your","he","she","it","they","them",
            "what","which","who","whom","this","that","these","those","am","is",
            "are","was","were","be","been","being","have","has","had","do","does",
            "did","will","would","could","should","may","might","shall","can",
            "a","an","the","and","but","or","nor","so","yet","for","of","at",
            "by","in","to","up","on","off","over","under","again","then","once",
            "here","there","when","where","why","how","all","both","each","few",
            "more","most","other","some","such","no","not","only","own","same",
            "than","too","very","just","about","into","through","with","from",
    }


def _preprocess(text: str) -> list[str]:
    """Lowercase, strip punctuation, remove stop-words, return token list."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = [w for w in text.split() if w and w not in STOP_WORDS]
    return tokens


def _tf(tokens: list[str]) -> dict[str, float]:
    freq: dict[str, int] = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    total = max(len(tokens), 1)
    return {t: c / total for t, c in freq.items()}


def _build_idf(corpus: list[list[str]]) -> dict[str, float]:
    N = len(corpus)
    df: dict[str, int] = {}
    for doc in corpus:
        for t in set(doc):
            df[t] = df.get(t, 0) + 1
    return {t: math.log((N + 1) / (n + 1)) + 1 for t, n in df.items()}


def _tfidf_vec(tokens: list[str], idf: dict[str, float]) -> dict[str, float]:
    tf = _tf(tokens)
    return {t: tf[t] * idf.get(t, 1.0) for t in tf}


def _cosine(v1: dict[str, float], v2: dict[str, float]) -> float:
    shared = set(v1) & set(v2)
    if not shared:
        return 0.0
    dot = sum(v1[k] * v2[k] for k in shared)
    mag1 = math.sqrt(sum(x * x for x in v1.values()))
    mag2 = math.sqrt(sum(x * x for x in v2.values()))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


class FAQChatbot:
    def __init__(self, faq_file: str, threshold: float = 0.20):
        with open(faq_file, "r", encoding="utf-8") as f:
            self.faqs = json.load(f)

        self._corpus_tokens = [_preprocess(item["question"]) for item in self.faqs]
        self._idf = _build_idf(self._corpus_tokens)
        self._faq_vecs = [_tfidf_vec(tokens, self._idf) for tokens in self._corpus_tokens]
        self.threshold = threshold

    def get_answer(self, user_question: str) -> tuple[str, float]:
        q_tokens = _preprocess(user_question)
        q_vec = _tfidf_vec(q_tokens, self._idf)

        best_score = 0.0
        best_index = 0
        for i, faq_vec in enumerate(self._faq_vecs):
            score = _cosine(q_vec, faq_vec)
            if score > best_score:
                best_score = score
                best_index = i

        if best_score < self.threshold:
            return (
                "Sorry, I couldn't find a close FAQ match. "
                "Please try asking in a different way.",
                best_score,
            )

        return self.faqs[best_index]["answer"], best_score
