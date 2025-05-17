from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

from search_memory import sm
from get_random_memory import rm
from get_memory import gm
from get_timeline import gt
from add_memory import am

# Search memories by keyword
@app.route('/search', methods=['GET'])
def search_memories():
    query = request.args.get("query", "")
    n = int(request.args.get("n", 3))
    query_time_str = request.args.get("query_time", None)
    relations_str = request.args.get("relations", "")

    query_time = None
    if query_time_str:
        try:
            query_time = datetime.fromisoformat(query_time_str)
        except:
            pass

    relations = [r.strip() for r in relations_str.split(",")] if relations_str else []

    try:
        results = sm(query=query, n=n, query_time=query_time, user_relations=relations)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Return a random memory (for random recall)
@app.route('/memory/random', methods=['GET'])
def get_random_memory():
    try:
        memory = rm()
        return jsonify(memory)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get full memory data by ID
@app.route('/memory/<int:memory_id>', methods=['GET'])
def get_memory(memory_id):
    try:
        memory = gm(memory_id)
        return jsonify(memory)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get compressed memory cards for timeline
@app.route('/timeline', methods=['GET'])
def get_timeline():
    try:
        timeline = gt()
        return jsonify(timeline)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Upload a new memory to the system
@app.route('/memory/upload', methods=['POST'])
def upload_memory():
    try:
        memory_data = request.get_json()
        result = am(memory_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5004)
