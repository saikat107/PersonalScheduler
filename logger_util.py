import inspect
import os
import pickle
import time

import notify2


class DailyWorkHour:
    def __init__(self, y, m, d, didx):
        self.year = y
        self.month = m
        self.day = d
        self.total_time = 0
        self.date_idx = didx

    def is_same_date(self, d):
        assert isinstance(d, DailyWorkHour)
        return self.year == d.year and self.month == d.month and self.day == d.day

    def is_previous_day(self):
        localtime = time.localtime()
        y = localtime.tm_year
        m = localtime.tm_mon
        d = localtime.tm_mday
        return (self.year < y) or (self.year == y and self.month < m) \
               or (self.year == y and self.month == m and self.day < d)

    def add_time(self, t=5):
        if self.is_previous_day():
            raise ValueError('Cannot add time to previous day. Create another Object for current day.')
        self.total_time += t

    def get_total_time(self, format='hour'):
        if format == 'hour':
            return self.total_time / 60.0
        else:
            return self.total_time

    def get_formatted_date(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        format = '%d-%d-%d (%s)' % (self.day, self.month, self.year, days[self.date_idx])
        return format


class WeeklyWorkHour:
    def __init__(self,
                 daily_notification=True,
                 interval_notification=True):
        self.daily_notification = daily_notification
        self.interval_notification = interval_notification
        self.weekly_hour = dict()

    def get_day_work_hour(self):
        localtime = time.localtime()
        y = localtime.tm_year
        m = localtime.tm_mon
        d = localtime.tm_mday
        didx = localtime.tm_wday
        if didx not in self.weekly_hour.keys():
            if len(self.weekly_hour.keys()) > 0:
                prev_didx = max(self.weekly_hour.keys())
                prev_day = self.weekly_hour[prev_didx]
                prev_day_total_time = prev_day.get_total_time()
                if self.daily_notification:
                    send_notification(
                        name='Daily Work!',
                        message='%s \nTotal Work %.3f hours\n' % (prev_day.get_formatted_date(), prev_day_total_time)
                    )
            daily_hour = DailyWorkHour(y, m, d, didx)
            self.weekly_hour[didx] = daily_hour
        return self.weekly_hour[didx]

    @property
    def week_ended(self):
        localtime = time.localtime()
        didx = localtime.tm_wday
        return didx < max(self.weekly_hour.keys())

    def add_time(self, t=5.0):
        if len(self.weekly_hour.keys()) > 0 and self.week_ended:
            raise ValueError('Cannot add time to previous Week. Create another Object for current Week.')
        cday = self.get_day_work_hour()
        cday.add_time(t)
        log('Total Daily Work on %s is %.3f hours'
            % (cday.get_formatted_date(), cday.get_total_time()), debug=False)
        if self.interval_notification:
            send_notification(
                'Interval',
                'Today %0.3f\tThis Week %0.3f' % (cday.get_total_time(), self.get_total_time())
            )

    def get_total_time(self, format='hour'):
        total_minutes = 0
        for k in self.weekly_hour.keys():
            total_minutes += self.weekly_hour[k].get_total_time('minute')
        if format == 'hour':
            return total_minutes / 60.0
        else:
            return total_minutes

    def get_summary(self):
        return 'Total work in this week %0.3f hours!' % self.get_total_time()


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