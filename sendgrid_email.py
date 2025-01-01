import os
from sendgrid import SendGridAPIClient, Attachment, FileContent, FileType, FileName, Disposition
from sendgrid.helpers.mail import Mail


def send_email(send_to, pdf_data):
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
            <p>přiletělo tvoje Demvis Menu! <br> Věřím, že ti přijde vhod a splní tvá očekávání.</p>
            <p>Pokud budeš mít jakékoliv otázky nebo potřebuješ další informace, neváhej se ozvat. Ráda ti pomůžu!</p>
            <p>Měj se krásně a dobrou chuť!</p>
            <p>S pozdravem,<br>Sandra</p>
        </div>
    </body>
    </html>
    """
    send_from = "info.demvis@gmail.com"

    message = Mail(
        from_email=send_from,
        to_emails=send_to,
        subject='Vaše menu',
        html_content=html_content
    )
    attachment = Attachment(
        FileContent(pdf_data),
        FileName("menu.pdf"),  # Adjust the file name
        FileType("application/pdf"),
        Disposition("attachment")
    )

    message.attachment = attachment

    try:
        sg = SendGridAPIClient(os.environ.get('sendgrid_api_key'))
        response = sg.send(message)
    except Exception as e:
        print(f"Error sending email: {e}")
