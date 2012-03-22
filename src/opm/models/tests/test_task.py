#test code for opm.models.task
import opm.models.project as project
import opm.models.store as store

import unittest
import bson
import datetime
import copy


class TestTask(unittest.TestCase):
    name = 'new task'
    description = """
    A description.
    With more than one line.
    In fact 3 lines.
    """


    def test_get_name(self):
        self.fail("Not implemented yet")


    def test_set_name(self):
        self.fail("Not implemented yet")


    def test_get_description(self):
        self.fail("Not implemented yet")


    def test_set_description(self):
        self.fail("Not implemented yet")


        
if __name__ == "__main__":
    unittest.main()
