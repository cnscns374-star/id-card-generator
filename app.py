import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import date
import smtplib
from email.message import EmailMessage
from reportlab.lib.utils import ImageReader

st.set_page_config(page_title="I Card Generator")

st.title("🪪 Online I-Card Generator")

# ---------- DOB RANGE ----------
today = date.today()
min_date = date(1901, 1, 1)

# ---------- FORM ----------
name = st.text_input("Enter Full Name")
address = st.text_area("Enter Address")
blood = st.text_input("Blood Group")

dob = st.date_input(
    "Select Date of Birth",
    min_value=min_date,
    max_value=today,
    value=date(2000, 1, 1)
)

email = st.text_input("Enter Email ID")

photo = st.file_uploader("Upload Photo", type=["jpg", "png", "jpeg"])

# ---------- BUTTON ----------
if st.button("Generate ID Card & Send Email"):

    if name and address and blood and email and photo:

        pdf_file = "id_card.pdf"

        # ---------- CREATE PDF ----------
        c = canvas.Canvas(pdf_file, pagesize=A4)

        c.setFont("Helvetica-Bold", 18)
        c.drawString(200, 800, "EMPLOYEE ID CARD")

        c.setFont("Helvetica", 12)
        c.drawString(80, 700, f"Name: {name}")
        c.drawString(80, 670, f"Address: {address}")
        c.drawString(80, 640, f"Blood Group: {blood}")
        c.drawString(80, 610, f"DOB: {dob.strftime('%d-%m-%Y')}")

        # ---------- PHOTO ----------
        image = ImageReader(photo)
        c.drawImage(image, 400, 640, width=120, height=140)

        c.save()

        # ---------- EMAIL SENDING ----------
        try:
            sender_email = "cnscns374@gmail.com"
            sender_password = "tnbe gaos pvzh iwct"

            msg = EmailMessage()
            msg["Subject"] = "Your I-Card"
            msg["From"] = sender_email
            msg["To"] = email
            msg.set_content("Dear User,\n\nYour ID Card is attached.\n\nRegards")

            with open(pdf_file, "rb") as f:
                msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="ID_Card.pdf")

            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()

            st.success("✅ ID Card Generated & Sent to Email Successfully!")

            # download button
            with open(pdf_file, "rb") as f:
                st.download_button("Download ID Card", f, file_name="ID_Card.pdf")

        except Exception as e:
            st.error(f"Email failed: {e}")

    else:
        st.warning("⚠ Please fill all fields and upload photo")
