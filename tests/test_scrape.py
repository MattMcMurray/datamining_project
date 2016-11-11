# add parent dir to path
import os.path
import sys
import shutil
import time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import start_scrape as sc

def test_create_dir():
    dirname = 'new_test_dir'

    sc.create_output_dir(dirname)

    dir_rel_path = os.path.join('..', dirname)
    dir_abs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        dir_rel_path)
    assert os.path.exists(dir_abs_path)

    ## cleanup
    shutil.rmtree(dir_abs_path, ignore_errors=True)
    assert not os.path.exists(dir_abs_path)
