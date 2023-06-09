# The main functions for CLI control

from argparse import ArgumentParser
from calendar_generator.HTMLTemplate import HTMLTemplate


def get_arguments():
    """
    Get the arguments from the command line, validate them and return them.
    """
    parser = ArgumentParser()
    parser.description = "Generate a HTML calendar for a given year"
    
    parser.add_argument("year", type=int, help="The year to generate the calendar for")
    parser.add_argument("file", type=str, help="The output file name")

    args = parser.parse_args()

    if args.year < 1582 or args.year > 2398:
        raise ValueError("The year must be after 1582 and before 2399")

    return args

def main():
    """
    Takes the arguments from the command line and generates a calendar for the given year, saving it to 
    the given file.
    """
    args = get_arguments()

    html_calendar = HTMLTemplate().format(args.year)

    with open(args.file, "w", encoding="utf-8") as output_file:
        output_file.write(html_calendar)

if __name__ == "__main__":
    main()