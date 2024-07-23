import os
from email.message import EmailMessage
import smtplib


def send_email(send_to, pdf_data):
    text_content = """Ahoj,
    přiletělo tvoje Demvis Menu!
    Věřím, že ti přijde vhod a splní tvá očekávání.

    Pokud budeš mít jakékoliv otázky nebo potřebuješ další informace, neváhej se ozvat.
    Ráda ti pomůžu!

    Měj se krásně a dobrou chuť! A nezapoměň se pochlubit kámoškám (mrk, mrk).

    S pozdravem,
    Sandra
    """

    html_content = """<!DOCTYPE html>
    <html lang="cs">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Demvis Menu</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                color: #333;
                margin: 0;
                padding: 20px;
            }
            .container {
                background-color: #fff;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #ff6600;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Ahoj,</h1>
            <p>přiletělo tvoje Demvis Menu! </br> Věřím, že ti přijde vhod a splní tvá očekávání.</p>
            <p>Pokud budeš mít jakékoliv otázky nebo potřebuješ další informace, neváhej se ozvat. Ráda ti pomůžu!</p>
            <p>Měj se krásně a dobrou chuť! A nezapoměň se pochlubit kámoškám (mrk, mrk).</p>
            <p>S pozdravem,<br>Sandra</p>
        </div>
    </body>
    </html>
    """

    email_password = os.environ.get("DEMVIS_SMTPLIB")
    send_from = "info.demvis@gmail.com"
    msg = EmailMessage()
    msg["From"] = send_from
    msg["Subject"] = "Vaše Menu"
    msg["To"] = send_to
    msg.set_content(text_content)
    msg.add_alternative(html_content, subtype="html")

    msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename="demvis_menu.pdf")

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=send_from, password=email_password)
        connection.send_message(msg)
