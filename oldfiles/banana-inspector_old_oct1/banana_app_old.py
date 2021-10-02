"""
9/14/21

diego.aliaga at helsinki dot fi
"""

from PyQt5 import QtWidgets
from banana_inspector.ui import BananaMainWindow
# from pyqtgraph import PlotWidget , plot
# import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication


class MainWindow( QtWidgets.QMainWindow ):
    
    def __init__( self , *args , **kwargs ):
        super( MainWindow , self ).__init__( *args , **kwargs )
        
        self.ui = BananaMainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Load the UI Page
        # uic.loadUi( 'ui/BananaFinder.ui' , self )
        

def main():
    app = QtWidgets.QApplication( sys.argv )
    main = MainWindow()
    main.show()
    sys.exit( app.exec_() )


if __name__ == '__main__':
    main()
