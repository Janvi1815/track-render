# travel_bp/routes.py
import csv
import os
from flask import Blueprint, render_template, request

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/custom')
def custom():
    return render_template('custom.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        month = request.form.get('month')
        days = request.form.get('days')
        travellers = request.form.get('travellers')
        details = request.form.get('details')

        # ✅ Save data to CSV file in the 'data' folder
        base_dir = os.path.abspath(os.path.dirname(__file__))  # path to travel_bp/
        data_folder = os.path.normpath(os.path.join(base_dir, '..', 'data'))
        os.makedirs(data_folder, exist_ok=True)  # auto create 'data/' if not exists

        file_path = os.path.join(data_folder, 'form_submissions.csv')
        file_exists = os.path.isfile(file_path)

        try:
            with open(file_path, mode='a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(['Name', 'Email', 'Phone', 'Month', 'Days', 'Travellers', 'Details'])  # header
                writer.writerow([name, email, phone, month, days, travellers, details])
        except Exception as e:
            print("❌ Error writing to CSV:", e)

        return render_template('contact.html', success=True)

    return render_template('contact.html')

@main.route('/travel')
def travel_blog():
    return render_template('travel.html')
