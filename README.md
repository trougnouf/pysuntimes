# pysuntimes
Print suntimes given a date and a set of coordinates. (civil/nautical/astronomical twilights, sunset/sunrise, and golden hours)

Usage: `python script.py <date> "<lat>" "<lon>"`

Default is (auto-detected) local-time, `--utc` flag can be added to the command line.

Dependencies: pytz, ephem, timezonefinder

eg: `python suntimes.py 2023-01-02 "N 19° 40.946'" "W 156° 01.943'"`

```
[trougnouf@bd ~]$ python scripts/suntimes.py 2023-01-02 "N 19° 40.946'" "W 156° 01.943'"
Astronomical Twilight Begin (Local): 2023-01-01 05:40:22 HST-1000
Nautical Twilight Begin: 2023-01-01 06:07:25 HST-1000
Civil Twilight Begin: 2023-01-01 06:34:07 HST-1000
Sunrise: 2023-01-01 06:59:57 HST-1000
Golden Hour End: 2023-01-01 07:30:13 HST-1000
Golden Hour Begin: 2023-01-01 17:25:22 HST-1000
Sunset: 2023-01-01 17:55:37 HST-1000
Civil Twilight End: 2023-01-01 18:21:28 HST-1000
Nautical Twilight End: 2023-01-01 18:48:09 HST-1000
Astronomical Twilight End: 2023-01-01 19:15:11 HST-1000
```

or: `python suntimes.py 2024-04-02 50.1313 4.5005`

```
[trougnouf@bd scripts]$ python suntimes.py 2024-04-02 50.1313 4.5005
Astronomical Twilight Begin (Local): 2024-04-01 05:23:24 CEST+0200
Nautical Twilight Begin: 2024-04-01 06:05:25 CEST+0200
Civil Twilight Begin: 2024-04-01 06:43:57 CEST+0200
Sunrise: 2024-04-01 07:19:31 CEST+0200
Golden Hour End: 2024-04-01 07:59:40 CEST+0200
Golden Hour Begin: 2024-04-02 19:34:09 CEST+0200
Sunset: 2024-04-02 20:14:27 CEST+0200
Civil Twilight End: 2024-04-02 20:50:13 CEST+0200
Nautical Twilight End: 2024-04-02 21:29:07 CEST+0200
Astronomical Twilight End: 2024-04-02 22:11:44 CEST+0200
```
