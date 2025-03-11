from flask import Flask, request, jsonify
import time
import logging

app = Flask(__name__)
calculation_history = []  # Store history of calculations
start_time = time.time()  # Track API uptime

# Configure logging
logging.basicConfig(level=logging.INFO)

def add_to_history(operation, a, b, result):
    calculation_history.append({
        "operation": operation,
        "a": a,
        "b": b,
        "result": result
    })

@app.before_request
def log_request():
    """Log all incoming requests."""
    logging.info("Incoming request: %s %s | Params: %s", request.method, request.path, request.args)


@app.route('/healthz', methods=['GET'])
def health_check():
    """Health check endpoint to monitor uptime."""
    uptime = time.time() - start_time
    return jsonify(status="healthy", uptime=f"{uptime:.2f} seconds")

@app.route('/add', methods=['GET'])
def add():
    try:
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
        result = a + b
        add_to_history("addition", a, b, result)
        return jsonify(result=result)
    except (TypeError, ValueError):
        return jsonify(error="Invalid input"), 400

@app.route('/subtract', methods=['GET'])
def subtract():
    try:
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
        result = a - b
        add_to_history("subtraction", a, b, result)
        return jsonify(result=result)
    except (TypeError, ValueError):
        return jsonify(error="Invalid input"), 400

@app.route('/multiply', methods=['GET'])
def multiply():
    try:
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
        result = a * b
        add_to_history("multiplication", a, b, result)
        return jsonify(result=result)
    except (TypeError, ValueError):
        return jsonify(error="Invalid input"), 400

@app.route('/divide', methods=['GET'])
def divide():
    try:
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
        if b == 0:
            return jsonify(error="Division by zero is not allowed"), 400
        result = a / b
        add_to_history("division", a, b, result)
        return jsonify(result=result)
    except (TypeError, ValueError):
        return jsonify(error="Invalid input"), 400

@app.route('/history', methods=['GET'])
def history():
    return jsonify(history=calculation_history)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
