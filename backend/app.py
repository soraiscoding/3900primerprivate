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
    return get_all_students()


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
    return insert_student(sd.get(name), sd.get(course), sd.get(mark))


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    pass  # replace with your implementation


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    return delete_student()


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    all_students = get_all_students()
    num_students = len(all_students)
    # mini = all_students(min) i dont think thisll work
    # maxi = all_students(max)
    minn = None # placeholder value
    maxx = None
    for s in all_students:
        total = total + s.get(mark)
        if (s.get(mark) < minn) minn = s.get(mark)
        if (s.get(mark) > minn) maxx = = s.get(mark)
        num_students++

    average = total/num_students
    stats = {
        "count": num_students,
        "average": average,
        "min": minn,
        "max": maxx
    }
    return stats  # replace with your implementation


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
