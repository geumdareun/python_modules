import sys, threading

debug_lock = threading.Lock()

def debug(b):
    debug_lock.acquire()
    sys.stdout.write(b)
    sys.stdout.flush()
    debug_lock.release()
    
def debug_line(line):
    debug(line + "\n")