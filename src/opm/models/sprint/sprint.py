import opm.models.store as store
import opm.models.project as project
import opm.models.sprint.task as task

class Sprint(store.Store):
    def __init__(self, oid):
        super(Sprint, self).__init__(oid)
