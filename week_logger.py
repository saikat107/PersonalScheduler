import os
import time
import notify2
import pickle
import argparse

from logger_util import WeeklyWorkHour, DailyWorkHour
from logger_util_func import check_screen_on, send_notification, save_data, check_beginning_of_hour, log
from week_stat import main as _week_stat

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--polling_interval', help='Interval of polling (in minutes),', default=5)
    parser.add_argument('--no_daily_notification', action='store_true')
    parser.add_argument('--no_weekly_notification', action='store_true')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--interval_notification', action='store_true')
    args = parser.parse_args()

    save_dir = os.path.join(os.environ['HOME'], '.work_logger')
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    save_path = os.path.join(save_dir, 'log.bin')
    notify2.init('Work Logger')

    if os.path.exists(save_path):
        log('File found!')
        fp = open(save_path, 'rb')
        weeks_data = pickle.load(fp)
        for w in weeks_data:
            if not hasattr(w, 'daily_notification'):
                setattr(w, 'daily_notification', not args.no_daily_notification)
            if not hasattr(w, 'interval_notification'):
                setattr(w, 'interval_notification', args.interval_notification)
            w.daily_notification = not args.no_daily_notification
            w.interval_notification = args.interval_notification
        fp.close()
        log('Total weeks available ', len(weeks_data))
        current_week = weeks_data[-1]
        log('Total days in current week ',
            len(current_week.weekly_hour.keys()))
    else:
        weeks_data = []
        log('Created New Week Data')
        current_week = WeeklyWorkHour(
            daily_notification=(not args.not_daily_notification),
            interval_notification=args.inteval_notification
        )
        weeks_data.append(current_week)

    while True:
        save_data(weeks_data, save_path)
        log('Data saved to ', save_path)
        time.sleep(args.polling_interval * 60)
        if check_screen_on():
            try:
                current_week.add_time(args.polling_interval)
                log(current_week.get_summary(), debug=args.debug)
            except ValueError:
                if not args.no_weekly_notification:
                    _week_stat(5, 40, 8)
                    send_notification(
                        name='Weekly Work Hours!',
                        message=current_week.get_summary()
                    )
                current_week = WeeklyWorkHour()
                weeks_data.append(current_week)
            if check_beginning_of_hour():
                log('Beginning of hour ',
                    current_week.get_summary(),
                    'Today : %0.3f hours' \
                    % current_week.get_day_work_hour().get_total_time()
                    )
                _week_stat(5, 40, 8)
                send_notification(
                    'Beginning of hour ',
                    current_week.get_summary() +
                    ' Today : %0.3f hours' \
                    % current_week.get_day_work_hour().get_total_time()
                )
        pass
