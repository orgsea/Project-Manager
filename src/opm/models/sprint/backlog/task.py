import opm.models.store as store
import opm.models.project as project


class Task(store.Store):
    def __init__(self, oid):
        super(Task, self).__init__(oid)

    @property
    def name(self):
        """
        The name of the task
        """
        return self._document['name']


    @name.setter
    def name(self, name):
        self._document['name'] = str(name)
        #set safe to True so that if something goes wrong it reports it
        self._db.update({'_id':self._id}, {'$set': self._document}, safe=True)

        return self._document['name']



    @property
    def description(self):
        """
        The description of what the task is
        """
        return self_document['description']



    @description.setter
    def description(self, description):
        self._document['description'] = description

        self._db.update({'_id':self._id}, {'$set': self._document}, safe=True)

        return self._document['description']
