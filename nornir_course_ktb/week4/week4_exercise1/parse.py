import re

def parse_uptime(uptime_str):
        """
        Extract the uptime string from the given Cisco IOS Device.
        Return the uptime in seconds as an integer
        """
        # Initialize to zero
        (years, weeks, days, hours, minutes) = (0, 0, 0, 0, 0)

        uptime_str = uptime_str.strip()
        time_list = uptime_str.split(",")
        for element in time_list:
            if re.search("year", element):
                years = int(element.split()[0])
            elif re.search("week", element):
                weeks = int(element.split()[0])
            elif re.search("day", element):
                days = int(element.split()[0])
            elif re.search("hour", element):
                hours = int(element.split()[0])
            elif re.search("minute", element):
                minutes = int(element.split()[0])

        uptime_sec = (
            (years * 31536000) # seconds in a year
            + (weeks * 604800) # seconds in a week
            + (days * 86400) # seconds in a day
            + (hours * 3600)
            + (minutes * 60)
        )
        return uptime_sec