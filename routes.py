from flask import Blueprint, jsonify, request
from data_handler import load_data, save_data
from validators import validate_rate_input
from datetime import datetime

routes = Blueprint('routes', __name__)

# Default and Home route
@routes.route('/')
def home():
    return "Welcome to the Bank Interest Rate API!"



# Rates route that accepts filtering
@routes.route('/rates', methods=['GET'])
def get_rates():

    print("GET /rates was hit")

    # Start with an unfiltered list
    bank_rates = load_data()

    # Get parameters from the URL
    country = request.args.get('country')
    bank = request.args.get('bank')
    account_type = request.args.get('account_type')

    # Filter list if applicable
    if country:
        bank_rates = [r for r in bank_rates if r['country'].lower() == country.lower()]
    if bank:
        bank_rates = [r for r in bank_rates if bank.lower() in r['bank'].lower()]
    if account_type:
        bank_rates = [r for r in bank_rates if r['account_type'].lower() == account_type.lower()]

    # Return the results
    return jsonify(bank_rates)



# Direct lookup route based on the ID
@routes.route('/rates/<int:rate_id>', methods=['GET'])
def get_rate_id(rate_id):
    bank_rates = load_data()

    rate = next((r for r in bank_rates if r["id"] == rate_id), None)
    if rate:
        return jsonify(rate)
    return jsonify({"error": "Rate not found"}), 404



# POST route for adding an entry
@routes.route('/rates', methods=['POST'])
def create_rate():
    # Get incoming data from the request body and send it to the validator to be sanitized. 
    data = request.get_json()
    is_valid, result = validate_rate_input(data, require_all_fields=True)

    # If the boolean from the validator comes back false, return a user-friendly error. 
    if not is_valid:
        return jsonify({"error": result}), 400

    # Otherwise, use our load_data function to prepare our JSON file to receive the incoming data. 
    rates = load_data()
    new_id = max((r["id"] for r in rates), default=0) + 1

    # Create new rate dictionary
    new_rate = {
        "id": new_id,
        **result, # Dictionary unpacking operater which plugs each piece from the dictionary into the next slot of our JSON structure. 
        "last_updated": data.get("last_updated") or datetime.now().strftime("%Y-%m-%d")
    }

    # Append the changes and save them to the JSON database. 
    rates.append(new_rate)
    save_data(rates)
    return jsonify(new_rate), 201



# PUT route for updating data
@routes.route('/rates/<int:rate_id>', methods=['PUT'])
def update_rate(rate_id):
    rates = load_data()
    data = request.get_json()

    rate = next((r for r in rates if r["id"] == rate_id), None)
    if not rate:
        return jsonify({"error": "Rate not found"}), 404

    is_valid, result = validate_rate_input(data, require_all_fields=False)
    if not is_valid:
        return jsonify({"error": result}), 400

    # Update only the provided fields and attach the timestamp (either user provided or dynamic)
    rate.update(result)
    rate["last_updated"] = data.get("last_updated") or datetime.now().strftime("%Y-%m-%d")

    save_data(rates)
    return jsonify(rate), 200



# DELETE route to remove a data entry
@routes.route('/rates/<int:rate_id>', methods=['DELETE'])
def delete_rate(rate_id):

    rates = load_data()

    rate = next((r for r in rates if r['id'] == rate_id), None)
    if not rate:
        return jsonify({"error": "Rate not found"}), 404

    rates = [r for r in rates if r['id'] != rate_id]
    save_data(rates)
    return jsonify({"message": f"Rate {rate_id} deleted"}), 200