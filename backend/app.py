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
    return db.get_all_students(), 200


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
    if check is None: return {"error": "Student not found"}, 404
    return db.update_student(student_id, sd.get("name"), sd.get("course"), sd.get("mark")), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    check = db.get_student_by_id(student_id)
    if check: return db.delete_student(student_id)
    return {"error": "Student not found"}, 404


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    

    students = db.get_all_students()
    marks = []
    for student in students:
        mark = student["mark"]
        if mark is not None:
            marks.append(mark)
    count = len(marks)
    if count == 0:
        return jsonify({"count": 0, "average": None, "min": None, "max": None}), 200
    else:
        return jsonify({"count": count, "average": sum(marks)/count, "min": min(marks), "max": max(marks)}), 200

    """
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    all_students = db.get_all_students() # either is None or not None
    if all_students is None: return {"error": "no students exist"}, 404

    # check if there is a student with a mark
    all_marks = [s["mark"] for s in all_students if s.get("mark") is not None]
    #average = sum(all_marks)/len(all_marks)
    if (len(all_marks) == 0): return {"error": "no students with marks"}, 404
    stats = {
        "count": len(all_marks),
        "average": sum(all_marks) / len(all_marks),
        "min": min(all_marks),
        "max": max(all_marks),
    }
    return jsonify(stats), 200

@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
