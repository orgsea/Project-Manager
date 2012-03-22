#test code for opm.models.project
import opm.models.project as project
import opm.models.store as store

import unittest
import bson
import datetime
import copy


class TestProject(unittest.TestCase):
    name = 'new project'
    owners = ['owner1', 'owner2',]
    team = ['member1', 'member2',]
    backlog_items = ['task1', 'task2',]
    start_date = datetime.datetime(2012, 3, 18, 23, 25, 13, 725000)
    projected_finish_date = datetime.datetime(2012, 4, 18, 23, 25, 13, 725000)
    finish_date = datetime.datetime(2012, 4, 18, 23, 25, 13, 725000)
    description = """A short description.
    With new lines.
    And another new line.
    """


    @classmethod
    def setUpClass(cls):
        #create a db object
        store.organisation = store.mongo_connection.test
        cls.db = store.organisation.Project
        #setup a temp Project in the db not using the Project class
        document = {'name':TestProject.name,
                    'owners':TestProject.owners,
                    'team':TestProject.team,
                    'backlog_items':TestProject.backlog_items,
                    'start_date':TestProject.start_date,
                    }
        cls.oid = cls.db.insert(document, safe=True)
        

    @classmethod
    def tearDownClass(cls):
        cls.db.remove(safe=True)
        del cls.db
        del cls.oid


    def try_get_attribute(self, attr):
        project_inst = project.Project(str(TestProject.oid))
        self.assertIsNotNone(project_inst)
        self.assertEqual(getattr(project_inst, attr), getattr(TestProject, attr))
        #make sure db is same
        entry = TestProject.db.find_one({'_id': TestProject.oid})
        self.assertEqual(entry['name'], TestProject.name)


    def try_get_list_attribute(self, attr):
        project_inst = project.Project(str(TestProject.oid))
        self.assertIsNotNone(project_inst)
        self.assertEqual(getattr(project_inst, attr),
                         tuple(getattr(TestProject, attr)))
        #make sure db is same
        entry = TestProject.db.find_one({'_id': TestProject.oid})
        self.assertEqual(entry['name'], TestProject.name)



    def try_set_attribute(self, attr, value):
        project_inst = project.Project(str(TestProject.oid))
        self.assertEqual(getattr(project_inst, attr),
                         getattr(TestProject, attr))
        
        setattr(project_inst, attr, value)
        self.assertEqual(getattr(project_inst, attr), value)
        
        #make sure it's changed on db too
        entry = TestProject.db.find_one({'_id': TestProject.oid})
        self.assertEqual(entry[attr], value)


    def try_set_list_attribute(self, attr, str_value, tuple_value, value):
        project_inst = project.Project(str(TestProject.oid))
        #try and set with a non list type
        try:
            setattr(project_inst, attr, str_value)
        except TypeError as error:
            pass
        else:
            self.fail("Shouldn't be able to assign string to owners")
        #try and set the owners as a tuple
        try:
            setattr(project_inst, attr, tuple_value)
        except TypeError as error:
            pass
        else:
            self.fail("Shouldn't be able to assign tuple to owners")

        #legit assignment of a list
        try:
            setattr(project_inst, attr, value)
        except Exception as error:
            self.fail(str(error))

        #check and make sure it has actually changed
        self.assertEqual(getattr(project_inst, attr), tuple(value))
        #make sure db is same
        entry = TestProject.db.find_one({'_id': TestProject.oid})
        self.assertEqual(entry[attr], value)


    def test_create_project(self):
        name = TestProject.name+'1'
        project_inst = project.Project.create(name,
                                              TestProject.owners,
                                              TestProject.team,
                                              TestProject.backlog_items)

        self.assertIsNotNone(project_inst)
        self.assertIsInstance(project_inst, project.Project)
        minst = TestProject.db.find_one({'_id':bson.ObjectId(project_inst.id)})
        self.assertIsNotNone(minst)
        self.assertEqual(str(project_inst.id), str(minst['_id']))
        self.assertEqual(str(project_inst.name), str(minst['name']))



    def test_get_existing_project(self):
        project_inst = project.Project(str(TestProject.oid))
        self.assertIsNotNone(project_inst)
        self.assertIsInstance(project_inst, project.Project)
        self.assertEqual(project_inst.id, str(TestProject.oid))
        self.assertEqual(str(project_inst.name), str(TestProject.name))



    def test_get_project_name(self):
        self.try_get_attribute('name')
                

    def test_set_project_name(self):
        self.try_set_attribute('name', TestProject.name+'2')
        
                         

    def test_get_owners(self):
        self.try_get_list_attribute('owners')
        

    def test_set_owners(self):
        self.try_set_list_attribute('owners', 'jim', ('jim',), ['jim'])


    def test_get_team(self):
        self.try_get_list_attribute('team')


    def test_set_team(self):
        self.try_set_list_attribute('team', 'jim', ('jim',), ['jim'])


    def test_get_backlog_items(self):
        self.try_get_list_attribute('backlog_items')


    def test_set_backlog_items(self):
        self.try_set_list_attribute('backlog_items', 'task1', ('task1',), ['task1'])


    def test_get_start_date(self):
        self.try_get_attribute('start_date')
        

    def test_set_start_date(self):
        now = datetime.datetime(2012, 3, 18, 23, 28, 15, 355000)
        self.try_set_attribute('start_date', now)
        

    def test_get_projected_finish_date(self):
        entry = TestProject.db.find_one({'_id': TestProject.oid})
        entry['projected_finish_date'] = TestProject.projected_finish_date
        del entry['_id'] #can't update with _id as part of the data to update
        TestProject.db.update({'_id': TestProject.oid},
                              {'$set': entry}, safe=True)
        self.try_get_attribute('projected_finish_date')


    def test_set_projected_finish_date(self):
        now = datetime.datetime(2012, 5, 18, 23, 28, 15, 355000)
        self.try_set_attribute('projected_finish_date', now)


    def test_get_finish_date(self):
        entry = TestProject.db.find_one({'_id': TestProject.oid})
        entry['finish_date'] = TestProject.finish_date
        del entry['_id'] #can't update with _id as part of the data to update
        TestProject.db.update({'_id': TestProject.oid},
                              {'$set': entry}, safe=True)
        self.try_get_attribute('finish_date')


    def test_set_finish_date(self):
        now = datetime.datetime(2012, 8, 18, 23, 28, 15, 355000)
        self.try_set_attribute('finish_date', now)


    def test_get_description(self):
        entry = TestProject.db.find_one({'_id': TestProject.oid})
        entry['description'] = TestProject.description
        del entry['_id'] #can't update with _id as part of the data to update
        TestProject.db.update({'_id': TestProject.oid},
                              {'$set': entry}, safe=True)


    def test_set_description(self):
        description = """
        Not another,
        description"""
        
        self.try_set_attribute('description', description)

        
if __name__ == '__main__':
    unittest.main()
    
