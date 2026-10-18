
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# For a student project, allow the StackBlitz frontend to connect.
# In production, restrict CORS to your actual frontend domain.
CORS(app)

# Dictionary data: each word has a meaning.
DICTIONARY = [
    {
        "word": "Algorithm",
        "meaning": "A step-by-step procedure for solving a problem or performing a computation."
    },
    {
        "word": "Array",
        "meaning": "A data structure that stores elements in an indexed sequence."
    },
    {
        "word": "Binary",
        "meaning": "A number system that uses only two digits: 0 and 1."
    },
    {
        "word": "Book",
        "meaning": "A collection of written or printed pages bound together."
    },
    {
        "word": "Code",
        "meaning": "Instructions written in a programming language for a computer to execute."
    },
    {
        "word": "Computer",
        "meaning": "An electronic device that processes data according to instructions."
    },
    {
        "word": "Database",
        "meaning": "An organized collection of data that can be accessed and managed."
    },
    {
        "word": "Data",
        "meaning": "Facts and information collected for reference or analysis."
    },
    {
        "word": "Disk",
        "meaning": "A storage device or medium used to store digital information."
    },
    {
        "word": "Function",
        "meaning": "A reusable block of code designed to perform a particular task."
    },
    {
        "word": "Internet",
        "meaning": "A worldwide network connecting computers and other devices."
    },
    {
        "word": "Loop",
        "meaning": "A programming structure that repeats a block of instructions."
    },
    {
        "word": "Python",
        "meaning": "A high-level programming language known for its readable syntax."
    },
    {
        "word": "Search",
        "meaning": "The process of finding a specific item in a collection."
    }
]

# Binary search requires the words to be sorted.
DICTIONARY.sort(key=lambda item: item["word"].casefold())


def binary_search(target):
    """Return the real binary-search steps and the matching definition."""

    target = target.strip().casefold()
    words = [item["word"] for item in DICTIONARY]

    low = 0
    high = len(words) - 1
    steps = []
    comparison_number = 0

    while low <= high:
        middle = (low + high) // 2
        middle_word = words[middle]
        comparison_number += 1

        # Record each actual comparison made by the algorithm.
        step = {
            "low": low,
            "mid": middle,
            "high": high,
            "word": middle_word,
            "comparison_number": comparison_number,
            "explanation": ""
        }

        middle_key = middle_word.casefold()

        if middle_key == target:
            step["explanation"] = (
                f'The middle word "{middle_word}" matches '
                f'the target. The word has been found.'
            )
            steps.append(step)

            return {
                "found": True,
                "word": middle_word,
                "meaning": DICTIONARY[middle]["meaning"],
                "index": middle,
                "comparisons": comparison_number,
                "steps": steps
            }

        elif target < middle_key:
            step["explanation"] = (
                f'"{target}" comes before "{middle_word}". '
                f'Discard the upper half and search the left half.'
            )
            steps.append(step)
            high = middle - 1

        else:
            step["explanation"] = (
                f'"{target}" comes after "{middle_word}". '
                f'Discard the lower half and search the right half.'
            )
            steps.append(step)
            low = middle + 1

    return {
        "found": False,
        "word": target,
        "meaning": "",
        "index": -1,
        "comparisons": comparison_number,
        "steps": steps
    }


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "LexiSearch Python API is running.",
        "endpoints": ["/api/search", "/api/words"]
    })


@app.route("/api/search", methods=["POST"])
def search_word():
    data = request.get_json(silent=True) or {}
    word = data.get("word", "")

    if not isinstance(word, str) or not word.strip():
        return jsonify({"error": "Please provide a valid word."}), 400

    result = binary_search(word)

    # Send the actual sorted words to the visualization.
    result["words"] = [item["word"] for item in DICTIONARY]

    return jsonify(result)


@app.route("/api/words", methods=["GET"])
def get_words():
    return jsonify({
        "words": DICTIONARY,
        "total": len(DICTIONARY)
    })


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
