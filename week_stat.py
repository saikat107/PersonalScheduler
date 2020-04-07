import os
import argparse
import pickle
from matplotlib import pyplot as plt
from logger_util import DailyWorkHour, WeeklyWorkHour


def autolabel(fig, rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        fig.annotate('%.2f' % height,
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def main(previous_weeks, weekly_goal, daily_goal):
    save_dir = os.path.join(os.environ['HOME'], '.work_logger')
    save_path = os.path.join(save_dir, 'log.bin')
    fp = open(save_path, 'rb')
    weeks_data = pickle.load(fp)
    fp.close()
    weekly_work_hours = []
    weekly_goal_achieved = []
    for wi in range(1, previous_weeks + 1):
        hour_this_week = 0
        if wi <= len(weeks_data):
            week = weeks_data[0 - wi]
            assert isinstance(week, WeeklyWorkHour)
            hour_this_week = week.get_total_time()
        weekly_work_hours.append(hour_this_week)
        weekly_goal_achieved.append("red" if hour_this_week < weekly_goal else "green")
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
        daily_goal_achieved.append("red" if hours_today < daily_goal else "green")
    plt.figure("Statistics")
    fig = plt.subplot(211)
    bars = plt.bar(['W %d' % (t + 1) for t in list(range(len(weekly_work_hours)))],
                   weekly_work_hours, color=weekly_goal_achieved)
    autolabel(fig, bars)
    plt.hlines(weekly_goal, -2, previous_weeks, label='Goal', color='blue')
    plt.legend(loc='lower left')
    plt.ylabel('Weekly Hours')
    plt.grid(True)
    fig = plt.subplot(212)
    bars = plt.bar(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], daily_work_hours, color=daily_goal_achieved)
    plt.hlines(daily_goal, -2, 7, label='Goal', color='blue')
    plt.legend(loc='lower left')
    plt.ylabel('Daily Hours')
    plt.grid(True)
    autolabel(fig, bars)
    plt.show()
    plt.savefig(os.path.join(save_dir, 'stat.png'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', help='Path of the saved data.', default='work_hour.bin')
    parser.add_argument('--previous_weeks', help='Stats for number of previous weeks', type=int, default=5)
    parser.add_argument('--weekly_goal', type=float, default=40)
    parser.add_argument('--daily_goal', type=float, default=8)

    args = parser.parse_args()
    d = args.data
    pw = args.previous_weeks
    wg = args.weekly_goal
    dg = args.daily_goal

    main(pw, wg, dg)
    pass