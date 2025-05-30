from PyQt5 import QtCore, QtGui, QtWidgets
import re


class Calculator:
    def __init__(self):
        self.result = 0

    def calculate(self, expression):
        try:
            expression = expression.replace('^', '**')

            self._validate_expression(expression)

            self.result = eval(expression)
            return self.result
        except Exception as e:
            return f"Error: {str(e)}"

    def _validate_expression(self, expression):
        if re.search(r'[^0-9+\-*/().\s\^]', expression):
            raise ValueError("Expression error")

        if expression.count('(') != expression.count(')'):
            raise ValueError("Expression error")


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(552, 486)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(10, 50, 351, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 20, 121, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(380, 60, 91, 20))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(20, 100, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.resultLabel = QtWidgets.QLabel(Form)
        self.resultLabel.setGeometry(QtCore.QRect(480, 60, 150, 20))
        self.resultLabel.setObjectName("resultLabel")
        self.resultLabel.setText("")

        self.pushButton.clicked.connect(self.calculate)

        self.calculator = Calculator()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Calculator"))
        self.label_2.setText(_translate("Form", "Result:"))
        self.pushButton.setText(_translate("Form", "Calculate"))

    def calculate(self):
        expression = self.lineEdit.text()
        if not expression:
            self.resultLabel.setText("Enter expression")
            return

        result = self.calculator.calculate(expression)
        self.resultLabel.setText(str(result))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
