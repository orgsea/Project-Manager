import sys
#make sure this is Python >=3.2
assert sys.version_info.major >= 3 and sys.version_info.minor >= 2, "Needs to be run under Python 3.2"

import pymongo
import bson

"""
The host to connect to.  Defaults to None and thus will assume mongodb is on localhost.
"""
HOST=None
"""
The port to connect to, if None will assume it to be the default mongodb port number.
"""
PORT=None


"""
The mongodb connection connecting to  HOST and PORT
"""
mongo_connection = pymongo.connection.Connection(HOST, PORT)
organisation = mongo_connection.organisation


class Store(object):
    def __init__(self, oid):
        """
        Connects to the DB and retrieves the record for the oid stored in the DB
        """
        self._db = organisation[self.type]
        oid = bson.ObjectId(oid)
        self._document = self._db.find_one({'_id':oid})
        if self._document:
            #ObjectId stored for later reference
            self._id = oid
            #make it easier to update later since mongo does not allow _id to be modified
            del self._document['_id']
        else:
            raise KeyError("Object with _id of " + str(oid) + " doesn't exist")

    
    @property
    def type(self):
        """
        The type of model this object represents.  It should match the name of the referenced class instance.
        """
        return self.__class__.__name__


    @property
    def id(self):
        """
        The unique id used to uniquely identify the database entry
        """
        return str(self._id)


    @property
    def document(self):
        """
        The raw database entry record from the database in dict form
        """
        return self._document


    @staticmethod
    def create(*args, **kwargs):
        raise NotImplementedError('Store.create is not ment to be used')
    
