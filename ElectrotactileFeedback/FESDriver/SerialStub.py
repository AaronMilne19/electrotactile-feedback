# stub serial connection for debugging purposes
class SerialStub(object):
    in_waiting = 0

    def __init__(self, _port, _baudrate):
        self.port = _port
        self.baudrate = _baudrate
        self.response = None

    def write(self, msg):
        print("SerialStub[{},{}]: {}".format(self.port, self.baudrate, msg))

    def read(self, num_bytes):
        if not isinstance(self.response, list):
            return None
        # return everything in buffer if buffer smaller or equal to num_bytes
        if len(self.response) <= num_bytes:
            response = self.response
            self.response = None
            self.in_waiting = 0
        # pop first num_bytes elements from buffer, leaving at least one
        else:
            response = self.response[0:num_bytes]
            self.response = self.response[num_bytes:]
            self.in_waiting = len(self.response)
        # avoid returning single element lists
        return response if len(response) != 1 else response[0]

    def isOpen(self):
        return True

    def close(self):
        pass

    def set_response(self, response):
        self.response = None
        self.in_waiting = 0
        if isinstance(response, list):
            self.response = response
            self.in_waiting = len(self.response)
            return True
        else:
            print("WARNING: response must be instance of list - setting response to None instead.")
            return False


