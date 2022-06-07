import xarray as xr

from .CtrlNodeTree import CtrlNodeTree


class FileSaver:
    def __init__(self):
        pass


class FileSaverNode(CtrlNodeTree):
    """saves a xarray file"""
    nodeName = "FileSaverNode"
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
            'name': 'var_name',
            'type': 'str',
            # 'value': 0.00,
            # 'readonly': True
        },
        {
            'name': 'comments',
            'type': 'str',
            # 'value': 0.00,
            # 'readonly': True
        },
    ]

    def __init__(self, name):
        ## Define the input / output terminals available on this node
        terminals = {
            'dataIn': dict(io='in'),
            'dataOut': dict(io='out'),
            # 't1': dict(io='in'),
            # 't2': dict(io='in'),
        }

        CtrlNodeTree.__init__(self, name, terminals=terminals)

        # param = self.ctrls.param('open file')
        # param.sigActivated.connect(self.open_file)

    # def open_file(self):

    # noinspection PyMethodOverriding
    def process(self, dataIn, display=True):
        # CtrlNode has created self.ctrls, which is a dict containing {ctrlName: widget}

        var_name = self.ctrls['var_name']
        file_path = self.ctrls['file path']
        comments = self.ctrls['comments']

        # ds = xr.open_dataset(file_path)

        da: xr.DataArray = dataIn
        da.name = var_name
        da.attrs = {'comments':comments}
        dataOut = da

        da.to_netcdf(file_path)


        return {'dataOut': dataOut}
