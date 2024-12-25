from flask import Flask
from routes import init_routes
from utils import init_expense_file

app = Flask(__name__)

# Initialize the expense file if it doesn't exist
init_expense_file()

# Register routes
init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)