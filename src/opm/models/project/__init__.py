import datetime

import opm.models.store as store

class Project(store.Store):
    """
    A project which could be a software project or anything.  It consists of a set of tasks to complete
    """
    def __init__(self, oid):
        """
        Constructor for the Project class.
        
        Connects to the DB and retrieves the record for this project, identified by its oid.

        oid - a string representing the _id of the project entry.
        """
        super(Project, self).__init__(oid)


    @property
    def name(self):
        """
        The name of the project.  Should be unique
        """
        return self._document['name']


    @name.setter
    def name(self, name):
        self._document['name'] = str(name)
        #set safe to True so that if something goes wrong it reports it
        self._db.update({'_id':self._id}, {'$set': self._document}, safe=True)

        return self._document['name']


    @property
    def owners(self):
        """
        The list of owners as a tuple.  Tuples are readonly as I don't want them modified by going Project.owners.append(name).
        """
        if not isinstance(self._document['owners'], list):
            if isinstance(self._document['owners'], str):
                raise TypeError("owners is not stored as a list of owners. It is instead a " + 
                                str(type(self._document['owners'])))
            
        return tuple(self._document['owners'])
    

    @owners.setter
    def owners(self, owners):
        #make sure it's a list
        if not isinstance(owners, list):
            raise TypeError('owners must be a list not a ' + str(type(owners)))


        self._document['owners'] = owners
        self._db.update({'_id':self._id}, {'$set': self._document}, safe=True)

        return tuple(self._document['owners'])


    @property
    def team(self):
        """
        The team members working on this project
        """
        if not isinstance(self._document['team'], list):
            raise TypeError("team must be stored as a list, instead it's being stored as a " +
                            str(type(self._document['team'])))
        
        return tuple(self._document['team'])



    @team.setter
    def team(self, team):
        if not isinstance(team, list):
            raise TypeError("team must be a list instead was supplied with a " +
                            str(type(team)))

        self._document['team'] = team
        self._db.update({'_id':self._id}, {'$set': self._document}, safe=True)

        return tuple(self._document['team'])


    @property
    def backlog_items(self):
        """
        The backlog items need doing for this project
        """
        if not isinstance(self._document['backlog_items'], list):
            raise TypeError('backlog_items is expected to be stored as a list of oids instead got a ' +
                            str(type(self._document['backlog_items'])))
        
        return tuple(self._document['backlog_items'])


    @backlog_items.setter
    def backlog_items(self, items):
        if not isinstance(items, list):
            raise TypeError('backlog_items expected to be a list of oids instead got a ' +
                            str(type(items)))

        self._document['backlog_items'] = items
        self._db.update({'_id':self._id}, {'$set': self._document}, safe=True)

        return tuple(self._document['backlog_items'])


    @property
    def start_date(self):
        """
        When the project began as a datetime.datetime object
        """
        if not isinstance(self._document['start_date'], datetime.datetime):
            raise TypeError("start_date is expected to be a datetime.datetime instance instead got " +
                            str(type(self._document['start_date'])))
        
        return self._document['start_date']


    @start_date.setter
    def start_date(self, start_date):
        if not isinstance(start_date, datetime.datetime):
            raise TypeError("start_date is expected to be a datetime.datetime instance instead got " +
                            str(type(start_date)))

        self._document['start_date'] = start_date
        self._db.update({'_id':self._id}, {'$set': self._document}, safe=True)

        return self._document['start_date']


    @property
    def projected_finish_date(self):
        """
        The date it is expected to finish
        """
        if not isinstance(self._document['projected_finish_date'], datetime.datetime):
            raise TypeError("projected_finish_date is expected to be a " +
                            "datetime.datetime instance instead got " +
                            str(type(self._document['projected_finish_date'])))
        
        return self._document['projected_finish_date']



    @projected_finish_date.setter
    def projected_finish_date(self, findate):
        if not isinstance(findate, datetime.datetime):
            raise TypeError("projected_finish_date is expected to be a " +
                            "datetime.datetime instance instead got " +
                            str(type(findate)))

        self._document['projected_finish_date'] = findate
        self._db.update({'_id':self._id}, {'$set':self._document}, safe=True)

        return self._document['projected_finish_date']


    @property
    def finish_date(self):
        """
        The actual finish date.  If project is still going it will be None
        """
        if 'finish_date' in self._document:
            if not isinstance(self._document['finish_date'], datetime.datetime):
                raise TypeError("finish_date is expected to be a datetime.datetime instance " +
                                "instead got a " + str(type(self._document['finish_date'])))

            return self._document['finish_date']

        
        return None

        

    @finish_date.setter
    def finish_date(self, findate):
        if not isinstance(findate, datetime.datetime):
            raise TypeError("finish_date is expected to be a " +
                            "datetime.datetime instance instead got " +
                            str(type(findate)))

        self._document['finish_date'] = findate
        self._db.update({'_id':self._id}, {'$set':self._document}, safe=True)

        return self._document['finish_date']


    @property
    def description(self):
        if 'description' in self._document:
            if not isinstance(self._document['description'], str):
                raise TypeError("'description' is expected to be a string " +
                                "instead got a " +
                                str(type(self._document['description'])))
            return self._document['description']
        
        return None


    @description.setter
    def description(self, description):
        if not isinstance(description, str):
            raise TypeError("'description' is expected to be a " +
                            "string instead got " +
                            str(type(description)))

        self._document['description'] = description
        self._db.update({'_id':self._id}, {'$set':self._document}, safe=True)

        return self._document['description']
    

    @staticmethod
    def create(name, owners, team, tasks, start_date=None, projected_finish=None, description = None):
        """
        Creates a new project, storing it in the database and returning a Project instance which represents it
        """
        if not isinstance(name, str) or not isinstance(owners, list) or not isinstance(team, list):
            raise TypeError("'name' must be a string, 'owners' and 'tasks' must be a list." +
                            "  Instead we got 'name': " + str(type(name)) +
                            " 'owners': " + str(type(owners)) + " 'tasks': " + str(type(tasks)))
        document = {'name':name, 'owners':owners, 'team':team,
                    'tasks':tasks,}
        if start_date:
            if isinstance(start_date, datetime.datetime):
                document['start_date'] = start_date
            else:
                raise TypeError("'start_date' expected to be a datetime.datetime.  Instead got " +
                                str(type(start_date)))
        else:
            document['start_date'] = datetime.datetime.now()

        if projected_finish:
            if isinstance(projected_finish, datetime.datetime):
                document['projected_finish_date'] = projected_finish
            else:
                raise TypeError("'projected_finish' expected to be a " +
                                "datetime.datetime.  Instead got " +
                                str(type(projected_finish)))


        if description:
            if isinstance(description, str):
                document['description'] = description
            else:
                raise TypeError("'description' expected to be a string.  " +
                                "Instead got " +
                                str(type(description)))
            
        db = store.organisation['Project']
        oid = str(db.insert(document))

        return Project(oid)
    

