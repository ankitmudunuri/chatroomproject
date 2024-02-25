


class ThreadQueue(object):

    def __init__(self):
        self.queueData = []
        self.size = 0

    def push(self, data):
        self.queueData.append(data)
        self.size += 1

    def pop(self):
        if (self.size > 0):
            self.size -= 1
            return self.queueData.pop(0)
        