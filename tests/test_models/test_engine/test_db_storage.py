#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import pep8
import unittest

DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        all_objects = models.storage.all()
        self.assertIsInstance(all_objects, dict)
        self.assertGreaterEqual(len(all_objects), 0)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """Test that new adds an object to the database"""
        initial_count = models.storage.count(State)
        state = State(name="California")
        models.storage.new(state)
        models.storage.save()
        self.assertEqual(models.storage.count(State), initial_count + 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to the database"""
        state = State(name="New York")
        models.storage.new(state)
        models.storage.save()
        retrieved_state = models.storage.get(State, state.id)
        self.assertIsNotNone(retrieved_state)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test that get retrieves the correct object"""
        state = State(name="California")
        models.storage.new(state)
        models.storage.save()
        retrieved_state = models.storage.get(State, state.id)
        self.assertEqual(retrieved_state, state)
        self.assertIsNotNone(retrieved_state)
        self.assertEqual(retrieved_state.id, state.id)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_non_existent(self):
        """Test that get returns None when no object is found"""
        self.assertIsNone(models.storage.get(State, "non-existent-id"))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test that count returns the correct number of objects"""
        initial_count = models.storage.count()
        state = State(name="Nevada")
        models.storage.new(state)
        models.storage.save()
        self.assertEqual(models.storage.count(), initial_count + 1)
        self.assertEqual(models.storage.count(State), initial_count + 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_class(self):
        """Test that count returns the correct number of objects for a class"""
        state_count = models.storage.count(State)
        state = State(name="Arizona")
        models.storage.new(state)
        models.storage.save()
        self.assertEqual(models.storage.count(State), state_count + 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_no_class(self):
        """Test that count returns the correct number of all objects"""
        initial_count = models.storage.count()
        state = State(name="Oregon")
        user = User(email="user@example.com", password="password")
        models.storage.new(state)
        models.storage.new(user)
        models.storage.save()
        self.assertEqual(models.storage.count(), initial_count + 2)
