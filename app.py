from flask import Flask, render_template, request, jsonify
from main import get_insurance_comparison

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    data = request.json
    insurance_names = data.get('insurance_names', [])
    
    if len(insurance_names) < 2:
        return jsonify({"error": "Please provide at least two insurance names"})
    
    try:
        result = get_insurance_comparison(insurance_names)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True) 