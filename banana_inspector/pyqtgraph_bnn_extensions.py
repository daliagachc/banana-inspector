"""
9/16/21

diego.aliaga at helsinki dot fi
"""
import pyqtgraph_back as pg
import pyqtgraph_back.flowchart.library as fclib
from pyqtgraph_back import QtCore
from pyqtgraph_back import QtGui
from pyqtgraph_back.WidgetGroup import WidgetGroup
from pyqtgraph_back.flowchart import Node
from pyqtgraph_back.widgets.ColorButton import ColorButton
# import PyQt5
from pyqtgraph_back.widgets.SpinBox import SpinBox



class BLE(QtGui.QLineEdit):
    def __init__(self, type, key, *args, **kargs):
        QtGui.QLineEdit.__init__(self, *args, **kargs)

        button = pg.QtGui.QPushButton(self)
        button.setText(key)
        # button.clicked.connect(self.button_clicked)

        # self.file_dialog = pg.FileDialog()
        # self.sel_dir = None
        self.type = type
        self.key = key
        self.button = button

        self.button.clicked.connect(self.button_clicked)

    def dir_sel(self, dir_str):
        # self.of.show()
        self.setText(dir_str)
        self.editingFinished.emit()

    def button_clicked(self):
        # print('dsf')
        # print(self.type)

        if self.type == 'set_dir':
            fd = pg.QtGui.QFileDialog()
            fd.setOption(fd.Option(1))
            fd.fileSelected.connect(self.dir_sel)
            fd.exec()
        if self.type == 'set_file':
            fd = pg.QtGui.QFileDialog()
            # fd.setOption(fd.Option(1))
            fd.fileSelected.connect(self.dir_sel)
            fd.exec()

    def widgetGroupInterface(self):
        tuple = (
            lambda w: w.editingFinished,
            lambda w: str(w.text()),
            BLE.setText
        )
        return tuple


class TextEdit(QtGui.QTextEdit):
    """
    A TextEdit editor that sends editingFinished events
    when the text was changed and focus is lost.
    """

    editingFinished = QtCore.pyqtSignal()
    receivedFocus = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(TextEdit, self).__init__(parent)
        self._changed = False
        self.setTabChangesFocus(True)
        self.textChanged.connect(self._handle_text_changed)

    def focusInEvent(self, event):
        super(TextEdit, self).focusInEvent(event)
        self.receivedFocus.emit()

    # def setText(self, p_str):
    #     super(TextEdit, self).setText(p_str)
    #     self.editingFinished.emit()

    def focusOutEvent(self, event):
        if self._changed:
            self.editingFinished.emit()
        super(TextEdit, self).focusOutEvent(event)

    def _handle_text_changed(self):
        self._changed = True

    def setTextChanged(self, state=True):
        self._changed = state

    def setHtml(self, html):
        QtGui.QTextEdit.setHtml(self, html)
        self._changed = False

    def widgetGroupInterface(self):
        tuple = (
            lambda w: w.editingFinished,
            lambda w: str(w.toPlainText()),
            TextEdit.setText
        )
        return tuple

class PlainTextEdit(QtGui.QPlainTextEdit):
    """
    A TextEdit editor that sends editingFinished events
    when the text was changed and focus is lost.
    """

    def __init__(self):
        super(QtGui.QPlainTextEdit, self).__init__()
        self.setReadOnly(True)

    def widgetGroupInterface(self):
        tuple = (
            lambda w: w.textChanged,
            lambda w: str(w.toPlainText()),
            PlainTextEdit.setPlainText
        )
        return tuple


