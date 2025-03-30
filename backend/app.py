from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb://localhost:27017')
db=client["notes_app"]
collection=db["notes"]

@app.route('/get_notes', methods=["GET"])
def get_notes():
    notes=[]
    for note in collection.find():
        notes.append({
            # "id": str(note["_id"]),
            "title": note["title"],
            "content": note["content"]
        })
    return jsonify(notes)

@app.route('/add_note', methods=["POST"])
def add_note():
    data=request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if not "title" in data or not "content" in data:
        return jsonify({"error": "Invalid data"}), 400
    result=collection.insert_one(data)
    return jsonify({"message": "Note added successfully"}), 200

@app.route('/delete_note', methods=["DELETE"])
def delete_note():
    data=request.get_json()
    title=data["title"]
    result=collection.delete_one({"title": title})
    return jsonify({"message": f"{title} note deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True, threaded=False)