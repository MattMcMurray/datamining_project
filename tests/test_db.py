# add parent dir to path
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from core.database.db_services import DatabaseServices as DatabaseServices
from settings import TEST_DATABASE_NAME

DATABASE = None

def test_engine_init():
    global DATABASE

    DATABASE = DatabaseServices(TEST_DATABASE_NAME)

    DATABASE.init_engine()

    assert DATABASE.engine is not None

def test_engine_persistence():
    global DATABASE

    assert DATABASE.engine is not None

def test_get_session():
    DATABASE.get_session()

    assert DATABASE.session is not None

def test_existence_and_cleanup():
    db_abs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..',
        TEST_DATABASE_NAME + '.db')

    print db_abs_path
    assert os.path.exists(db_abs_path)

    os.remove(db_abs_path)

    assert not os.path.exists(db_abs_path)

