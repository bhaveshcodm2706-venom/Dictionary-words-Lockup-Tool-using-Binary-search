
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Dictionary words are stored in alphabetical order.
# Each word appears only once.
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

# Sorted list ensures binary search works correctly.
words = sorted(dictionary.keys())


def binary_search(search_word):
    low = 0
    high = len(words) - 1
    steps = []

    while low <= high:
        middle = (low + high) // 2
        middle_word = words[middle]

        # Save the current search range for visualization.
        steps.append({
            "low": low,
            "high": high,
            "middle": middle,
            "middle_word": middle_word,
            "explanation": (
                f"Check the middle word: '{middle_word}'. "
                f"The current search range is positions {low} to {high}."
            )
        })

        if middle_word == search_word:
            return {
                "found": True,
                "word": middle_word,
                "meaning": dictionary[middle_word],
                "steps": steps
            }

        elif search_word < middle_word:
            high = middle - 1
        else:
            low = middle + 1

    return {
        "found": False,
        "word": search_word,
        "meaning": "",
        "steps": steps
    }


@app.route("/")
def home():
    return jsonify({
        "message": "Dictionary Binary Search API is running."
    })


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
            "message": "Please enter a word."
        }), 400

    search_word = search_word.strip().lower()
    result = binary_search(search_word)
    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
