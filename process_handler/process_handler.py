try:
    from queue import Queue, Empty
except:
    from Queue import Queue, Empty
from subprocess import Popen, PIPE
import shlex, time, threading
from debug import debug

class process_handler:
    
    def __init__(self, command, debug = True):
        self.stdout = Queue()
        bufferless_command = "stdbuf -i0 -o0 -e0 %s" % (command)
        self.process = Popen(shlex.split(bufferless_command), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        self.enqueue_thread = threading.Thread(target = self.enqueue_stdout_on_thread)
        self.enqueue_thread.start()

    def enqueue_stdout_on_thread(self):
        while True:
            b = self.process.stdout.read(1)
            if b == '':
                break
            self.stdout.put(b)

    def read(self):
        try:
            b = self.stdout.get(False)
            if debug:
                debug(b)
            return b
        except:
            return ''

    #Asynchronous reading with 100ms timeout.
    def read_all(self, delay = 0.1):
        out = ""
        b = ''
        while True:
            while b != '':
                out += b
                b = self.read()
            time.sleep(delay)
            b = self.read()
            if b == '':
                return out

    def write(self, line):
        if debug:
            debug(line)
        self.process.stdin.write(line.encode())

    def write_line(self, line):
        self.write(line + "\n")

    def query_line(self, line):
        self.write_line(line)
        return self.read_all()

    def kill(self):
        self.process.kill()
