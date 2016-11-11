# add parent dir to path
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from core.database.db_services import DatabaseServices as DatabaseServices

DATABASE = None

def test_engine_init():
    global DATABASE

    DATABASE = DatabaseServices()

    DATABASE.init_engine(debug=True)

    assert DATABASE.engine is not None

def test_engine_persistence():
    global DATABASE

    assert DATABASE.engine is not None

def test_get_session():
    DATABASE.get_session()

    assert DATABASE.session is not None
