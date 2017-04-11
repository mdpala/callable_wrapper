from .callable_wrapper import CallableWrapper
from functools import wraps
from threading import Thread

def run_async_thread(log=None, callbackFunc=None):
    '''
    def printCallback(result=None):
        print("CALLBACK DONE")
        print("Return: %s"% result)

    @run_async_thread(callbackFunc=printCallback)
    def print_info(**kwargs):
        from time import sleep
        print('starting print_info')
        sleep(2)
        print('print_info: still working')
        sleep(2)
        print ('print_info: finished')
        return 'DONE'
    '''
    def wrapper(func):
        @wraps(func)
        def async_func(*args, **kwargs):
            toCall = ThreadedCall(func, log, True, callbackFunc, *args, **kwargs)
            toCall.start()
            return toCall

        return async_func
    return wrapper 

class ThreadedCall(CallableWrapper):
    def __init__(self, func, log, raiseException=True, doneCallback=None, *args, **kwargs):
        self.thread = Thread(target = self.execute)
        self.thread.setDaemon(True)
        super(ThreadedCall, self).__init__(func, log, raiseException, doneCallback, *args, **kwargs)

    def start(self):
        self.thread.start()

    def set_callback_on_done(self, callbackFunc):
        self.doneCallback = callbackFunc