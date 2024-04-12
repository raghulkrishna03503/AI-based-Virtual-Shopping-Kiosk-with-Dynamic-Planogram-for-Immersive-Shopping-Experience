from email.mime.text import MIMEText
import razorpay
from flask import Flask, render_template, redirect, request
import firebase_admin
from firebase_admin import db, credentials
import smtplib
from email.mime.multipart import MIMEMultipart
from datetime import datetime


# def create_bill(data):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)

#     # Add content to the PDF
#     pdf.cell(200, 10, txt="SSN SUPERMARKET", ln=True, align='C')
#     pdf.ln(10)
#     for key, value in data.items():
#         if key == 'address':
#             pdf.cell(200, 10, txt=f"Address: {value}", ln=True, align='L')
#         elif key == 'productList':
#             pdf.cell(200, 10, txt="Product List:", ln=True, align='L')
#             products = value.split('\n')
#             for product in products:
#                 pdf.cell(200, 10, txt=product, ln=True, align='L')
#         else:
#             pdf.cell(200, 10, txt=f"{key}: {value}", ln=True, align='L')

#     # Save the PDF file with executable and writable permissions
#     pdf_filename = "bill.pdf"
#     pdf.output(pdf_filename)

#     # Return the PDF filename
#     return pdf_filename


def send_email_with_data(data, recipient_email):
    # Email content
    subject = "Your Bill from SSN SUPERMARKET"
    body = f"Thank you for shopping with us!\n\n"
    body += f"Customer Name: {data['customer_name']}\n"
    body += f"Customer Mobile: {data['customer_mobile']}\n"
    body += f"Customer Email: {data['customer_email']}\n"
    body += f"Customer Address:\n{data['customer_address']}\n\n"
    body += f"Order ID: {data['ordid']}\n"
    body += f"Payment ID: {data['pid']}\n"
    body += f"Products Purchased:\n{data['productList']}\n"
    body += f"Total Amount Paid: {data['total']}\n"
    body += f"Date and Time: {data['amount_paid']}\n"

    # Email setup
    sender_email = "rkocfb@gmail.com"
    password = "nmgzuntvhnrryfzv"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", str(e))


app = Flask(__name__)
client = razorpay.Client(auth=("rzp_test_eGzRpH4AIisrk8", "2K7xULDD1JHAV5xELjVZzTEn"))

cred = credentials.Certificate("vrsupermarket-f6ccc-firebase-adminsdk-is6xr-0ba53a941e.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://vrsupermarket-f6ccc-default-rtdb.asia-southeast1.firebasedatabase.app/"})

orderIDList = []

@app.route('/')
def func_name():
    return """
    <form action="/pay" method="post">
        <center>
            <p style="font-size: 50px; margin-top: 250px;">Enter the Amount you need to pay!!!</p>
            <input type="number" name="amt" id="" style="font-size: 50px;">
            <button type="submit" style="font-size: 50px;">Pay</button>
        </center>
    </form>
    """

@app.route('/pay/<orderID>', methods=["GET", "POST"])
def pay(orderID):
    orderIDList.append(orderID)
    print(orderIDList)
    ref = db.reference("receipts/" + orderID + "/" + "total/")
    amount = round(ref.get(), 2)
    data = {"amount": amount * 100, "currency": "INR", "receipt": "order_rcptid_11"}
    payment = client.order.create(data=data)
    pdata = [amount, payment["id"]]
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Payment Page</title>
    </head>
    <body>
        <center>
            <button id="rzp-button1" style="font-size: 50px; margin-top: 250px;">Pay with Razorpay</button>
        </center>
        <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
        <script>
            var options = {
                "key": "rzp_test_eGzRpH4AIisrk8", // Enter the Key ID generated from the Dashboard
                "amount": """ + str(pdata[0]) + """, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                "currency": "INR",
                "name": "SSN Supermarket",
                "description": "Test Transaction",
                "image": "https://example.com/your_logo",
                "order_id": '""" + str(pdata[1]) + """',
                "callback_url": "/success",
                "prefill": {
                    "name": "Raghul Yadhav K",
                    "email": "raghulkrishna03052003@gmail.com",
                    "contact": "8015023475"
                },
                "notes": {
                    "address": "Razorpay Corporate Office"
                },
                "theme": {
                    "color": "#5cffab"
                }
            };
            var rzp1 = new Razorpay(options);
            document.getElementById('rzp-button1').onclick = function(e){
                rzp1.open();
                e.preventDefault();
            }
        </script>
    </body>
    </html>
    """
    return html_code


@app.route("/thankyou")
def thankyou():
    return "<center><p style=\"font-size: 50px; margin-top: 250px;\">Thank you for shopping with us. Your Receipt is sent to your Whatsapp Number. You can exit the browser now!!!</p></center>"

@app.route('/success', methods=["POST"])
def success():
    pid = request.form.get("razorpay_payment_id")
    ordid = request.form.get("razorpay_order_id")
    sign = request.form.get("razorpay_signature")
    print(f"The payment id : {pid}, order id : {ordid} and signature : {sign}")
    ref = db.reference("receipts/" + orderIDList[0] + "/" + "isPaid/")
    ref.set(True)
    ref = db.reference("receipts/" + orderIDList[0] + "/" + "ordid/")
    ref.set(ordid)
    ref = db.reference("receipts/" + orderIDList[0] + "/" + "pid/")
    ref.set(pid)
    ref = db.reference("receipts/" + orderIDList[0] + "/" + "sign/")
    ref.set(sign)
    params = {
        'razorpay_order_id': ordid,
        'razorpay_payment_id': pid,
        'razorpay_signature': sign
    }
    final = client.utility.verify_payment_signature(params)
    if final:
        data = {}
        ref = db.reference("receipts/" + orderIDList[0] + "/" + "address")
        address = ref.get().split('_')
        contact = address[1].split(',')
        address = address[0].split(',')
        for i in range(len(address)):
            address[i] = address[i].strip('\u200b').strip().upper()
        
        customer_name = contact[0].strip('\u200b').upper()
        customer_mobile = contact[1].strip('\u200b').strip()
        customer_email = contact[2].strip('\u200b')
        customer_address = "\n".join(address)

        now = datetime.now()

        data['customer_name'] = customer_name
        data['customer_mobile'] = customer_mobile
        data['customer_email'] = customer_email
        data['customer_address'] = customer_address
        data['amount_paid'] = now.strftime("%d/%m/%Y %H:%M:%S")

        ref = db.reference("receipts/" + orderIDList[0] + "/" + "ordid")
        data['ordid'] = ref.get()
        ref = db.reference("receipts/" + orderIDList[0] + "/" + "pid")
        data['pid'] = ref.get()
        ref = db.reference("receipts/" + orderIDList[0] + "/" + "productList")
        data['productList'] = ref.get()
        ref = db.reference("receipts/" + orderIDList[0] + "/" + "total")
        data['total'] = ref.get()
        # create_bill(data)
        send_email_with_data(data, customer_email)
        orderIDList.clear()
        return redirect("/thankyou", code=301)
    return "Something Went Wrong Please Try Again"

if __name__ == "__main__":
    app.run(debug=True)
