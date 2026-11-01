from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

dictionary = {
    "algorithm": "A step-by-step procedure for solving a problem.",
    "binary": "A number system that uses only 0 and 1.",
    "computer": "An electronic device that processes data.",
    "database": "An organized collection of information.",
    "function": "A reusable block of code that performs a task.",
    "internet": "A global network of interconnected computers.",
    "keyword": "A reserved word with a special meaning in a programming language.",
    "loop": "A programming structure that repeats instructions.",
    "python": "A high-level programming language.",
    "search": "The process of finding a particular item."
}

words = sorted(dictionary.keys())


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Dictionary Binary Search API is running."
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/api/words", methods=["GET"])
def get_words():
    return jsonify({"words": words})


@app.route("/api/search", methods=["POST"])
def search():
    data = request.get_json(silent=True) or {}
    search_word = data.get("word", "")

    if not isinstance(search_word, str) or not search_word.strip():
        return jsonify({
            "found": False,
            "word": "",
            "meaning": "",
            "steps": [],
            "words": words,
            "message": "Please enter a valid word."
        }), 400

    search_word = search_word.strip().lower()

    low = 0
    high = len(words) - 1
    steps = []
    comparison = 0
    found_index = -1

    while low <= high:
        middle = (low + high) // 2
        middle_word = words[middle]
        comparison += 1

        steps.append({
            "low": low,
            "high": high,

            # Both versions of your JavaScript are supported.
            "middle": middle,
            "mid": middle,

            "middle_word": middle_word,
            "comparison_number": comparison,

            "explanation": (
                f"Checking middle word: {middle_word}. "
                f"Current search range: {low} to {high}."
            )
        })

        if middle_word == search_word:
            found_index = middle
            break

        elif search_word < middle_word:
            high = middle - 1

        else:
            low = middle + 1

    found = found_index != -1

    return jsonify({
        "found": found,
        "word": search_word,
        "meaning": dictionary.get(search_word, ""),
        "index": found_index,
        "words": words,
        "steps": steps
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)