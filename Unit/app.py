from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

WeightOptions = {
    'kilogram': 1,          # Baseline unit
    'gram': 1000,           # 1 kilogram = 1000 grams
    'milligram': 1e6,       # 1 kilogram = 1,000,000 milligrams
    'microgram': 1e9,       # 1 kilogram = 1,000,000,000 micrograms
    'ton': 0.001,           # 1 kilogram = 0.001 tons (metric ton)
    'pound': 2.20462,       # 1 kilogram = 2.20462 pounds
    'ounce': 35.274,        # 1 kilogram = 35.274 ounces
    'stone': 0.157473,      # 1 kilogram = 0.157473 stones
    'short_ton': 0.00110231,# 1 kilogram = 0.00110231 short tons (US ton)
    'long_ton': 0.000984207,# 1 kilogram = 0.000984207 long tons (Imperial ton)
    'carat': 5000,          # 1 kilogram = 5000 carats
    'atomic_mass_unit': 6.022e26, # 1 kilogram = 6.022e26 atomic mass units (amu)
}

sWeightOptions = set(WeightOptions.keys())

LengthOptions = {
    'meter': 1,               # Baseline unit
    'kilometer': 0.001,       # 1 meter = 0.001 kilometers
    'centimeter': 100,        # 1 meter = 100 centimeters
    'millimeter': 1000,       # 1 meter = 1000 millimeters
    'micrometer': 1e6,        # 1 meter = 1,000,000 micrometers
    'nanometer': 1e9,         # 1 meter = 1,000,000,000 nanometers
    'mile': 0.000621371,      # 1 meter = 0.000621371 miles
    'yard': 1.09361,          # 1 meter = 1.09361 yards
    'foot': 3.28084,          # 1 meter = 3.28084 feet
    'inch': 39.3701,          # 1 meter = 39.3701 inches
    'nautical_mile': 0.000539957, # 1 meter = 0.000539957 nautical miles
    'light_year': 1.057e-16,  # 1 meter = 1.057e-16 light years
    'astronomical_unit': 6.68459e-12, # 1 meter = 6.68459e-12 astronomical units
    'parsec': 3.24078e-17,    # 1 meter = 3.24078e-17 parsecs
    'furlong': 0.00497096,    # 1 meter = 0.00497096 furlongs
    'angstrom': 1e10,         # 1 meter = 10,000,000,000 angstroms
}

sLengthOptions = set(LengthOptions.keys())

# Example conversion function to be used
def convert(from_unit: str, to_unit: str, value: float) -> (float, int):
    # Here you can implement your logic for unit conversion
    # This is just a placeholder example
    if from_unit in sLengthOptions and to_unit in sLengthOptions:
        return value / LengthOptions[from_unit] * LengthOptions[to_unit], 0
    if from_unit in sWeightOptions and to_unit in sWeightOptions:
        return value / WeightOptions[from_unit] * WeightOptions[to_unit], 0
    return None, 1


# Route for both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Expect JSON data with 'from' and 'to' fields
        data = request.get_json()
        if not data or 'from' not in data or 'to' not in data or 'value' not in data:
            return jsonify({"error": "Invalid JSON request, 'value', 'from' and 'to' fields are required"}), 400

        # Retrieve the 'from' and 'to' values
        from_unit = data['from']
        to_unit = data['to']
        value = data['value']

        if not isinstance(value, float) and not isinstance(value, int):
            return jsonify({"error": "Invalid JSON request, 'value' is not a numeric value"}), 400

        # Call the convert function
        result, status = convert(from_unit, to_unit, value)

        # Return the result as a JSON response
        return jsonify({"result": result if status == 0 else "error..."})

    # For GET request, return the usage information
    else:
        return send_from_directory('static', 'index.html')

# Route for GET requests
@app.route('/available-options', methods=['GET'])
def available_options():
    return jsonify({"length": list(sLengthOptions), "weight": list(sWeightOptions)})

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
#
