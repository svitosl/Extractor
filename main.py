from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QHeaderView

from main_wnd import Ui_MainWindow

import re
import sys
import analysis
import marker
import my_errors

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.mark = marker.MyMarker()
        self.ui.btn_extract.clicked.connect(self.btnClicked)
        self.ui.btn_keywrd.clicked.connect(self.btn2Clicked)
        self.ui.btn_fileopen.clicked.connect(self.btn3Clicked)
        self.ui.btn_save.clicked.connect(self.btn4Clicked)
        self.ui.check_words.stateChanged.connect(self.btn5Clicked)
        self.ui.btn_clear.clicked.connect(self.btn6Clicked)
        self.ui.btn_clearall.clicked.connect(self.btn7Clicked)

    def btnClicked(self):
        self.ui.key_table.clear()
        self.ui.key_table.setRowCount(0)
        self.ui.key_combo.clear()
        self.ui.label_path.clear()
        self.mark.clear_selection(self.ui.text_form)

        try:
            if len(re.sub(r'\s', '', self.ui.text_form.toPlainText())) == 0:
                raise my_errors.MyError('textform_empty_error')
        except my_errors.MyError:
            self.ui.text_form.clear()
        else:
            if self.ui.check_count.isChecked():
                self.ui.key_table.horizontalHeader().show()
                self.ui.key_table.verticalHeader().hide()
                self.ui.key_table.setColumnCount(2)
                self.ui.key_table.setHorizontalHeaderLabels(["Ключевое выражение:", "Колличество вхождений в текст:"])
                self.ui.key_table.horizontalHeader().resizeSection(0, 380)
                self.ui.key_table.horizontalHeader().resizeSection(1, 240)
            else:
                self.ui.key_table.horizontalHeader().hide()
                self.ui.key_table.verticalHeader().hide()
                self.ui.key_table.setColumnCount(1)
                self.ui.key_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

            self.source_text = self.ui.text_form.toPlainText()

            extractor = analysis.analyzer(self.ui.text_form.toPlainText(), self.ui.check_nested.isChecked())
            keywords = extractor.analyze()

            for keyword in keywords:
                if self.check_wordcount(keyword[1]):
                    if keyword[0] >= self.ui.spin_count.value():
                        rowPosition = self.ui.key_table.rowCount()
                        self.ui.key_table.insertRow(rowPosition)
                        self.ui.key_table.setItem(rowPosition, 0, QTableWidgetItem(keyword[1]))
                        if self.ui.check_count.isChecked():
                            item = QTableWidgetItem(str(keyword[0]))
                            item.setTextAlignment(Qt.AlignCenter)
                            self.ui.key_table.setItem(rowPosition, 1, item)
                        self.ui.key_combo.addItem(keyword[1], keyword)

    def btn2Clicked(self):
        try:
            if self.ui.key_combo.currentIndex() == -1:
                raise my_errors.MyError('combobox_empty_error')
            elif len(re.sub(r'\s', '', self.ui.text_form.toPlainText())) == 0:
                raise my_errors.MyError('textform_empty_error')
            elif self.ui.key_table.rowCount() == 0:
                raise my_errors.MyError('keyform_empty_error')
            elif self.source_text != self.ui.text_form.toPlainText():
                raise my_errors.MyError('mismatch_error')
        except my_errors.MyError:
            self.ui.key_table.clear()
            self.ui.key_table.setRowCount(0)
            self.ui.key_table.horizontalHeader().hide()
            self.ui.key_combo.clear()
        else:
            self.mark.fill(self.ui.text_form.toPlainText(), self.ui.key_combo.currentData(), self.ui.text_form)
            self.mark.change_color()

    def btn3Clicked(self):
        fname = QFileDialog.getOpenFileName(self, 'Загрузить текст из файла', '*.txt', 'Text document (*.txt)')
        if fname[0] != '':
            f = open(fname[0], 'r', encoding='utf8')
            with f:
                data = f.read()
                self.ui.text_form.setText(data)
            self.ui.label_path.setText(fname[0])

    def btn4Clicked(self):
        try:
            if self.ui.key_table.rowCount() == 0:
                raise my_errors.MyError('keyform_empty_error')
        except my_errors.MyError:
            self.ui.key_table.clear()
            self.ui.key_table.setRowCount(0)
            self.ui.key_table.horizontalHeader().hide()
        else:
            path = QFileDialog.getSaveFileName(self, 'Сохранить файл', 'keywords.txt', 'Text document (*.txt)')
            if path[0] != '':
                f = open(path[0], 'w', encoding='utf8')
                with f:
                    for i in range(0, self.ui.key_table.rowCount()):
                        data = self.ui.key_table.item(i,0).text()
                        if self.ui.key_table.columnCount()==2: data+='  '+self.ui.key_table.item(i,1).text()+'\n'
                        else: data += '\n'
                        f.write(data)

    def check_wordcount(self, string):
        if self.ui.check_words.isChecked() == False:
            lst = string.split()
            if len(lst) <= self.ui.spin_word.value(): return True
            return False
        else:
            return True

    def btn5Clicked(self):
        if self.ui.check_words.isChecked() == True:
            self.ui.spin_word.setEnabled(False)
        else:
            self.ui.spin_word.setEnabled(True)

    def btn6Clicked(self):
        try:
            if self.ui.key_combo.currentIndex() == -1:
                raise my_errors.MyError('combobox_empty_error')
            elif len(re.sub(r'\s', '', self.ui.text_form.toPlainText())) == 0:
                raise my_errors.MyError('textform_empty_error')
            elif self.source_text != self.ui.text_form.toPlainText():
                raise my_errors.MyError('mismatch_error')
        except my_errors.MyError:
            self.ui.key_table.clear()
            self.ui.key_table.setRowCount(0)
            self.ui.key_table.horizontalHeader().hide()
            self.ui.key_combo.clear()
        finally:
            self.mark.clear_selection(self.ui.text_form)

    def btn7Clicked(self):
        self.ui.key_table.clear()
        self.ui.key_table.setRowCount(0)
        self.ui.key_table.horizontalHeader().hide()
        self.ui.key_combo.clear()
        self.ui.label_path.clear()
        self.ui.text_form.clear()

app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())