def generateUi(opts):
    """Convenience function for generating common UI types"""
    widget = QtGui.QWidget()
    l = QtGui.QFormLayout()
    l.setSpacing(0)
    widget.setLayout(l)
    ctrls = {}
    row = 0
    for opt in opts:
        if len(opt) == 2:
            k, t = opt
            o = {}
        elif len(opt) == 3:
            k, t, o = opt
        else:
            raise Exception(
                "Widget specification must be (name, type) or (name, type, {opts})")

        ## clean out these options so they don't get sent to SpinBox
        hidden = o.pop('hidden', False)
        tip = o.pop('tip', None)

        if t == 'intSpin':
            w = QtGui.QSpinBox()
            if 'max' in o:
                w.setMaximum(o['max'])
            if 'min' in o:
                w.setMinimum(o['min'])
            if 'value' in o:
                w.setValue(o['value'])
        elif t == 'doubleSpin':
            w = QtGui.QDoubleSpinBox()
            if 'max' in o:
                w.setMaximum(o['max'])
            if 'min' in o:
                w.setMinimum(o['min'])
            if 'value' in o:
                w.setValue(o['value'])
        elif t == 'spin':
            w = SpinBox()
            w.setOpts(**o)
        elif t == 'check':
            w = QtGui.QCheckBox()
            if 'checked' in o:
                w.setChecked(o['checked'])
        elif t == 'combo':
            w = QtGui.QComboBox()
            for i in o['values']:
                w.addItem(i)
        elif t == 'text':
            w = QtGui.QLineEdit()
            w.setText(o['value'])

        elif (t == 'set_dir') or (t == 'set_file'):
            # of = pg.FileDialog(None)
            w = BLE(type=t, key=k)
            w.setText(o['value'])

        elif t == 'peel_edit':
            w = TextEdit(None)
            w.setText(o['text'])

        elif t == 'multi_text':
            w = PlainTextEdit()
            w.setPlainText(o['text'])

        # elif t == 'colormap':
        # w = ColorMapper()
        elif t == 'color':
            w = ColorButton()

        # elif t == 'button':
        #     w = QtGui.QPushButton()
        #     w.clicked.connect(o['function'])
        else:
            raise Exception("Unknown widget type '%s'" % str(t))

        if tip is not None:
            w.setToolTip(tip)
        w.setObjectName(k)
        if (t == 'set_dir') or (t == 'set_file'):
            # # button = pg.QtGui.QPushButton()
            # button = o['button']
            # button.clicked.connect(w.dir_sel)
            # button.setText(k)
            # # w.button = button
            l.addRow(w.button, w)
        else:
            l.addRow(k, w)
        if hidden:
            w.hide()
            label = l.labelForField(w)
            label.hide()

        ctrls[k] = w
        w.rowNum = row
        row += 1
    group = WidgetGroup(widget)
    return widget, group, ctrls


class CtrlNodeExt(Node):
    """Abstract class for nodes with auto-generated control UI
    This class was extended by bnn-inspection"""

    sigStateChanged = QtCore.Signal(object)

    def __init__(self, name, ui=None, terminals=None):
        if terminals is None:
            terminals = {'In': {'io': 'in'},
                         'Out': {'io': 'out', 'bypass': 'In'}}
        Node.__init__(self, name=name, terminals=terminals)

        if ui is None:
            if hasattr(self, 'uiTemplate'):
                ui = self.uiTemplate
            else:
                ui = []

        self.ui, self.stateGroup, self.ctrls = generateUi(ui)
        self.stateGroup.sigChanged.connect(self.changed)

    def ctrlWidget(self):
        return self.ui

    def changed(self):
        self.update()
        self.sigStateChanged.emit(self)

    def process(self, In, display=True):
        out = self.processData(In)
        return {'Out': out}

    def saveState(self):
        state = Node.saveState(self)
        state['ctrl'] = self.stateGroup.state()
        return state

    def restoreState(self, state):
        Node.restoreState(self, state)
        if self.stateGroup is not None:
            self.stateGroup.setState(state.get('ctrl', {}))

    def hideRow(self, name):
        w = self.ctrls[name]
        l = self.ui.layout().labelForField(w)
        w.hide()
        l.hide()

    def showRow(self, name):
        w = self.ctrls[name]
        l = self.ui.layout().labelForField(w)
        w.show()
        l.show()


def register_nodes():
    '''registers all the nodes in the nodes folder.
    the name of the node class should by the same as the module name'''
    import banana_inspector.nodes as nodes
    import glob
    from importlib import import_module
    node_path = nodes.__path__[0]
    names = glob.glob1(node_path, '*Node.py')
    n2 = [n[:-3] for n in names]
    node_klasses = []
    for n in n2:
        mod = import_module(f'banana_inspector.nodes.{n}')
        k = getattr(mod, n)
        fclib.registerNodeType(k, [('Display',)])
