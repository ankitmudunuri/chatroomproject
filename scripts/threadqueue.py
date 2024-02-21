
class ThreadQueue(object):

    def __init__(self):
        self.queueData = []

    def push(self, data):
        self.queueData.append(data)

    def pop(self):
        return self.queueData.pop(0)