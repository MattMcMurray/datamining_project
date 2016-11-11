# add parent dir to path
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import core.database.db_services as db

def test_engine_init():
    db.init_engine(debug=True)

    assert db.ENGINE is not None

def test_engine_persistence():
    assert db.ENGINE is not None

def test_get_session():
    db.get_session()

    assert db.MY_SESSION is not None

