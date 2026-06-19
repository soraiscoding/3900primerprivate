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
    Diagnostic route to catch and print errors
    """
    try:
        all_students = get_all_students()
        
        # 1. Print exactly what the database is giving us
        print("\n=== DEBUG: DATABASE OUTPUT ===", file=sys.stderr)
        print(f"Type of all_students: {type(all_students)}", file=sys.stderr)
        print(f"Value of all_students: {all_students}", file=sys.stderr)
        
        if not all_students:
            return jsonify({"count": 0, "average": 0, "min": None, "max": None}), 200

        # 2. Print a sample student to see its structure
        print(f"Sample student structure: {all_students[0]}", file=sys.stderr)
        print(f"Sample student type: {type(all_students[0])}", file=sys.stderr)

        # Extract marks
        marks = [s.get("mark") for s in all_students if s.get("mark") is not None]
        print(f"Extracted marks: {marks}", file=sys.stderr)
        
        if not marks:
            return jsonify({"count": len(all_students), "average": 0, "min": None, "max": None}), 200

        num_students = len(all_students)
        total = sum(marks)
        average = total / len(marks)
        mini = min(marks)
        maxi = max(marks)

        return jsonify({
            "count": num_students,
            "average": round(average, 2),
            "min": mini,
            "max": maxi
        }), 200

    except Exception as e:
        # 3. Catch ANY crash and print the exact line/reason to the terminal
        print("\n=== DEBUG: CRASH DETECTED ===", file=sys.stderr)
        print(f"Error Type: {type(e).__name__}", file=sys.stderr)
        print(f"Error Message: {str(e)}", file=sys.stderr)
        print("=============================\n", file=sys.stderr)
        
        return jsonify({"error": f"Server crashed: {type(e).__name__} - {str(e)}"}), 500



@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
