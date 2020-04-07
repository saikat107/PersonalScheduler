import inspect
import os
import pickle
import time

import notify2


def check_screen_on():
    x = os.popen("xset -q").read()
    return "Monitor is On" in x


def send_notification(name, message, icon_path='stat.png'):
    n = notify2.Notification(None, icon=icon_path)
    n.set_urgency(notify2.URGENCY_NORMAL)
    n.set_timeout(10000)
    n.update(name, message)
    n.show()


def save_data(weeks_data, save_path):
    with open(save_path, 'wb') as fp:
        pickle.dump(weeks_data, fp)
    pass


def check_beginning_of_hour(polling_interval=5):
    minute = time.localtime().tm_min
    return minute < polling_interval


def log(*messages, debug=False):
    if debug:
        caller = inspect.stack()[1]
        fpath = caller.filename
        ln = caller.lineno
        location = "File \"%s\", line %d " % (fpath, ln) + '\t'
    else:
        location = ''
    message = ' '.join([str(m) for m in messages])
    t = time.strftime('%y-%m-%d %H:%M:%S')
    print(location + t + '\t' + message)