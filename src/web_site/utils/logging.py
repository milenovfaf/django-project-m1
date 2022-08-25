
import logging
import traceback


class Formatter(logging.Formatter):
    def format(self, record):
        record.exc_text = None  # <<<= DO NOT CACHE trice info !
        return super(Formatter, self).format(record)


class DetailFormatter(Formatter):
    def formatException(self, ei):
        """ enable local variables to trace back of exception """
        try:
            tb_render = traceback.TracebackException(
                ei[0], ei[1], ei[2], capture_locals=True)
            return ''.join(tb_render.format(chain=True))
        except TypeError:
            return super(DetailFormatter, self).formatException(ei)
#
