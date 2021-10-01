"""
9/14/21

diego.aliaga at helsinki dot fi
"""

from pyqtgraph_back import LayoutWidget
import pyqtgraph_back as pg
import pyqtgraph_back.console
import numpy as np
from .. import shared_data as sd
from .. import funs

class Console(LayoutWidget):
    def __init__( self , parent, **kargs ):
        super().__init__( parent=parent, **kargs )
        namespace = {
                'pg': pg ,
                'np': np ,
                'sd': sd ,
                'parent':parent,
                'funs': funs
                }
        text = ''
        console = pyqtgraph_back.console.ConsoleWidget(
                namespace=namespace , text=text )
        
        self.addWidget( console )

