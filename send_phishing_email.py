#!/usr/bin/env python3
# Script to simulate sending a phishing email with a malicious PDF attachment

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

def send_phishing_email(target_email):
    # For simulation purposes only - in a real test environment, 
    # you would use a controlled mail server
    
    # This simulates what the email would look like
    # In your controlled lab, you would deliver this directly to the victim machine
    
    # Email content
    subject = "URGENT: Banking Security Update Required"
    from_email = "security@secure-banking-system.com"
    
    html_content = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333; }
            .header { color: #004080; border-bottom: 1px solid #004080; padding-bottom: 10px; }
            .footer { font-size: 12px; color: #666; border-top: 1px solid #ccc; margin-top: 30px; padding-top: 10px; }
            .important { color: #cc0000; font-weight: bold; }
        </style>
    </head>
    <body>
        <h2 class="header">URGENT: Banking Security Update Required</h2>
        
        <p>Dear Valued Customer,</p>
        
        <p>Our security team has detected that your banking application requires an <span class="important">immediate security update</span> to protect against a new wave of cyber threats targeting financial institutions.</p>
        
        <p class="important">This update is MANDATORY and must be installed by March 20, 2025.</p>
        
        <p>The security update addresses the following vulnerabilities:</p>
        <ul>
            <li>Critical vulnerability in transaction processing</li>
            <li>Potential data exposure in customer records</li>
            <li>Authentication bypass in certain account operations</li>
        </ul>
        
        <p><strong>Installation Instructions:</strong></p>
        <p>Please open the attached PDF document and follow the instructions to install this critical security update.</p>
        
        <p>If you have any questions, please contact our support team at support@secure-banking-system.com.</p>
        
        <p>Thank you for your cooperation,</p>
        <p>Banking Security Operations Team</p>
        
        <div class="footer">
            <p>This is an automated security notification. Please do not reply to this email.</p>
            <p>© 2025 Secure Banking System. All rights reserved.</p>
        </div>
    </body>
    </html>
    """
    
    # Create message container
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = target_email
    msg['Subject'] = subject
    
    # Attach HTML content
    msg.attach(MIMEText(html_content, 'html'))
    
    # Attach PDF
    with open("Security_Update_2025.pdf", "rb") as pdf_file:
        pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
        pdf_attachment.add_header('Content-Disposition', 'attachment', filename="Security_Update_2025.pdf")
        msg.attach(pdf_attachment)
    
    # Output the email content to a file (for simulation)
    with open("phishing_email_content.html", "w") as email_file:
        email_file.write(html_content)
    
    print(f"Email would be sent to: {target_email}")
    print(f"Subject: {subject}")
    print("Attachment: Security_Update_2025.pdf")
    print("Email content saved to: phishing_email_content.html")
    print("\nNOTE: In a real environment, this would connect to an SMTP server")
    print("      For your forensic exercise, manually deliver these files to the victim VM")

if __name__ == "__main__":
    target_email = "johntravolt2025@outlook.com"
    send_phishing_email(target_email)
