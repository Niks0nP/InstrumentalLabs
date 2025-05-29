from flask import Flask, request
from waitress import serve
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        addr_from = request.form['from']
        password = request.form['password']
        addr_to = request.form['to']
        msg_subj = request.form['subject']
        msg_text = request.form['text']
        smtp_server = request.form['smtp_server']
        smtp_port = int(request.form['smtp_port'])

        print(addr_from, password, addr_to, msg_subj, msg_text, smtp_server, smtp_port)

        result = send_email(addr_from, password, addr_to, msg_subj, msg_text, smtp_server, smtp_port)

        return result
    else:
        return '''
        <html>
            <head>
                <title>Практика 4</title>
            </head>
            <body>
                <h1>Практика 4</h1>
                <form method="POST">
                    <p>Почта отправителя: <input type="text" name="from"></p>
                    <p>Пароль: <input type="password" name="password"></p>
                    <p>Почта получателя: <input type="text" name="to"></p>
                    <p>Тема: <input type="text" name="subject"></p>
                    <p>SMTP Сервер: <input type="text" name="smtp_server" value="smtp.gmail.com"></p>
                    <p>SMTP Порт: <input type="number" name="smtp_port" value="587"></p>
                    <p>Сообщение:<br><textarea name="text" rows="10" cols="50"></textarea></p>
                    <p><input type="submit" val-ue="Отправить"></p>
                </form>
            </body>
        </html>
        '''


def send_email(addr_from, password, addr_to, msg_subj, msg_text, smtp_server, smtp_port):
    msg = MIMEMultipart()
    msg["From"] = addr_from
    msg["To"] = addr_to
    msg["Subject"] = msg_subj
    msg.attach(MIMEText(msg_text, "plain"))
    try:
        msg = MIMEMultipart()
        msg['From'] = addr_from
        msg['To'] = addr_to
        msg['Subject'] = Header(msg_subj, 'utf-8')
        msg.attach(MIMEText(msg_text, 'plain', 'utf-8'))
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(addr_from, password)
        server.sendmail(addr_from, [addr_to], msg.as_string())
        server.quit()

        return "Email успешно отправлен!"
    except Exception as e:
        return f"Ошибка при отправке email: {str(e)}"


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=1516)
