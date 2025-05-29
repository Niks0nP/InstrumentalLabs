import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PyQt5 import QtCore, QtGui, QtWidgets

sender_email = "nikita.niko40@gmail.com"
sender_password = "tdnu tffp zovp efyb"

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(505, 500)

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(10, 410, 81, 31))
        self.pushButton.setObjectName("pushButton")

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 60, 111, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 100, 111, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(20, 150, 111, 31))
        self.label_3.setObjectName("label_3")

        self.lineEdit = QtWidgets.QLineEdit(Form)

        self.lineEdit.setGeometry(QtCore.QRect(140, 60, 171, 31))
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(140, 100, 171, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(140, 150, 281, 221))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Отправить"))
        self.label.setText(_translate("Form", "Адрес получателя"))
        self.label_2.setText(_translate("Form", "Тема"))
        self.label_3.setText(_translate("Form", "Текст отправки"))

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.send_email)

    def send_email(self):
        recipient = self.ui.lineEdit.text().strip()
        subject   = self.ui.lineEdit_2.text().strip()
        body      = self.ui.textEdit.toPlainText()

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"]   = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()

            server.login(sender_email, sender_password)

            server.sendmail(sender_email, [recipient], msg.as_string())
            server.quit()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
