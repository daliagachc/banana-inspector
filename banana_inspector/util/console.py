from .. import confg
import pyqtgraph.console

def create_console():
    namespace = {'c': confg}

    ## initial text to display in the console
    text = """
    This is an interactive python console. 
    the conf space is at c. for example c.dock_area
    """
    pg_console = pyqtgraph.console.ConsoleWidget(
        namespace=namespace, text=text)

    return pg_console