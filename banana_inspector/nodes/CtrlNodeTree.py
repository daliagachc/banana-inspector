from pyqtgraph.Qt import QtCore
from pyqtgraph.flowchart import Node


class CtrlNodeTree(Node):
    """Abstract class for nodes with auto-generated control UI
    it is similat ro CtrlNode but implements the parameter tree as
    the control ui

    """


    sigStateChanged = QtCore.Signal(object)

    def __init__(self, name, ui=None, terminals=None):
        if terminals is None:
            terminals = {'In': {'io': 'in'}, 'Out': {'io': 'out', 'bypass': 'In'}}
        Node.__init__(self, name=name, terminals=terminals)

        if ui is None:
            if hasattr(self, 'uiTemplate'):
                ui = self.uiTemplate
            else:
                ui = []



        # self.ui, self.stateGroup, self.ctrls = generateUi(ui)
        from pyqtgraph.parametertree import Parameter, ParameterTree
        p = Parameter.create(
            name='params', type='group', children=ui)

        t = ParameterTree()
        t.setParameters(p, showTop=False)

        p.sigTreeStateChanged.connect(self.changed)

        self.ui = t
        self.stateGroup = p
        self.ctrls = p

        # for c in  p.children():
        #     c.sigValueChanged.connect(self.changed)


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
        state['ctrl'] = self.stateGroup.saveState()
        return state

    def restoreState(self, state):
        Node.restoreState(self, state)
        if self.stateGroup is not None:
            self.stateGroup.restoreState(state.get('ctrl', {}))

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