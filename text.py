from PyQt5 import QtWidgets, uic, QtCore
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
from ntp import sync_with_ntp

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi('qt_kuddus.ui', self)
        self.graphWidget.setBackground('w')
        
        styles = {'color':'r', 'font-size':'15px'}
        self.graphWidget.setLabel('left', 'Delay (s)', **styles)
        self.graphWidget.setLabel('bottom', 'Seconds (s)', **styles) #  
        self.graphWidget.showGrid(x=True, y=True) #  сетка


        self.ui.button_connect.clicked.connect(lambda: print(self.listEdit_server.text()))


        #  self.graphWidget.clear()

        self.y = [float(sync_with_ntp('ntp1.ntp-servers.net')) for i in range(10)] 
        self.x = [i for i in range(10)]


        my_pen = pg.mkPen(color=(255, 0, 0))
        self.data_line= self.graphWidget.plot(self.x, self.y, pen=my_pen)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()


    def update_plot_data(self):
        #  self.x.append(self.x[-1] + 1)

        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append(sync_with_ntp('ntp1.ntp-servers.net'))  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.



def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
