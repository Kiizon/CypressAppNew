from flask import jsonify, request
from models.report import Report, db  # Import the Report model
# Display all users
def index():
    # Query all users from the database
    reports = Report.query.all()

    # Convert all users to a list of dictionaries using the to_dict method
    reports_list = [report.to_dict() for report in reports]

    # Return the list as a JSON response
    return jsonify(reports_list)

# Method to insert a new report
def insert_report():
    # Get the data from the request (assuming JSON payload)
    data = request.get_json()

    # Ensure the required fields are in the request
    if not data or not data.get('name') or not data.get('description'):
        return jsonify({"error": "Missing required fields"}), 400

    # Create a new report object
    new_report = Report(
        name=data['name'],
        description=data['description'],
        longitude=data.get('longitude'),
        latitude=data.get('latitude'),
        category=data.get('category'),
        user_id=data.get('user_id')
    )

    # Add the new report to the database
    db.session.add(new_report)
    db.session.commit()

    # Return the newly created report as a JSON response
    return jsonify(new_report.to_dict()), 201
