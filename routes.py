from flask import render_template, request, jsonify
from datetime import datetime
from utils import add_expense_to_csv, get_filtered_expenses
from charts import generate_charts

def init_routes(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/add-expense', methods=['POST'])
    def add_expense():
        data = request.json
        date = data.get('date', datetime.now().strftime("%Y-%m-%d"))
        amount = data['amount']
        category = data['category']
        
        add_expense_to_csv(date, amount, category)
        return jsonify({'status': 'success', 'message': 'Expense added successfully!'})

    @app.route('/get-expenses', methods=['GET'])
    def get_expenses():
        month = request.args.get('month')
        category = request.args.get('category')
        data = get_filtered_expenses(month, category)
        return data.to_json(orient='records')

    @app.route('/generate-report', methods=['GET'])
    def generate_report():
        month = request.args.get('month')
        data = get_filtered_expenses(month)
        
        if data.empty:
            return jsonify({'status': 'error', 'message': 'No data available for this month.'})

        bar_path, pie_path = generate_charts(data, month)
        return jsonify({
            'status': 'success',
            'bar_chart': bar_path,
            'pie_chart': pie_path
        })