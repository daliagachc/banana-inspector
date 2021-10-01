from PyQt5 import QtWidgets
from banana_inspector.ui import input_output_tool_bar
# from pyqtgraph import PlotWidget , plot
import pyqtgraph_back as pg
from pyqtgraph_back.widgets.FileDialog import FileDialog
import sys  # We need sys so that we can pass argv to QApplication


class MainWindow( QtWidgets.QWidget ):

    def __init__( self , *args , **kwargs ):
        super( MainWindow , self ).__init__( *args , **kwargs )

        self.ui = input_output_tool_bar.Ui_Form()
        self.ui.setupUi(self)

        # self.connect_slots()


        # Load the UI Page
        # uic.loadUi( 'ui/BananaFinder.ui' , self )

    def sel_dir(self):
        # fd = FileDialog()
        # pg.QtGui.QFileDialog.getSaveFileName(self, "Save State..", "untitled.cfg", "Config Files (*.cfg)")
        res = pg.QtGui.QFileDialog.getExistingDirectory()
        print(res)
        self.ui.input_dir.setText(res)

    def sel_file(self):
        # fd = FileDialog()
        # pg.QtGui.QFileDialog.getSaveFileName(self, "Save State..", "untitled.cfg", "Config Files (*.cfg)")
        res = pg.QtGui.QFileDialog.getOpenFileName(
            directory=self.ui.input_dir.text()
        )
        print(res)
        self.ui.input_file.setText(res[0])

    def sel_out_dir(self):
        # fd = FileDialog()
        # pg.QtGui.QFileDialog.getSaveFileName(self, "Save State..", "untitled.cfg", "Config Files (*.cfg)")
        res = pg.QtGui.QFileDialog.getExistingDirectory()
        print(res)
        self.ui.output_dir.setText(res)

def main():
    app = QtWidgets.QApplication( sys.argv )
    main = MainWindow()
    main.show()
    sys.exit( app.exec() )


if __name__ == '__main__':
    main()