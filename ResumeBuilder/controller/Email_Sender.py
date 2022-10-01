import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def Sender(subject, receiver_email, role, content):
    sender_email = "services.propad@gmail.com"
    receiver_email = receiver_email
    password = "Propad@1234"

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    # text = """\
    # Hi Dear,
    # Welcome to Resume Builder..!!
    # The Best Resume Building Online Portal:
    # www.resumebuilder.in"""
    #

    before_role = """
                <html>
                    <head>
                        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
                    </head>
                    <body style="align-items:center;text-align:center;">
                        <div style="background-image: linear-gradient(aqua, aquamarine);width:50%;margin:auto;border:5px solid aqua;">
                            <b><p>Hi Dear,<br>
                               Welcome to <a href="http://www.resumebuilder.in">Resume Builder</a>..!!<br>
                               The Simple and Easy to make Resume Online.
                            </p></b>
                """

    html = ""
    if role == "evs":
            html = before_role+"""\
                        <h3>Please Verify Your Email By Clicking</h3>
                        <a href=""" + content + """><button style="font-size:25px; padding: 10px;border:5px solid aqua;border-radius:25px;">Verify Email</button></a><br>
                """
    elif role == "fg":
            html = before_role+"""\
                        <h3>You are Requested for Resume Builder Password<br>Your Password is : </h3>
                        <button style="font-size:25px; padding: 10px;border:5px solid aqua;border-radius:25px;">""" + content + """</button><br> 
                """
    # Turn these into plain/html MIMEText objects
    # part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    # message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
# Sender("Email Verification", "dhobaleprasad33@Gmail.com", "e_verification", "http://localhost:8000/verification?id=101&token=47989")
