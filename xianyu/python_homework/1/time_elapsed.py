# constant variables
MINUTES_PER_HOUR = 60
HOURS_PER_DAY = 24
HOURS_PER_HALF_DAY = 12
MINUTES_PER_DAY = HOURS_PER_DAY * MINUTES_PER_HOUR
MINUTES_PER_HALF_DAY = HOURS_PER_HALF_DAY * MINUTES_PER_HOUR

# get minutes since mid night from user input
elapsed_minutes = int(raw_input('Minutes since mid night: '))

# calculate the End time
minutes_since_today = elapsed_minutes % MINUTES_PER_DAY
end_time_str = ''
if minutes_since_today >= MINUTES_PER_HALF_DAY:
    minutes_since_noon = minutes_since_today - MINUTES_PER_HALF_DAY
    if minutes_since_noon >= MINUTES_PER_HOUR:
        hour = minutes_since_noon // MINUTES_PER_HOUR
        minutes = minutes_since_noon % MINUTES_PER_HOUR
        hour_str = str(hour)
        if minutes <= 9:
            minutes_str = '0' + str(minutes)
        else:
            minutes_str = str(minutes)
        end_time_str = hour_str + ':' + minutes_str + 'pm'
    else:
        # use 12:50pm rather than 0:50pm
        hour_str = '12'
        minutes = minutes_since_noon % MINUTES_PER_HOUR
        if minutes <= 9:
            minutes_str = '0' + str(minutes)
        else:
            minutes_str = str(minutes)
        end_time_str = hour_str + ':' + minutes_str + 'pm'
else:
    if minutes_since_today >= MINUTES_PER_HOUR:
        hour = minutes_since_today // MINUTES_PER_HOUR
        minutes = minutes_since_today % MINUTES_PER_HOUR
        hour_str = str(hour)
        if minutes <= 9:
            minutes_str = '0' + str(minutes)
        else:
            minutes_str = str(minutes)
        end_time_str = hour_str + ':' + minutes_str + 'am'
    else:
        # use 12:50am rather than 0:50am
        hour_str = '12'
        minutes = minutes_since_today % MINUTES_PER_HOUR
        if minutes <= 9:
            minutes_str = '0' + str(minutes)
        else:
            minutes_str = str(minutes)
        end_time_str = hour_str + ':' + minutes_str + 'am'

# output
print('Start time: 12:00am')
print('End time: ' + end_time_str)


