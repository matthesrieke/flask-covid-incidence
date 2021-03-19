import papermill as pm
from papermill.exceptions import PapermillExecutionError

import pathlib
import datetime

def get_incidence_graph(region_name):
    out_file = "/tmp/%s.jpg" % region_name
    
    if not check_file_up_to_date(out_file):
        try:
            pm.execute_notebook(
                '/home/jovyan/nb.ipynb',
                '/tmp/output.ipynb',
                parameters = dict(kreis=region_name, output_file=out_file)
            )
        except PapermillExecutionError as e:
            raise ValueError(e)
    
    return out_file
        
def check_file_up_to_date(graph_file):
    fname = pathlib.Path(graph_file)
    if fname.exists():
        mtime = datetime.datetime.fromtimestamp(fname.stat().st_mtime)
        now = datetime.datetime.now()
        return (now - mtime).seconds < (20 * 60)
    else:
        return False