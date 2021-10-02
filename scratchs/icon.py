import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

import banana_inspector.resources
path = banana_inspector.resources.__path__[0]
print(path)
class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300,300,300,220)
        self.setWindowTitle('Icon')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    path = os.path.join(path, 'icon.png')
    app.setWindowIcon(QIcon(path))
    ex = Example()
    sys.exit(app.exec_())