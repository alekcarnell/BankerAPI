from flask import Flask, jsonify, request
from routes import routes

app = Flask(__name__)

# Register routes.py blueprint
app.register_blueprint(routes, url_prefix='/api') 

# Run the app
if __name__ == '__main__':
    app.run(debug=True)