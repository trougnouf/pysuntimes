#!/usr/bin/env python
"""Print suntimes given a date and a set of coordinates."""
import ephem
import sys
import datetime
import timezonefinder
import pytz

def convert_coordinates(coord):
    """
    Convert coordinates from 'N 19° 40.946' or 'W 156° 01.943' format to decimal.
    """
    try:
       return float(coord)
    except ValueError:
        direction = coord[0]
        parts = coord[1:].split('°')
        degrees = float(parts[0])
        minutes = float(parts[1].replace('\'', ''))
        decimal = degrees + minutes / 60
        if direction in ['S', 'W']:
            decimal *= -1
        return decimal

def get_twilight_and_golden_hour_times(date, lat, lon, utc=False):
    """
    Calculate twilight times and golden hour for a given date and location.
    """
    observer = ephem.Observer()
    observer.date = datetime.datetime.strptime(date, '%Y-%m-%d')
    observer.lat, observer.lon = str(convert_coordinates(lat)), str(convert_coordinates(lon))

    sun = ephem.Sun(observer)

    tf = timezonefinder.TimezoneFinder()
    timezone_str = tf.timezone_at(lat=convert_coordinates(lat), lng=convert_coordinates(lon))
    timezone = pytz.timezone(timezone_str)

    # Convert ephem time to local time
    def to_local_time(utctime):
        if isinstance(utctime, datetime.datetime):
            utc_dt = pytz.utc.localize(utctime)
        else:
            utc_dt = pytz.utc.localize(utctime.datetime())
        local_dt = utc_dt.astimezone(timezone)
        return local_dt

    observer.horizon = '6'  # Golden hour
    golden_hour_begin = observer.previous_rising(sun, use_center=True)
    golden_hour_end = observer.next_setting(sun, use_center=True)

    # Calculate twilight times with specific horizon adjustments
    observer.horizon = '0'  # Civil twilight
    sunrise = observer.previous_rising(sun, use_center=True)
    sunset = observer.next_setting(sun, use_center=True)

    # Calculate twilight times with specific horizon adjustments
    observer.horizon = '-6'  # Civil twilight
    civil_twilight_begin = observer.previous_rising(sun, use_center=True)
    civil_twilight_end = observer.next_setting(sun, use_center=True)

    observer.horizon = '-12'  # Nautical twilight
    nautical_twilight_begin = observer.previous_rising(sun, use_center=True)
    nautical_twilight_end = observer.next_setting(sun, use_center=True)

    observer.horizon = '-18'  # Astronomical twilight
    astronomical_twilight_begin = observer.previous_rising(sun, use_center=True)
    astronomical_twilight_end = observer.next_setting(sun, use_center=True)

    if utc:
        return {
        # UTC Times in chronological order
        'Astronomical Twilight Begin (UTC)': astronomical_twilight_begin.datetime(),
        'Nautical Twilight Begin': nautical_twilight_begin.datetime(),
        'Civil Twilight Begin': civil_twilight_begin.datetime(),
        'Sunrise': sunrise.datetime(),
        'Golden Hour End': golden_hour_begin.datetime(),
        'Golden Hour Begin': golden_hour_end.datetime(),
        'Sunset': sunset.datetime(),
        'Civil Twilight End': civil_twilight_end.datetime(),
        'Nautical Twilight End': nautical_twilight_end.datetime(),
        'Astronomical Twilight End': astronomical_twilight_end.datetime()}
    else:
        return {
        # Local Times in chronological order
        'Astronomical Twilight Begin (Local)': to_local_time(astronomical_twilight_begin),
        'Nautical Twilight Begin': to_local_time(nautical_twilight_begin),
        'Civil Twilight Begin': to_local_time(civil_twilight_begin),
        'Sunrise': to_local_time(sunrise.datetime()),
        'Golden Hour End': to_local_time(golden_hour_begin),
        'Golden Hour Begin': to_local_time(golden_hour_end),
        'Sunset': to_local_time(sunset.datetime()),
        'Civil Twilight End': to_local_time(civil_twilight_end),
        'Nautical Twilight End': to_local_time(nautical_twilight_end),
        'Astronomical Twilight End': to_local_time(astronomical_twilight_end),
        }

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        print("Usage: python script.py <date> \"<lat>\" \"<lon>\"")
        print("eg: python suntimes.py 2023-01-02 \"N 19° 40.946'\" \"W 156° 01.943'\"")
        print("or: python suntimes.py 2024-04-02 50.1313 4.5005")
        sys.exit(1)
    utc = '--utc' in sys.argv

    date = sys.argv[1]
    lat = sys.argv[2]
    lon = sys.argv[3]

    times = get_twilight_and_golden_hour_times(date, lat, lon, utc=utc)
    for event, time in times.items():
        if utc:
            print(f"{event}: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        else:
            print(f"{event}: {time.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")

