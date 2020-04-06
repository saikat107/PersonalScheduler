import os
import argparse
import pickle
from matplotlib import pyplot as plt
from week_logger import WeeklyWorkHour, DailyWorkHour


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', help='Path of the saved data.', default='work_hour.bin')
    parser.add_argument('--previous_weeks', help='Stats for number of previous weeks', type=int, default=5)
    parser.add_argument('--weekly_goal', type=float, default=40)
    parser.add_argument('--daily_goal', type=float, default=8)

    args = parser.parse_args()

    save_dir = os.path.join(os.environ['HOME'], '.work_logger')
    save_path = os.path.join(save_dir, 'log.bin')
    fp = open(save_path, 'rb')
    weeks_data = pickle.load(fp)
    fp.close()
    weekly_work_hours = []
    weekly_goal_achieved = []
    for wi in range(1, args.previous_weeks + 1):
        hour_this_week = 0
        if wi <= len(weeks_data):
            week = weeks_data[0 - wi]
            assert isinstance(week, WeeklyWorkHour)
            hour_this_week = week.get_total_time()
        weekly_work_hours.append(hour_this_week)
        weekly_goal_achieved.append("red" if hour_this_week < args.weekly_goal else "green")
    weekly_work_hours = weekly_work_hours[::-1]
    weekly_goal_achieved = weekly_goal_achieved[::-1]
    running_or_prev_week = weeks_data[-1]
    assert isinstance(running_or_prev_week, WeeklyWorkHour)
    daily_work_hours = []
    daily_goal_achieved = []
    for di in range(7):
        hours_today = 0
        if di in running_or_prev_week.weekly_hour.keys():
            today = running_or_prev_week.weekly_hour[di]
            assert isinstance(today, DailyWorkHour)
            hours_today = today.get_total_time()
        daily_work_hours.append(hours_today)
        daily_goal_achieved.append("red" if hours_today < args.daily_goal else "green")

    plt.figure("Statistics")
    plt.subplot(211)
    plt.bar(['W %d' % (t + 1) for t in list(range(len(weekly_work_hours)))],
            weekly_work_hours, color=weekly_goal_achieved)
    plt.hlines(args.weekly_goal, -2, args.previous_weeks, label='Goal', color='blue')
    plt.legend(loc='lower left')
    plt.ylabel('Weekly Hours')
    plt.grid(True)
    plt.subplot(212)
    plt.bar(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], daily_work_hours, color=daily_goal_achieved)
    plt.hlines(args.daily_goal, -2, 7, label='Goal', color='blue')
    plt.legend(loc='lower left')
    plt.ylabel('Daily Hours')
    plt.grid(True)
    plt.show()
    pass