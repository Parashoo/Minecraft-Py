import sys

class status_message:
    def __init__(self, msg):
        self.msg = msg
        self.start()

    def start(self):
        sys.stdout.write(self.msg + '... ')
        sys.stdout.flush()

    def complete(self):
        sys.stdout.write('Done\n')
        sys.stdout.flush()
        