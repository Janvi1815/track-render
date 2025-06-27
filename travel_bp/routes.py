from flask import Blueprint, render_template, request
import pymysql
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

main = Blueprint('main', __name__)

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='travel_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def send_email_to_owner(name, email, phone, month, days, travellers, details):
    sender_email = "bhattjanvi152@gmail.com"  # 🔁 Your Gmail
    receiver_emails = [
        "bhattjanvi152@gmail.com"              # ✅ Your own Gmail (can add more if needed)
    ]
    password = "your_app_password"             # 🔁 Replace with Gmail App Password

    subject = f"New Travel Inquiry from {name}"
    body = f"""
📩 New Travel Inquiry

Name: {name}
Email: {email}
Phone: {phone}
Month of Travel: {month}
Number of Days: {days}
Travellers: {travellers}
Details: {details}
"""

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_emails, msg.as_string())
        server.quit()
        print("✅ Email sent to owner")
    except Exception as e:
        print("❌ Email error:", e)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/custom')
def custom():
    return render_template('custom.html')

@main.route('/travel')
def travel_blog():
    return render_template('travel.html')

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

        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO contact_form (name, email, phone, month, days, travellers, details)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (name, email, phone, month, days, travellers, details))
                conn.commit()
        except Exception as e:
            print("❌ DB Error:", e)
        finally:
            conn.close()

        # ✅ Send email to owner
        send_email_to_owner(name, email, phone, month, days, travellers, details)

        return render_template('contact.html', success=True)

    return render_template('contact.html')

@main.route('/admin-data')
def admin_data():
    submissions = []
    headers = ['Name', 'Email', 'Phone', 'Month', 'Days', 'Travellers', 'Details']

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT name, email, phone, month, days, travellers, details FROM contact_form")
            submissions = cursor.fetchall()
    except Exception as e:
        print("❌ Error reading DB:", e)
    finally:
        conn.close()

    return render_template('admin-data.html', headers=headers, submissions=submissions)
