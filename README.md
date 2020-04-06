# Self Scheduler for Work From Home. 

------

This is a simple work logger. This is implemented based on polling the screen. If the computer screen is on, we assumed the user is working. If the scheduler is running, beginning of every day (12.00 am) and beginning of every week, it will send a desktop notification.
  

### Requirements
1. ``Python >= 3.6``
2. ``dbus-python == 1.2.16``
3. ``notify2 == 0.3.1``
#### Step1: 
Install all the requirements
```shell script
    pip install dbus-python==1.2.16
    pip install notify2==0.3.1
```
#### Step2: 
Clone this repository
```shell script
    git clone https://www.github.com/saikat107/PersonalScheduler.git
```
#### Step3: 
Install this tool
```shell script
    cd PersonalScheduler
    bash install.sh
```
### Usage
1. Run ``start_logger`` to start the logger. (N.B. if the logger is already running, it will not create another logger.)
2. To see the statistics, run ``work_stat``. 

---

#### Feel free to fork and report any issue. 
