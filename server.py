from flask import Flask, jsonify

import json

app = Flask(__name__)

# Load JSON data from file
with open("periodic_elements.json", "r", encoding="utf-8") as file:
    elements_data = json.load(file)

@app.route('/elements', methods=['GET'])
def get_elements():
    return jsonify(elements_data)

@app.route('/element/<symbol>', methods=['GET'])
def get_element(symbol):
    # Find the element by symbol
    element = next((el for el in elements_data if el["symbol"].lower() == symbol.lower()), None)
    
    if element:
        return jsonify(element)
    else:
        return jsonify({"error": "Element not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
