"""
9/14/21

diego.aliaga at helsinki dot fi
"""

"""this implements the singleton design pattern.
all data and values that need to be communicated between the
qt windows are stored here."""

import pyqtgraph.dockarea



banana_data = None
"""maybe we dont need this anymore"""

dock_area: pyqtgraph.dockarea.DockArea = None
'''share dock area. new docks should be built here'''