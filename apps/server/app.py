from flask import Flask, render_template, jsonify, request
from licensed.licensed import CSVLoader
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

api_endpoint = os.getenv('API_ENDPOINT')

csv_loader = CSVLoader("licensed/list.csv.zip")

CORS(app, resources={r"/*": {"origins": api_endpoint}})

@app.route('/get-columns', methods=['GET'])
def get_columns():
    return jsonify(csv_loader.get_columns())

@app.route('/filter', methods=['POST'])
def filter_data():
    """Filters the in-memory DataFrame based on user input."""
    try:
        data = request.get_json()
        if not isinstance(data, list):  # Expecting a list of (column, value) pairs
            return jsonify({"error": "Invalid input format, expected list of pairs"}), 400

        filtered_df = csv_loader.filter_by_criteria(data)
        return jsonify(filtered_df.to_dict(orient="records"))  # Return filtered results

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)