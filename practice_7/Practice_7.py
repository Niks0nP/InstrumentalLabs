from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
import sys
import os
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(537, 540)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(20, 50, 101, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(140, 50, 61, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(220, 50, 81, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(330, 50, 81, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(10, 80, 501, 41))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 140, 61, 16))
        self.label.setObjectName("label")
        self.textEdit_2 = QtWidgets.QTextEdit(Form)
        self.textEdit_2.setGeometry(QtCore.QRect(10, 160, 501, 341))
        self.textEdit_2.setObjectName("textEdit_2")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Connect"))
        self.pushButton_2.setText(_translate("Form", "Query"))
        self.pushButton_3.setText(_translate("Form", "Close con-nection"))
        self.pushButton_4.setText(_translate("Form", "Delete"))
        self.label.setText(_translate("Form", "Results:"))



class DatabaseApp(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = None
        self.connection_name = "qt_sql_default_connection"

        self.pushButton.clicked.connect(self.connect_to_db)
        self.pushButton_2.clicked.connect(self.execute_query)
        self.pushButton_3.clicked.connect(self.close_db)
        self.pushButton_4.clicked.connect(self.delete_record)

        self.textEdit.setText("SELECT * FROM table_name")

    def connect_to_db(self):
        try:
            if self.db and self.db.isOpen():
                self.db.close()
                QSqlDatabase.removeDatabase(self.connection_name)

            self.db = QSqlDatabase.addDatabase("QPSQL", self.connection_name)
            self.db.setHostName("localhost")
            self.db.setDatabaseName("postgres")
            self.db.setUserName("postgres")
            self.db.setPassword("2413")
            self.db.setPort(5432)

            if not self.db.open():
                self.textEdit_2.setText(self.db.lastError().text())
                return
            query = QSqlQuery(self.db)
            query.exec("SELECT table_name FROM infor-mation_schema.tables WHERE table_schema='public'")

            tables = []
            while query.next():
                tables.append(query.value(0))

            self.textEdit_2.setText(
                f"Connected.\nTables: {', '.join(tables)}")

        except Exception as e:
            self.textEdit_2.setText(str(e))

    def execute_query(self):
        if not self.db or not self.db.isOpen():
            self.textEdit_2.setText("No connection.")
            return

        sql_query = self.textEdit.toPlainText().strip()
        if not sql_query:
            self.textEdit_2.setText("Input query.")
            return

        try:
            query = QSqlQuery(self.db)
            if not query.exec(sql_query):
                self.textEdit_2.setText(f"Query error: {query.lastError().text()}")
                return

            if sql_query.upper().startswith("SELECT"):
                result = []
                header = []

                record = query.record()
                for i in range(record.count()):
                    header.append(record.fieldName(i))

                result.append("\t".join(header))
                result.append("-" * 80)

                while query.next():
                    row = []
                    for i in range(record.count()):
                        row.append(str(query.value(i)))
                    result.append("\t".join(row))

                self.textEdit_2.setText("\n".join(result))
            else:
                self.textEdit_2.setText(
                    query.numRowsAffected())

        except Exception as e:
            self.textEdit_2.setText(str(e))

    def close_db(self):
        if self.db and self.db.isOpen():
            self.db.close()
            QSqlDatabase.removeDatabase(self.connection_name)
            self.textEdit_2.setText("Closed connection.")
        else:
            self.textEdit_2.setText("No connection to close.")

    def delete_record(self):
        if not self.db or not self.db.isOpen():
            self.textEdit_2.setText("No connection.")
            return

        try:
            table_name, ok = QtWidgets.QInputDialog.getText(self, "Deletion", "Enter table name:")
            if not ok or not table_name:
                return

            condition, ok = QtWidgets.QInputDialog.getText(self, "Deletion",
                                                           "Enter deletion condition")
            if not ok:
                return

            sql_query = f"DELETE FROM {table_name}"
            if condition:
                sql_query += f" WHERE {condition}"

            reply = QtWidgets.QMessageBox.question(self, "Confirm deletion",
                                                   f"Confirm de-letion: {sql_query}?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                query = QSqlQuery(self.db)
                if not query.exec(sql_query):
                    self.textEdit_2.setText(f"Deletion error: {query.lastError().text()}")
                else:
                    self.textEdit_2.setText(f"Deleted {query.numRowsAffected()}")

        except Exception as e:
            self.textEdit_2.setText(str(e))

    def closeEvent(self, event):
        if self.db and self.db.isOpen():
            self.db.close()
            QSqlDatabase.removeDatabase(self.connection_name)
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DatabaseApp()
    window.show()
    sys.exit(app.exec_())
