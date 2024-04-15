import smtplib
import csv
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time

def send_certificate(participant_email, certificate_file):
    # Email configurations
    sender_email = "<yourgmail>"
    sender_password = "<app_password>"
    smtp_server = "smtp.gmail.com"

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = participant_email
    msg['Subject'] = "Certificate of Participation"

    # Attach message body
    body = """
        html code here
    """
    msg.attach(MIMEText(body, 'html'))

    # Attach certificate
    attachment = open(certificate_file, "rb")
    certificate = MIMEBase('application', 'octet-stream')
    certificate.set_payload((attachment).read())
    encoders.encode_base64(certificate)
    certificate.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(certificate_file))
    msg.attach(certificate)

    try:
        # Connect to SMTP server and send email
        server = smtplib.SMTP(smtp_server, 587)  # Update port accordingly
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, participant_email, text)
        print(f"Certificate sent to {participant_email}")
    except Exception as e:
        print(f"Error sending certificate to {participant_email}: {e}")
    finally:
        server.quit()  # Close the connection

# Read participant emails from CSV
def read_participant_emails(csv_file):
    participants = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            participants.append({"email": row[0], "id": row[1]})  # Assuming email is in the first column and participant ID is in the second column
    return participants

# Example usage
csv_file = "test.csv"  # Update with your CSV file path
certificates_folder = "test"  # Update with the folder containing certificates

participants = read_participant_emails(csv_file)
for participant in participants:
    certificate_id = participant["id"]
    certificate_file = os.path.join(certificates_folder, f"{certificate_id}.png")
    if os.path.exists(certificate_file):
        send_certificate(participant["email"], certificate_file)
        print(f"Certificate sent to {participant['email']}")
        time.sleep(5)
    else:
        print(f"Certificate not found for participant {participant['email']}")
