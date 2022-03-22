try:
    import ADL as ADL
except:
    pass

class Amot:

    @staticmethod
    def starter():
        return AmotRuntime.getInstance().run()

    @staticmethod
    def attached(component):
        return AmotRuntime.getInstance().attached(component)

class AmotRuntime():
    _instance = None

    @staticmethod
    def setInstanceWith(ip, env):
        if AmotRuntime._instance == None:
            AmotRuntime._instance = AmotRuntime(ip, env)
    
    @staticmethod
    def getInstance():
        return AmotRuntime._instance

    def __init__(self, ip, env):
        self.ip = ip
        self.env = env

        #set configurations
        self.current_components = self.loadComponents()
        self.attachments = ADL.adl["attachments"]
        print(self.attachments)
        self.configuration = ADL.adl["configuration"]

        self.app = None

    def main(self, app):
        self.app = app

        self.app.setup()

        while True:
            try:
                self.app.loop()
            except OSError as err:
                print(err) 
    

    def loadComponents(self):
        current_components = {}
        components = ADL.adl["components"]

        for component in components:
            namespace = __import__("Components."+ component)
            component_module = getattr(namespace, component)
            component_instance = getattr(component_module, component)
            current_components[component] = component_instance()
        return current_components

    
    def run(self):
        return self.current_components[self.configuration["start"]]

    
    def attached(self, component):
        class_name = component.__class__.__name__
        next_class = self.attachments.get(class_name)
        next_object = self.current_components[next_class]
        return next_object