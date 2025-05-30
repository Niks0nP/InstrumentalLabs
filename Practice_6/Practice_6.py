from PyQt5 import QtCore, QtGui, QtWidgets
import os

class TextEditor(QtWidgets.QWidget):
    def __init__(self):
        super(TextEditor, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.connect_events()

        self.add_font_sizes()

        self.current_file = None

    def connect_events(self):
        self.ui.pushButton.clicked.connect(self.open_file)

        self.ui.pushButton_2.clicked.connect(self.save_file)

        self.ui.pushButton_3.clicked.connect(self.close)

        self.ui.pushButton_4.clicked.connect(self.set_bold)

        self.ui.pushButton_5.clicked.connect(self.set_italic)

        self.ui.pushButton_6.clicked.connect(self.set_underline)

        self.ui.fontComboBox.currentFontChanged.connect(self.change_font)

        self.ui.comboBox.currentTextChanged.connect(self.change_font_size)
    def add_font_sizes(self):
        font_sizes = ['8', '9', '10', '11', '12', '14', '16', '18', '20', '22', '24', '26', '28', '36', '48', '72']
        self.ui.comboBox.addItems(font_sizes)
        self.ui.comboBox.setCurrentText('12')

    def open_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Mở tệp",
            "",
            "Text Files (*.txt);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    self.ui.plainTextEdit.setPlainText(text)
                    self.current_file = file_path
                    self.setWindowTitle(f"Text Editor - {os.path.basename(file_path)}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Lỗi", f"Không thể mở tệp: {str(e)}")

    def save_file(self):
        if self.current_file:
            self.save_to_file(self.current_file)
        else:
            self.save_as()

    def save_as(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            self.save_to_file(file_path)

    def save_to_file(self, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                text = self.ui.plainTextEdit.toPlainText()
                file.write(text)
                self.current_file = file_path
                self.setWindowTitle(f"Text Editor - {os.path.basename(file_path)}")
                QtWidgets.QMessageBox.information(self, "Log", "Saved")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Saving error: {str(e)}")

    def set_bold(self):
        cursor = self.ui.plainTextEdit.textCursor()
        char_format = cursor.charFormat()

        if char_format.fontWeight() == QtGui.QFont.Bold:
            char_format.setFontWeight(QtGui.QFont.Normal)
        else:
            char_format.setFontWeight(QtGui.QFont.Bold)

        cursor.mergeCharFormat(char_format)
        self.ui.plainTextEdit.setTextCursor(cursor)

    def set_italic(self):
        cursor = self.ui.plainTextEdit.textCursor()
        char_format = cursor.charFormat()

        char_format.setFontItalic(not char_format.fontItalic())

        cursor.mergeCharFormat(char_format)
        self.ui.plainTextEdit.setTextCursor(cursor)

    def set_underline(self):
        cursor = self.ui.plainTextEdit.textCursor()
        char_format = cursor.charFormat()

        char_format.setFontUnderline(not char_format.fontUnderline())

        cursor.mergeCharFormat(char_format)
        self.ui.plainTextEdit.setTextCursor(cursor)

    def change_font(self, font):
        cursor = self.ui.plainTextEdit.textCursor()
        char_format = cursor.charFormat()

        char_format.setFont(font)

        cursor.mergeCharFormat(char_format)
        self.ui.plainTextEdit.setTextCursor(cursor)

    def change_font_size(self, size_text):
        if not size_text:
            return

        cursor = self.ui.plainTextEdit.textCursor()
        char_format = cursor.charFormat()

        font = char_format.font()
        font.setPointSize(int(size_text))
        char_format.setFont(font)

        cursor.mergeCharFormat(char_format)
        self.ui.plainTextEdit.setTextCursor(cursor)


class Ui_Form():
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(796, 595)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(50, 30, 71, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 30, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(520, 30, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(60, 100, 21, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(110, 100, 21, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(150, 100, 21, 23))
        self.pushButton_6.setObjectName("pushButton_6")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(250, 100, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(510, 100, 47, 13))
        self.label_2.setObjectName("label_2")
        self.fontComboBox = QtWidgets.QFontComboBox(Form)
        self.fontComboBox.setGeometry(QtCore.QRect(290, 100, 187, 22))
        self.fontComboBox.setObjectName("fontComboBox")
        self.plainTextEdit = QtWidgets.QTextEdit(Form)
        self.plainTextEdit.setGeometry(QtCore.QRect(90, 190, 641, 351))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(550, 100, 69, 22))
        self.comboBox.setObjectName("comboBox")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Text Editor"))
        self.pushButton.setText(_translate("Form", "Open files"))
        self.pushButton_2.setText(_translate("Form", "SAVE"))
        self.pushButton_3.setText(_translate("Form", "EXIT"))
        self.pushButton_4.setText(_translate("Form", "B"))
        self.pushButton_5.setText(_translate("Form", "I"))
        self.pushButton_6.setText(_translate("Form", "U"))
        self.label.setText(_translate("Form", "FONT:"))
        self.label_2.setText(_translate("Form", "SIZE:"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())
