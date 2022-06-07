import xarray as xr

from .CtrlNodeTree import CtrlNodeTree


class FileOpener():
    def __init__(self):
        pass


class FileOpenerNode(CtrlNodeTree):
    """opens a xarray file"""
    nodeName = "FileOpenerNode"
    uiTemplate = [
        # {
        #     'name': 'open file',
        #     'type': 'action',
        #     # 'value': 0.00,
        #     # 'readonly': True
        # },
        {
            'name'      : 'file path',
            'type'      : 'file',
            'fileMode'  : 'AnyFile',
            'acceptMode': 'AcceptOpen',
            # 'default'   : '/tmp/ff.cf',
        },
        {
            'name': 'field',
            'type': 'str',
            # 'value': 0.00,
            # 'readonly': True
        },
    ]

    def __init__(self, name):
        ## Define the input / output terminals available on this node
        terminals = {
            # 'dataIn': dict(io='in'),
            'dataOut': dict(io='out'),
            # 't1': dict(io='in'),
            # 't2': dict(io='in'),
        }

        CtrlNodeTree.__init__(self, name, terminals=terminals)

        # param = self.ctrls.param('open file')
        # param.sigActivated.connect(self.open_file)

    # def open_file(self):

    # noinspection PyMethodOverriding
    def process(self, display=True):
        # CtrlNode has created self.ctrls, which is a dict containing {ctrlName: widget}

        field = self.ctrls['field']
        file_path = self.ctrls['file path']

        ds = xr.open_dataset(file_path)
        da = ds[field]
        dataOut = da

        return {'dataOut': dataOut}
