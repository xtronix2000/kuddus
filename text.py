from PyQt5 import QtWidgets, uic, QtCore
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
from ntp import sync_with_ntp
import subprocess

# ntp1.ntp-servers.net

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        uic.loadUi('qt_kuddus.ui', self)
        self.graphWidget.setBackground('w')
        
        styles = {'color':'r', 'font-size':'15px'}
        self.graphWidget.setLabel('left', 'Delay (s)', **styles)
        self.graphWidget.setLabel('bottom', 'Seconds (s)', **styles)
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setEnabled(False)

        self.button_connect.clicked.connect(self.connect1)
        self.button_sync.clicked.connect(self.sync1)


    def sync1(self):
        commands = []
        linux = [f'chrony '] # комманда для синхронизации 
        windows = [f'w32tm ' ]
        if self.comboBox.currentText() == 'Linux':
            commands = linux
            print('linux')
        elif self.comboBox.currentText() == 'Windows':
            commands = windows
            print('windows')

        #for i in commands:
            #subprocess.call(i)


    def connect1(self):
        if self.button_connect.text() == 'Подключится':
            self.button_connect.setText('Отключится')

            self.y = [0 for i in range(10)] 
            self.x = [i for i in range(10)]

            my_pen = pg.mkPen(color=(255, 0, 0))
            self.data_line= self.graphWidget.plot(self.x, self.y, pen=my_pen)

            self.timer = QtCore.QTimer()
            self.timer.setInterval(1000)
            self.timer.timeout.connect(self.update_plot_data)
            self.timer.start()
        else:
            self.timer.stop()
            self.graphWidget.clear()
            self.button_connect.setText('Подключится')


    def update_plot_data(self):
        self.x = self.x[1:]
        self.x.append(self.x[-1] + 1)
        self.y = self.y[1:]
        self.y.append(sync_with_ntp(self.lineEdit.text()))
        self.data_line.setData(self.x, self.y)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
