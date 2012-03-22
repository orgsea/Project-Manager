import cherrypy


class Resource(object):
    exposed = True
    def __init__(self):
        pass

    def GET(self):
        return "GET"


    def PUT(self):
        return "PUT"



    def POST(self):
        return "POST"



    def DELETE(self):
        return "DELETE"



class Root(object):
    pass

root = Root()

root.orders = Resource()

conf = {
    'global' : {
        'server.socket_host' : '0.0.0.0',
        'server.socket_port' : 8000,
        },
    '/'      : {
        'request.dispatch'   : cherrypy.dispatch.MethodDispatcher(),
        },
    }


cherrypy.quickstart(root, '/', conf)

