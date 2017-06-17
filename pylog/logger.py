#!/usr/bin/env python

from __future__ import print_function
import sys
import os.path
import time
import logging
import inspect


global _verboseFlag, _debugFlag, _logger
_verboseFlag = False
_debugFlag = False
_logger = None


class CustomLogFormatter(logging.Formatter, object):

    def __init__(self, verbose=False, debug=False):
        self.fmt = "%(message)s"
        if verbose is True:
            self.fmt = "%(levelname)-8s %(message)s"
        if debug is True:
            self.fmt = "%(levelname)-8s  %(asctime)s  %(callerFile)-20s %(callerLine)-6d %(callerFunc)-32s %(message)s"
        super(CustomLogFormatter, self).__init__(fmt=self.fmt)

    def formatException(self, exc_info):
        "Format exception messages."
        text = logging.Formatter.formatException(self, exc_info)
        text = '\n'.join(('! %s' % line) for line in text.splitlines())
        return text


class Logger(object):

    def __init__(self, verbose=False, debug=False, filename=None, stream=sys.stdout):
        self._logger = logging.getLogger()
        if self._logger.handlers:
            for handler in self._logger.handlers:
                self._logger.removeHandler(handler)
        formatter = CustomLogFormatter(verbose=verbose, debug=debug)
        handler = logging.StreamHandler(stream)
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        if filename:
            handler = logging.FileHandler(filename)
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
        if debug:
            self._logger.setLevel(logging.DEBUG)
        elif verbose:
            self._logger.setLevel(logging.INFO)
        else:
            self._logger.setLevel(logging.WARNING)

    def _getStackFrame(self, offset=0):
        _, fname, lineno, func, _, _ = inspect.getouterframes(inspect.currentframe())[offset]
        extra = {
            'callerFile': os.path.basename(fname),
            'callerLine': lineno,
            'callerFunc': func
        }
        return extra

    def _message(self, func, msg, *args, **kwargs):
        if "extra" in list(kwargs.keys()):
            ret = func(msg, *args, **kwargs)
        else:
            ret = func(msg, *args, extra=self._getStackFrame(offset=3), **kwargs)
        self.flush()
        return ret

    def debug(self, msg, *args, **kwargs):
        return self._message(self._logger.debug, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        return self._message(self._logger.info, msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        return self._message(self._logger.warn, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        return self._message(self._logger.warning, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        return self._message(self._logger.error, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        return self._message(self._logger.critical, msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        return self._message(self._logger.exception, msg, *args, **kwargs)

    def disable(self):
        logging.shutdown()

    def flush(self):
        if self._logger:
            [h.flush() for h in self._logger.handlers]


def _message(func, msg, *values):
    frame, filename, linenum, funcname, lines, index = \
        inspect.getouterframes(inspect.currentframe())[2]
    extra = {'callerFile': os.path.basename(filename),
             'callerLine': linenum,
             'callerFunc': funcname}
    func(msg, *values, extra=extra)


def flush():
    sys.stdout.flush()
    sys.stderr.flush()


def info(msg, *values):
    if _logger:
        _message(_logger.info, msg, *values)


def debug(msg, *values):
    if _logger:
        _message(_logger.debug, msg, *values)


def warn(msg, *values):
    if _logger:
        _message(_logger.warn, msg, *values)


def error(msg, *values):
    if _logger:
        _message(_logger.error, msg, *values)


def critical(msg, *values):
    if _logger:
        _message(_logger.critical, msg, *values)


def exception(msg, *values):
    if _logger:
        _message(_logger.exception, msg, *values)


def _exit(stacktrace=False, exitcode=0):
    if stacktrace:
        where(useLogger=True)
    flush()
    sys.exit(exitcode)


def exit(msg, stacktrace=False, flushOutput=True, exitcode=0, *values):
    info(msg, *values)
    _exit(stacktrace=False, flushOutput=flushOutput, exitcode=0)


def abort(msg, stacktrace=True, flushOutput=True, *values):
    critical(msg, *values)
    _exit(stacktrace=True, flushOutput=flushOutput, exitcode=1)


def startLogging(verbose=False, debug=False, filename=None):
    global _verboseFlag, _debugFlag, _logger
    _verboseFlag = verbose
    _debugFlag = debug
    _logger = Logger(verbose=verbose, debug=debug, filename=filename)


def stopLogging():
    global _verboseFlag, _debugFlag, _logger
    _verboseFlag = False
    _debugFlag = False
    if _logger:
        _logger.disable()
        _logger = None


def main():
    startLogging(verbose=True, debug=True)
    debug("debug: debug")
    info("debug: info")
    warn("debug: warning")
    error("debug: error")
    critical("debug: critical")
    stopLogging()


if __name__ == '__main__':
    main()
