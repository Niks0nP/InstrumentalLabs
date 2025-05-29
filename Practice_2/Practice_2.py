import mimetypes
import os
import smtplib
import sys
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PyQt5 import QtCore, QtWidgets


def attach_file(msg, filepath):
    filename = os.path.basename(filepath)
    ctype, encoding = mimetypes.guess_type(filepath)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    if maintype == 'text':
        try:
            with open(filepath, 'r', encoding='utf-8') as fp:
                file_content = fp.read()
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='latin-1') as fp:
                file_content = fp.read()
        mime = MIMEText(file_content, _subtype=subtype, _charset='utf-8')
    elif maintype == 'image':
        with open(filepath, 'rb') as fp:
            mime = MIMEImage(fp.read(), _subtype=subtype)
    elif maintype == 'audio':
        with open(filepath, 'rb') as fp:
            mime = MIMEAudio(fp.read(), _subtype=subtype)
    else:
        with open(filepath, 'rb') as fp:
            mime = MIMEBase(maintype, subtype)
            mime.set_payload(fp.read())
        encoders.encode_base64(mime)
    mime.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(mime)


def process_attachments(msg, files):
    for f in files:
        f = f.strip()
        if f:
            if os.path.isfile(f):
                attach_file(msg, f)
            elif os.path.exists(f):
                for file in os.listdir(f):
                    full_path = os.path.join(f, file)
                    if os.path.isfile(full_path):
                        attach_file(msg, full_path)


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 714)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(10, 530, 90, 31))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 60, 130, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 290, 160, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 340, 130, 31))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(150, 290, 331, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(140, 60, 171, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(150, 340, 331, 241))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(20, 20, 130, 31))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(10, 150, 130, 16))
        self.label_5.setObjectName("label_5")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 150, 81, 21))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(10, 190, 130, 16))
        self.label_6.setObjectName("label_6")
        self.lineEdit_4 = QtWidgets.QLineEdit(Form)
        self.lineEdit_4.setGeometry(QtCore.QRect(150, 180, 331, 101))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(10, 100, 130, 31))
        self.label_7.setObjectName("label_7")
        self.lineEdit_5 = QtWidgets.QLineEdit(Form)
        self.lineEdit_5.setGeometry(QtCore.QRect(140, 110, 171, 31))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.comboBox = QtWidgets.QComboBox(Form)  # ComboBox chọn máy chủ
        self.comboBox.setGeometry(QtCore.QRect(140, 30, 151, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Email Sender"))
        self.pushButton.setText(_translate("Form", "Отправить"))
        self.label.setText(_translate("Form", "Адрес отправителя"))
        self.label_2.setText(_translate("Form", "Тема"))
        self.label.setText(_translate("Form", "Адрес отправителя"))
        self.label_2.setText(_translate("Form", "Тема"))
        self.label_3.setText(_translate("Form", "Текст отправки"))
        self.label_4.setText(_translate("Form", "Сервер"))
        self.label_5.setText(_translate("Form", "Выбрать Файл"))
        self.pushButton_2.setText(_translate("Form", "Открыть"))
        self.label_6.setText(_translate("Form", "Список файлов"))
        self.label_7.setText(_translate("Form", "Пароль"))
        self.comboBox.setItemText(0, _translate("Form", "Yandex"))
        self.comboBox.setItemText(1, _translate("Form", "Mail.ru"))
        self.comboBox.setItemText(2, _translate("Form", "Gmail"))

class EmailForm(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EmailForm, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.attachments = []

        self.ui.pushButton_2.clicked.connect(self.open_file)
        self.ui.pushButton.clicked.connect(self.send_email)

    def open_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Открыть файл", "", "All Files (*)")
        if file_path:
            self.attachments.append(file_path)
            current_text = self.ui.lineEdit_4.text()
            if current_text:
                current_text += ';' + file_path
            else:
                current_text = file_path
            self.ui.lineEdit_4.setText(current_text)

    def send_email(self):
        addr_from = self.ui.lineEdit_2.text().strip()
        password = self.ui.lineEdit_5.text().strip()
        subject = self.ui.lineEdit.text().strip()
        body = self.ui.lineEdit_3.text().strip()

        if not addr_from or not password or not subject or not body:
            QtWidgets.QMessageBox.warning(self, "Error", "Error")
            return

        addr_to, ok = QtWidgets.QInputDialog.getText(self, "Re-cipient", "Recipient")
        if not ok or not addr_to.strip():
            QtWidgets.QMessageBox.warning(self, "Error", "Empty field.")
            return

        index = self.ui.comboBox.currentIndex()
        try:
            if index == 0:
                server = smtplib.SMTP('smtp.yandex.ru', 587)
                server.starttls()
            elif index == 1:
                server = smtplib.SMTP('smtp.mail.ru', 587)
                server.starttls()
            elif index == 2:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Empty email.")
                return
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"SMTP connection error: {str(e)}")
            return

        msg = MIMEMultipart()
        msg['From'] = addr_from
        msg['To'] = addr_to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        file_list_text = self.ui.lineEdit_4.text().strip()
        if file_list_text:
            files = file_list_text.split(';')
            process_attachments(msg, files)

        try:
            server.login(addr_from, password)
            server.sendmail(addr_from, [addr_to], msg.as_string())
            server.quit()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = EmailForm()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
