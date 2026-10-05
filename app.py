from flask import Flask, render_template, request, jsonify
from chatbot import FAQChatbot

app = Flask(__name__)
bot = FAQChatbot("data/faqs.json")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()

    if not question:
        return jsonify({"answer": "Please enter a question."})

    answer, score = bot.get_answer(question)
    return jsonify({"answer": answer, "score": round(float(score), 3)})

if __name__ == "__main__":
    app.run(debug=True)
