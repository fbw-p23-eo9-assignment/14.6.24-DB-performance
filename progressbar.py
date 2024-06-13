"""Utils."""

import json
import sys

from django.conf import settings


class ProgressBar:
    """Progress bar."""

    total = 0
    log = None
    _log = None
    _current = 0
    _done = 0
    _perc_done = float(0)

    def __init__(self, width=50, todo_character='-', done_character='#',
                 logfile=None):
        """Constructor."""
        self.width = width
        self.todo_character = todo_character
        self.done_character = done_character
        self.logfile = logfile
        self.logpath = ''

    def log_init(self, log=None):
        """Initialize log."""
        self._log = log
        self.save_log()

    def save_log(self):
        """Save the log file."""
        if self.logfile:
            self.logpath = settings.BASE_DIR + '/uploads/logs/' + self.logfile
            file = open(self.logpath, 'w')
            file.write(json.dumps(list(self._log)))
            file.close()

    def start(self, total=0, width=None, title=None):
        """Initialize bar."""
        self.total = total
        self._done = 0
        self._perc_done = 0
        if self.logfile:
            self.log = self._log[self._current]
            self._current = self._current + 1
            if title:
                self.log['title'] = str(title)
            self.log['total'] = self.total
            self.save_log()
        else:
            if width:
                self.width = width
            if title:
                self._print_title(title)
            step_width = self.width / 10 - 1
            steps = [' ' * int(step_width) for step in range(10)]
            print(" {}".format('·'.join(steps)))
            sys.stdout.write("0%")
            for step in range(1, 11):
                sys.stdout.write(" " * (int(step_width) - 2))
                sys.stdout.write("{}0%".format(str(step)))
            sys.stdout.write("\n")
            sys.stdout.flush()

            sys.stdout.write("[{}]".format(self.todo_character * (self.width)))
            sys.stdout.flush()
            sys.stdout.write("\b" * (self.width + 1))
        self.tick(0)

    def tick(self, count):
        """Tick the bar."""
        perc = 100
        if self.total:
            perc = 100 * float(count) / float(self.total)
        if self.logfile:
            self.log['done'] = count
            if count == self.total or (perc - self._perc_done >= 0.01):
                self._perc_done = perc
                self.save_log()
        else:
            position = int((count / self.total) * self.width)
            if position - self._done >= 1:
                increment = position - self._done
                self._done = position
                sys.stdout.write(self.done_character * increment)
                sys.stdout.flush()

            label = "{}{}%".format(
                self.todo_character,
                str(round(perc, 2))
            )
            sys.stdout.write(label)
            sys.stdout.write("\b" * (len(label)))
            sys.stdout.flush()

    def finish(self):
        """Finish the bar."""
        if self.logfile:
            self.tick(self.total)
        else:
            increment = int(self.width) - self._done
            sys.stdout.write(self.done_character * increment)
            sys.stdout.flush()
            sys.stdout.write("]          \n\n")

    def end(self):
        """Alias."""
        self.finish()

    def _print_title(self, title):
        """Print the title."""
        empty_left = ">" * (int((self.width - len(title)) / 2) - 1)
        empty_right = "<" * (int((self.width - len(title)) / 2) - 1)
        sys.stdout.write("{} {} {}<\n".format(empty_left, title.upper(),
                                              empty_right))
        sys.stdout.flush()
