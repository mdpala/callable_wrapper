from functools import partial
from collections import namedtuple
import logging

logger = logging.getLogger(__name__)

class CallableWrapper:

    CallResult = namedtuple('Result', 'result status exception callableId')
    (kDone, kError) = range(1, 3)
    _lastid = 1

    def __init__(self, func, log, raiseException=True, doneCallback=None, *args, **kwargs):
        self.callableId = CallableWrapper._lastid
        CallableWrapper._lastid += 1
        self.exception = None
        self.result = None
        self.log = log
        if len(kwargs) or len(args):
            self.callable = partial(func, *args, **kwargs)
        else:
            self.callable = partial(func)
        self.raiseException = raiseException
        self.doneCallback = doneCallback
        self._isDone = False

    def __str__(self):
        return "CallableWrapper ID: {} calling function {} @ module {}, args {}".format(
                self.callableId, self.callable.func.__name__, self.callable.func.__module__, str(self.callable.args))

    def __call__(self):
        return self.start()

    def start(self):
        self.execute()

    def execute(self):
        try:
            exception = None
            result = None
            status = self.kDone
            try:
                result = self.callable()
            except Exception as ex:
                exception = ex
                status = self.kError
                if self.log:
                    self.log("Exception from [%s]: %s" % (self, str(ex)))
                else:
                    logger.exception("Exception from [%s]" % (self))
        finally:
            self._isDone = True
            self.result = CallableWrapper.CallResult(result, status, exception, self.callableId)
            if self.doneCallback:
                self.doneCallback(self.result)
