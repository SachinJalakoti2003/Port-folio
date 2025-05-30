from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'supersecretkey')

# Flask-Mail configuration (update with your email credentials in .env)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resume')
def view_resume():
    return render_template('resume_viewer.html')

@app.route('/download_resume')
def download_resume():
    return send_from_directory('Profile', 'SachinJalakoti_Resume.pdf', as_attachment=True)

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    if not name or not email or not message:
        flash('Please fill in all fields.', 'danger')
        return redirect(url_for('index') + '#contact')
    try:
        msg = Message(f'Portfolio Contact: {name}',
                      sender=email,
                      recipients=[os.getenv('MAIL_RECEIVER', app.config['MAIL_USERNAME'])])
        msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        mail.send(msg)
        flash('Your message has been sent successfully!', 'success')
    except Exception as e:
        flash('An error occurred while sending your message. Please try again later.', 'danger')
    return redirect(url_for('index') + '#contact')

if __name__ == '__main__':
    app.run(debug=True) 