class ProcessorInterface:
    def __init__(self, data, config):
        self.data = data
        self.config = config

    def handle(self):
        raise NotImplementedError
