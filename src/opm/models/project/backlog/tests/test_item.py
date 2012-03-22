import opm.models.project.backlog.item as item

import unittest

class TestItem(unittest.TestCase):
    name = "Test Item"
    description = """
    A description of many lines.
    Starting with this one.
    Ending with this.
    """
    priority = "High"
    effort = 12

    
    @classmethod
    def setUpClass(cls):
        document = { 'name'        : TestItem.name,
                     'description' : TestItem.description,
                     }
        #create a db object
        store.organisation = store.mongo_connection.test
        cls.db = store.organisation.Item
        cls.oid = cls.db.insert(document, safe=True)

    @classmethod
    def tearDownClass(cls):
        cls.db.remove(safe=True)
        del cls.db
        del cls.oid
        


    def test_get_name(self):
        self.fail("Not implemented")


    def test_set_name(self):
        self.fail("Not implemented")


    def test_get_description(self):
        self.fail("Not implemented")


    def test_set_description(self):
        self.fail("Not implemented")


    def test_get_priority(self):
        self.fail("Not implemented")


    def test_set_priority(self):
        self.fail("Not implemented")


    def test_get_effort(self):
        self.fail("Not implemented")


    def test_set_effort(self):
        self.fail("Not implemented")


    def test_create(self):
        self.fail("Not implemented")
