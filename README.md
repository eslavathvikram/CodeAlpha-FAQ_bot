# FAQ Chatbot - Task 2

A simple FAQ chatbot that:
- Stores FAQ questions and answers in JSON.
- Preprocesses text using NLTK.
- Converts FAQ questions to TF-IDF vectors.
- Uses cosine similarity to find the most similar FAQ.
- Returns the best matching answer.
- Includes a simple Flask web chat UI.

## Project Structure

```text
faq_chatbot/
├── app.py
├── chatbot.py
├── requirements.txt
├── README.md
├── data/
│   └── faqs.json
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## 1. Install Python

Use Python 3.9 or newer.

## 2. Create a virtual environment (recommended)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

The first run may download the NLTK English stopwords dataset automatically.

## 4. Run the chatbot

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## How it works

1. FAQ questions are loaded from `data/faqs.json`.
2. NLTK preprocessing converts text to lowercase, removes punctuation and stopwords.
3. `TfidfVectorizer` converts FAQ questions into numerical vectors.
4. The user's question is converted into a TF-IDF vector.
5. Cosine similarity compares the user question with every FAQ.
6. The FAQ with the highest similarity score is selected.
7. If the score is below the threshold, the chatbot says it could not find a suitable answer.
8. Flask sends the response to the web interface.

## Example questions

- How can I track my order?
- Can I return my product?
- What payment methods do you accept?
- How long does delivery take?
- Can I cancel my order?
- How do I reset my password?

## Customizing FAQs

Edit:

```text
data/faqs.json
```

Add more objects in this format:

```json
{
  "question": "Your question here",
  "answer": "Your answer here"
}
```

## Main technologies

- Python
- Flask
- NLTK
- Scikit-learn
- TF-IDF
- Cosine Similarity
- HTML/CSS/JavaScript

## Task requirements covered

✓ Collect FAQs and answers  
✓ NLP preprocessing  
✓ Similarity-based FAQ matching  
✓ Best answer displayed as chatbot response  
✓ Simple chat UI
