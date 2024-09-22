from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

# Home route to verify the API is working
@app.route('/')
def home():
    return "Welcome to the BFHL API"

# GET method that returns the hardcoded operation code
@app.route('/bfhl', methods=['GET'])
def bfhl_get():
    response = {
        "operation_code": 1
    }
    return jsonify(response), 200

# POST method that processes user data and Base64 encoded file
@app.route('/bfhl', methods=['POST'])
def bfhl_post():
    try:
        # Parse incoming request data
        data = request.json.get('data', [])
        file_b64 = request.json.get('file_b64', None)

        # Extract numbers and alphabets from the 'data' array
        numbers = [item for item in data if item.isdigit()]
        alphabets = [item for item in data if item.isalpha()]

        # Get all lowercase alphabets and find the highest
        lowercase_alphabets = [ch for ch in alphabets if ch.islower()]
        highest_lowercase_alphabet = max(lowercase_alphabets, default=None)

        # Static user information (for demo purposes)
        user_id = "john_doe_17091999"
        email = "john@xyz.com"
        roll_number = "ABCD123"

        # File handling logic
        file_valid = False
        file_mime_type = None
        file_size_kb = None

        if file_b64:
            try:
                # Decode the Base64 file and calculate its size
                file_data = base64.b64decode(file_b64)
                file_size_kb = len(file_data) / 1024
                file_mime_type = "application/octet-stream"  # Generic MIME type
                file_valid = True
            except Exception:
                file_valid = False

        # Create response
        response = {
            "is_success": True,
            "user_id": user_id,
            "email": email,
            "roll_number": roll_number,
            "numbers": numbers,
            "alphabets": alphabets,
            "highest_lowercase_alphabet": [highest_lowercase_alphabet] if highest_lowercase_alphabet else [],
            "file_valid": file_valid,
            "file_mime_type": file_mime_type,
            "file_size_kb": file_size_kb
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"is_success": False, "error": str(e)}), 400

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
