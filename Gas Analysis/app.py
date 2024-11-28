from flask import Flask, render_template, request, send_file
import smtplib
from email.message import EmailMessage
from gas_analysis import analyze_gas
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)

# Data simulation for gas and sensor values
gas_data = {"CO2": 400, "NH3": 30, "NOx": 50}  # Simulated gas levels (ppm)
temperature = 25  # Simulated temperature (°C)
humidity = 60  # Simulated humidity (%)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/analyze', methods=['POST'])
def analyze():
    # Simulate gas analysis
    results = analyze_gas(gas_data)
    future_impact = {
        "CO2": "Contributes to global warming and respiratory issues.",
        "NH3": "Can cause irritation to eyes and throat.",
        "NOx": "Leads to acid rain and respiratory problems.",
    }
    return render_template("report.html", gas_data=gas_data, results=results, temperature=temperature, 
                           humidity=humidity, future_impact=future_impact)


@app.route('/download', methods=['POST'])
def download_report():
    results = analyze_gas(gas_data)
    file_path = "gas_report.pdf"
    
    # Generate PDF
    pdf = canvas.Canvas(file_path)
    pdf.drawString(100, 800, "Gas Detection Report")
    pdf.drawString(100, 780, f"Temperature: {temperature} °C")
    pdf.drawString(100, 760, f"Humidity: {humidity} %")
    pdf.drawString(100, 740, "Detected Gas Levels:")
    
    y = 720
    for gas, level in gas_data.items():
        pdf.drawString(120, y, f"{gas}: {level} ppm")
        y -= 20
    
    pdf.drawString(100, y, "Predictions:")
    y -= 20
    for gas, prediction in results.items():
        pdf.drawString(120, y, f"{gas}: {prediction}")
        y -= 20
    
    pdf.save()
    return send_file(file_path, as_attachment=True)


@app.route('/send-email', methods=['POST'])
def send_email():
    user_email = request.form['email']
    subject = "Gas Detection Report"
    body = "Attached is the gas detection report for your review."
    file_path = "gas_report.pdf"

    # Email setup
    email = EmailMessage()
    email['Subject'] = subject
    email['From'] = "your_email@gmail.com"
    email['To'] = user_email
    email.set_content(body)

    with open(file_path, 'rb') as f:
        email.add_attachment(f.read(), maintype='application', subtype='pdf', filename=file_path)
    
    # Sending email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("your_email@gmail.com", "your_email_password")
        smtp.send_message(email)
    
    return "Email sent successfully!"


if __name__ == "__main__":
    app.run(debug=True)
