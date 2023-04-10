# Contains the PageFormatter class which generates a HTML page containing a calendar for a given year.

from calendar_generator.YearCalendar import HTMLCalendar
from pathlib import Path


class HTMLTemplate:
    """A class that generates a HTML page containing a calendar for a given year (including the year before and the year after)."""

    def _create_calendar(self) -> HTMLCalendar:
        """Creates a HTMLCalendar object.

        Returns:
            HTMLCalendar: A HTMLCalendar object.
        """
        return HTMLCalendar()

    def _import_css_inline(self) -> str:
        """Imports the css from the style.css file and returns it as a string wrapped in style tags.
        This function is safe from path location.

        Returns:
            str: The css from the style.css file wrapped in style tags.
        """        
        with open(Path(__file__).parent / "style.css", encoding="utf-8") as f:
            return f"""<style>
                {f.read()}
            </style>
            """

    def _generate_html_header(self, year: int) -> str:
        """Generates the html for the head of the page.
        This includes the title, encoding and the css.

        Args:
            year (int): The year to generate the calendar for.

        Returns:
            str: The html for the head of the page.
        """        

        return f"""
        <head>
            <meta charset="UTF-8">
            <title>Calendar for {year - 1}, {year} and {year + 1}</title>
            {self._import_css_inline()}
        </head>
        """

    def _generate_html_body(self, year: int) -> str:
        """Generates the html for the body of the page.
        The body contains 3 calendars, one for the year before, one for the given year and one for the year after.
        These are wrapped in a <body> tag.

        Args:
            year (int): The year to generate the calendar for.

        Returns:
            str: The html for the body of the page.
        """        
        calendar = self._create_calendar()
        return f"""
        <body>
            {calendar.generate_year_html(year - 1)}
            {calendar.generate_year_html(year)}
            {calendar.generate_year_html(year + 1)}
        </body>
        """

    def format(self, year: int) -> str:
        """Generates a HTML page containing a calendar for a given year (including the year before and the year after).

        Args:
            year (int): The year to generate the calendar for.

        Returns:
            str: The HTML page
        """        
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        {self._generate_html_header(year)}
        {self._generate_html_body(year)}
        </html>
        """
