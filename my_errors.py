from PyQt5.QtWidgets import QMessageBox

class MyError(Exception):
    def __init__(self, text):
        self.txt = text
        if self.txt == 'combobox_empty_error':
            err_msg = 'Введите исходный текст на русском языке и нажмите кнопку "Анализ"'
        elif self.txt == 'textform_empty_error':
            err_msg = 'Введите исходный текст на русском языке'
        elif self.txt == 'keyform_empty_error':
            err_msg = 'Отсутствует список ключевых выражений. Нажмите кнопку "Анализ"'
        elif self.txt == 'mismatch_error':
            err_msg = 'Исходный текст был изменен. Нажмите на кнопку "Анализ" повторно'
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(err_msg)
        msg.setWindowTitle("Ошибка")
        msg.exec_()