import sys
import smtplib
import csv
import os
import mimetypes
from PyQt5 import QtCore, QtGui, QtWidgets
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email import encoders
from email.header import Header


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(587, 571)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(10, 520, 81, 31))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 60, 111, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 200, 111, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 250, 111, 31))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(150, 200, 331, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(140, 60, 171, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(150, 250, 331, 241))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(20, 20, 111, 31))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(10, 150, 101, 16))
        self.label_5.setObjectName("label_5")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 150, 81, 21))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(10, 100, 111, 31))
        self.label_7.setObjectName("label_7")
        self.lineEdit_5 = QtWidgets.QLineEdit(Form)
        self.lineEdit_5.setGeometry(QtCore.QRect(140, 110, 171, 31))
        self.lineEdit_5.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(140, 30, 151, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.statusLabel = QtWidgets.QLabel(Form)
        self.statusLabel.setGeometry(QtCore.QRect(100, 520, 400, 31))
        self.statusLabel.setText("")
        self.statusLabel.setObjectName("statusLabel")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Email Sender"))
        self.pushButton.setText(_translate("Form", "Отправить"))
        self.label.setText(_translate("Form", "Адрес отправиттеля"))
        self.label_2.setText(_translate("Form", "Тема"))
        self.label_3.setText(_translate("Form", "Текст отправки"))
        self.label_4.setText(_translate("Form", "Сервер"))
        self.label_5.setText(_translate("Form", "Выбрать CSV Файл"))
        self.pushButton_2.setText(_translate("Form", "Открыть"))
        self.label_7.setText(_translate("Form", "Пароль"))
        self.comboBox.setItemText(0, _translate("Form", "Yandex"))
        self.comboBox.setItemText(1, _translate("Form", "Mail"))
        self.comboBox.setItemText(2, _translate("Form", "Gmail"))


class EmailSender(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.csv_path = ""

        self.ui.pushButton.clicked.connect(self.send_emails)
        self.ui.pushButton_2.clicked.connect(self.open_csv_file)

    def open_csv_file(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Выбрать CSV файл", "",
            "CSV Files (*.csv);;All Files (*)", options=options)

        if fileName:
            self.csv_path = fileName
            self.ui.statusLabel.setText(f"Выбран файл: {os.path.basename(fileName)}")

    def send_emails(self):
        if not self.csv_path:
            self.ui.statusLabel.setText("Ошибка: CSV файл не выбран")
            return

        addr_from = self.ui.lineEdit_2.text()
        password = self.ui.lineEdit_5.text()
        subject = self.ui.lineEdit.text()
        message = self.ui.lineEdit_3.text()

        if not addr_from or not password or not subject or not message:
            self.ui.statusLabel.setText("Ошибка: Заполните все поля")
            return

        server_type = self.ui.comboBox.currentText()

        try:


            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=';')

                with open("send.txt", "a", encoding='utf-8') as log_file:

                    for row in reader:
                        if len(row) < 1:
                            continue

                        addr_to = row[0].strip()

                        files = [file.strip().strip("'").strip('"') for file in row[1:] if file.strip()]


                        try:
                            self.send_email(server_type, addr_from, password, addr_to, subject, message, files)

                            log_file.write(f"\nEmail {addr_to}; тема: {subject}; сообщение: {message}\n")

                            self.ui.statusLabel.setText(f"Письмо отправлено: {addr_to}")
                        except Exception as e:
                            self.ui.statusLabel.setText(f"Ошибка при отправке {addr_to}: {str(e)}")

            self.ui.statusLabel.setText("Все письма отправлены")
        except Exception as e:
            self.ui.statusLabel.setText(f"Ошибка: {str(e)}")

    def send_email(self, server_type, addr_from, password, addr_to, subject, message, files):
        msg = MIMEMultipart()
        msg['From'] = addr_from
        msg['To'] = addr_to
        msg['Subject'] = Header(subject, 'utf-8')

        msg.attach(MIMEText(message, 'plain', 'utf-8'))

        self.process_attachement(msg, [r"C:\Users\nikit\PyCharmMiscProject\Practice_3\my_file.csv"])

        if server_type == "Yandex":
            server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
        elif server_type == "Mail":
            server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        elif server_type == "Gmail":
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
        else:
            raise ValueError("Неизвестный тип сервера")

        server.login(addr_from, password)

        server.send_message(msg)

        server.quit()

    def process_attachement(self, msg, files):
        for f in files:
            f = os.path.normpath(f)  # Fix path format
            if os.path.isfile(f):
                self.attach_file(msg, f)
            elif os.path.exists(f):
                for file in os.listdir(f):
                    self.attach_file(msg, os.path.join(f, file))
        print(f"Attachments: {files}")
        for f in files:
            print(f"Checking file: {f} -> Exists: {os.path.exists(f)}")

    def attach_file(self, msg, filepath):
        filename = os.path.basename(filepath)
        ctype, encoding = mimetypes.guess_type(filepath)

        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'

        maintype, subtype = ctype.split('/', 1)

        with open(filepath, 'rb') as fp:
            if maintype == 'text':
                file = MIMEText(fp.read().decode('utf-8', errors='ignore'), _subtype=subtype)
            elif maintype == 'image':
                file = MIMEImage(fp.read(), _subtype=subtype)
            elif maintype == 'audio':
                file = MIMEAudio(fp.read(), _subtype=subtype)
            else:
                file = MIMEBase(maintype, subtype)
                file.set_payload(fp.read())
                encoders.encode_base64(file)

        file.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(file)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = EmailSender()
    window.show()
    sys.exit(app.exec_())
