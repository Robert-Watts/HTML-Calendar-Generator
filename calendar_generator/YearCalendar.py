# Contains the YearCalendar class which generates a calendar for a given year.

# Take a day of the week integer and return the string representation
DAY_TO_STRING = {
    0: "Mon",
    1: "Tues",
    2: "Weds",
    3: "Thurs",
    4: "Fri",
    5: "Sat",
    6: "Sun"
}

# Take a month integer and return the string representation
MONTH_TO_STRING = {
    0: "January",
    1: "February",
    2: "March",
    3: "April",
    4: "May",
    5: "June",
    6: "July",
    7: "August",
    8: "September",
    9: "October",
    10: "November",
    11: "December"
}



class HTMLCalendar:
    """A class that generates a HTML calendar for a given year"""

    @staticmethod
    def is_leap_year(year: int) -> bool:
        """Determins if the given year is a leap year.        
        Returns True if the given year is a leap year, False otherwise.

        Args:
            year (int): The year

        Returns:
            bool: True if the year is a leap year, False otherwise.
        """
        return True if year % 4 == 0 and year % 100 != 0 or year % 400 == 0 else False

    @staticmethod
    def days_in_month(year: int, month: int) -> int:
        """Returns the number of days in the given month of the given year.

        This function takes into account leap years and correct febuary accordingly.

        Args:
            year (int): The year
            month (int): The month (1-12)

        Returns:
            int: The number of days in the month
        """
        if month == 2:
            return 29 if HTMLCalendar.is_leap_year(year) else 28
        elif month in [4, 6, 9, 11]:
            return 30
        else:
            return 31

    @staticmethod
    def day_of_week(year: int, month: int, day: int) -> int:
        """Returns the day of the week for a given date as an integer where monday is 0, tuesday is 1, etc.

        Args:
            year (int): The year
            month (int): The month (1-12)
            day (int): The day within the month

        Returns:
            int: The day of the week that the day falls on.
        """
        MONTH_CODES = {
            1: 0,
            2: 3,
            3: 3,
            4: 6,
            5: 1,
            6: 4,
            7: 6,
            8: 2,
            9: 5,
            10: 0,
            11: 3,
            12: 5
        }

        CENTURY_CODES = {
            15: 0,
            16: 6,
            17: 4,
            18: 2,
            19: 0,
            20: 6,
            21: 4,
            22: 2,
            23: 0
        }

        year_decade = int(str(year)[-2:])

        # Year Code
        # (YY + (YY div 4)) mod 7
        year_code = (year_decade + (year_decade // 4)) % 7

        # Month Code
        month_code = MONTH_CODES[month]

        # Century Code
        century_code = CENTURY_CODES[int(str(year)[:2])]

        # Day Number
        day_number = day

        # Leap Year Code
        leap_year_code = 1 if HTMLCalendar.is_leap_year(year) and month < 3 else 0


        # Using this formula sunday is 0, monday is 1, etc
        # (Year Code + Month Code + Century Code + Day Number - Leap Year Code) mod 7
        day_of_week_formula = (year_code + month_code + century_code + day_number - leap_year_code) % 7

        #Convert the day of the week such that monday is 0, tuesday is 1, etc
        day_of_week = day_of_week_formula - 1 if day_of_week_formula > 0 else 6

        return day_of_week

    
    def generate_month(self, year: int, month: int) -> list:
        """Generates a calendar for a given month of a given year.

        Returns in the form of a matrix where each row is a week and each column is a day.
        Days are represented in the form of a tuple (day number, day of the week)
        e.g. (1, 0) is the first day of the month which is a monday.
        Days that are not in the month are represented as (0, 0).

        Args:
            year (int): The year
            month (int): The month where January is 1 and December is 12

        Returns:
            list: A matrix where each row is a week and each column is a day.
        """

        # Create an array to hold the days padding the start of the moth with 0
        calendar_days = [(0, 0)] * self.day_of_week(year, month, 1)

        for day in range(1, self.days_in_month(year, month) + 1):
            calendar_days.append((day, self.day_of_week(year, month, day)))

        # Pad the end of the month with 0 so that the final week is complete
        while len(calendar_days) % 7 != 0:
            calendar_days.append((0, 0))

        # Split the array into weeks
        return [calendar_days[i:i+7] for i in range(0, len(calendar_days), 7)]

    def generate_month_header(self, month: int) -> str:
        """Generates the header section of a table for a given month.
        The content contains the month name and the days of the week, all
        wrapped in a <tr> tag.

        Args:
            month (int): The month where January is 1 and December is 12

        Returns:
            str: The html for the header section of a table for a given month.
        """
        days = "\n".join(
            [f"<th class=\"day-header\">{DAY_TO_STRING[day]}</th>" for day in range(0, 7)]
        )
        return f"""
        <tr>
            <th colspan="7" class="month-name">{MONTH_TO_STRING[month - 1]}</th>
        </tr>
        <tr>
            {days}
        </tr>
        """

    def generate_week_html(self, week: list) -> str:
        """Generates the html for a week.

        Args:
            week (list): A list of tuples where each tuple represents a day in the week.

        Returns:
            str: The html for a week.
        """
        lines = []

        for day, _ in week:
            # If they day of the week is 0 then it is outside the month so should not have content
            if day == 0:
                day = ""

            lines.append(f"<td>{day}</td>\n")

        return f"""
        <tr>
            {"".join(lines)}
        </tr>
        """

    def generate_month_html(self, year: int, month: int) -> str:
        """Generates a html table for a month.

        Args:
            year (int): The year
            month (int): The month where January is 1 and December is 12

        Returns:
            str: A HTML table containing a calendar for a month.
        """ 
        return f"""
        <table cellpadding="0" cellspacing="0" >
            {self.generate_month_header(month)}
            {"".join([self.generate_week_html(week) for week in self.generate_month(year, month)])}
        </table>
        """

    def generate_year_html(self, year: int) -> str:
        """Generates a html section for a years calendar.
        This contains the year wrapped in a <h1> tag and a <section> tag containing a table 
        for each month.

        Args:
            year (int): The year

        Returns:
            str: A HTML section containing a calendar for a year.
        """
        months_html = []

        for month in range(1, 13):
            months_html.append(f"<div>{self.generate_month_html(year, month)}</div>")

        return f"""
        <article style="postion: relative">
        <h1 class="year">{year}</h1>
        <section class="grid">
        
        {"".join(months_html)}
        </section>
        </article>
        """
