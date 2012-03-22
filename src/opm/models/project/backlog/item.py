import opm.models.store as store
import opm.models.project as project

class Item(store.Store):
    def __init__(self, oid):
        super(Item, self).__init__(oid)


    @property
    def name(self):
        return self._document['name']


    @name.setter
    def name(self, name):
        self._document['name'] = str(name)

        self._db.update({'_id':self._id}, {'$set': self._document}, safe=True)
        
        return self._document['name']
    

    @property
    def description(self):
        return self._document['name']



    @description.setter
    def description(self, description):
        self._document['description'] = description

        self._db.update({'_id':self._id}, {'$set': self._document}, safe=True)


        return self._document['description']


    @property
    def priority(self):
        """
        The priority of this backlog item
        """
        return self._document['priority']



    @priority.setter
    def priority(self, priority):
        self._document['priority'] = priority

        self._db.update({'_id':self._id}, {'$set': self._document}, safe=True)

        return self._document['priority']



    @property
    def effort(self):
        return self._document['effort']


    @effort.setter
    def effort(self, effort):
        self._document['effort'] = priority

        self._db.update({'_id':self._id}, {'$set': self._document}, safe=True)

        return self._document['effort']


    @staticmethod
    def create(name, description, priority=None, effort=None):
        document = { 'name':str(name),
                     'description': description,
                     }
        if priority:
            document['priority'] = priority

        if effort:
            document['effort'] = effort

        oid = self._db.insert(document)

        return Item(oid)
    
    
