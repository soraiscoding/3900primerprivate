from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    return db.get_all_students()


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """
    # Getting the request body - replace with your implementation
    # sd is student data
    sd = request.json
    return db.insert_student(sd.get("name"), sd.get("course"), sd.get("mark")), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    sd = request.json

    # check student exists
    check = db.get_student_by_id(student_id)
    if check: return db.update_student(student_id, sd.get("name"), sd.get("course"), sd.get("mark"))
    return 404


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    check = db.get_student_by_id(student_id)
    if check: return db.delete_student(student_id)
    return 404


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    all_students = get_all_students() # either is None or not None
    if (all_students is None): return 404

    # check if there is a student with a mark
    i = 0
    for s in all_students and int(s.get("mark")) is not None:
        i += 1

    if (i == 0): return 404

    average = 0
    total = 0
    minn = all_students[0].get("mark") # placeholder value
    maxx = 0
    for s in all_students and int(s.get("mark")) is not None:
        total = total + int(s.get("mark"))
        if (int(s.get("mark")) < minn): minn = int(s.get("mark"))
        if (int(s.get("mark")) > maxx): maxx = int(s.get("mark"))

    # if minn or maxx is still None then no students had a mark
    # if (minn == None): minn = 0
    # if (maxx == None): maxx = 0
    average = total/i
    stats = {
        "count": i,
        "average": average,
        "min": minn,
        "max": maxx
    }
    return jsonify(stats), 200  # replace with your implementation


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
