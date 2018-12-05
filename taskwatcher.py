from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem

import MainWindow
import PersonPopup
import sys
import os
import collections


class Main(QMainWindow, MainWindow.Ui_MainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

        # operation
        self.btn_load_data.clicked.connect(self.load_data)
        self.tableWidget.clicked.connect(self.open_person_popup)
        #self.tableWidget.cellClicked.connect(self.print_hai)
        self.tableWidget.clicked.connect(self.print_hai)


    def open_person_popup(self):
        self.mynew_window = Second()
        # TODO get first item only
        self.mynew_window.label_nama.setText(self.tableWidget.currentItem().text())
        self.mynew_window.show()


    def print_hai(self):
        print(self.tableWidget.currentItem().row())
        print('Hai hai hai')


    def get_perpeson_value():
        # CWD = os.getcwd()
        ROOTDIR = '/home/azzamsya/code-coba-home/taskwtacher-coba/coba_baca_perfolder/'

        all_window_perperson = {}
        auth_info_perperson = {}
        focused_windows_perperson = {}
        perpeson_value = {}

        for subdir, dirs, files in os.walk(CWD):
            for file in files:
                if file == 'all_windows':
                    filepath = subdir + os.sep + file
                    all_window_linecount = len(open(filepath).readlines(  ))
                    all_window_perperson[subdir.split('/')[-2]] = all_window_linecount
                    print('ketemu ' + file + ' di ' + subdir)
                if file == 'auth_info':
                    filepath = subdir + os.sep + file
                    auth_info_linecount = len(open(filepath).readlines(  ))
                    auth_info_perperson[subdir.split('/')[-2]] = auth_info_linecount
                    print('ketemu ' + file + ' di ' + subdir)
                if file == 'focused_windows':
                    filepath = subdir + os.sep + file
                    focused_windows_linecount = len(open(filepath).readlines(  ))
                    focused_windows_perperson[subdir.split('/')[-2]] = focused_windows_linecount
                    print('ketemu ' + file + ' di ' + subdir)

        print("all window per person :" + str(all_window_perperson))
        print("auth info per person : " + str(auth_info_perperson))
        print("focused windows per person : " + str(focused_windows_perperson))

        perpeson_value['all_window_perperson'] = all_window_perperson
        perpeson_value['auth_info_perperson'] = auth_info_perperson
        perpeson_value['focused_window_perperson'] = focused_windows_perperson

        return perpeson_value

    def load_data(self):
        print('load dipencet')

        all_data = collections.OrderedDict([('budi',
                                             collections.OrderedDict([('nama', 'budi'),
                                                                  ('all_window_perperson', 9),
                                                                      ('auth_info_perperson', 3),
                                                                      ('focused_windows_perperson', 1)])),
                                            ('ani',
                                             collections.OrderedDict([('nama', 'ani'),
                                                                 ('all_window_perperson', 10),
                                                                      ('auth_info_perperson', 30),
                                                                      ('focused_windows_perperson', 10)])),
                                            ('caca',
                                             collections.OrderedDict([('nama', 'caca'),
                                                                  ('all_window_perperson', 40),
                                                                      ('auth_info_perperson', 44),
                                                                      ('focused_windows_perperson', 47)]))])

        self.tableWidget.setRowCount(0)

        for row_number, nama_key in enumerate(all_data):
            print('row number : %d, row data : %s' % (row_number, str(nama_key)))
            self.tableWidget.insertRow(row_number)

            for column_number, column_key in enumerate(all_data[nama_key]):
                print('row number : %d, column_number : %d,  column_key : %s, value : %s'
                      % (row_number, column_number, column_key, str(all_data[nama_key][column_key])))
                table_item = QTableWidgetItem(str(all_data[nama_key][column_key]))
                self.tableWidget.setItem(row_number, column_number, table_item)


class Second(QTableWidget, PersonPopup.Ui_Form):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)
        self.setupUi(self)

if __name__ == "__main__":

    QCoreApplication.setApplicationName("app name")
    QCoreApplication.setApplicationVersion("app version")
    QCoreApplication.setOrganizationName("Your name")
    QCoreApplication.setOrganizationDomain("Your URL")

    app = QApplication(sys.argv)
    form = Main()
    form.show()
    sys.exit(app.exec_())
