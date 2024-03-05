from datetime import date
import re
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("aunty_acids_guide_to_mayhem")


"""
Learned about validating URL input via this thread on Stackoverflow:
https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
"""
url_regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\
          .?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'   # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def get_event_date():
    """
    Date of the event from user input.
    Found assistance with date validation via this thread on Stackoverflow:
    https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python
    """
    date_is_valid = False
    while date_is_valid is False:
        date_input = input("Please enter the date of the event (yyyy-mm-dd) \n")
        if date_input:  # Validate is not empty
            if len(date_input) == 10:  # Validate length
                if "-" in date_input:  # Validate separator
                    try:
                        valid_date = date.fromisoformat(date_input)
                        date_is_valid = True
                        return valid_date
                    except ValueError:
                        print("Date format invalid, please follow (yyyy-mm-dd)")
                else:
                    print("Date separator invalid, please follow (yyyy-mm-dd)")
            else:
                print("Date format invalid, please follow (yyyy-mm-dd)")
        else:
            print("Date cant be empty, please follow yyyy-mm-dd")


"""
#List of genres for select_genre function.
"""
genres = ["Black Metal", "Blues", "Death Metal", "Stoner", "Rock",
"Doom", "Thrash Metal", "Prog", "Heavy Metal", "Power Metal",
"Jazz", "Funk", "Speed Metal", "Core", "Punk", "Soul", "Psychedelic"]


def select_genre():
    """
    Selecting a genre from the genres list.
    Is required. Loops through until user selected correct option from genres list.
    """
    user_input = input("Please choose a genre. Please Capitalize! (ex. write. Black Metal): \n") 
    while user_input in genres:
        if  "," in user_input:
            user_input.split(",")
            return user_input
        else:
            while user_input not in genres:
                print(f"Incorrect input. Please select a genre \
from the list (Please Capitalize! (ex. write. Black Metal): {genres}.")
                user_input = input("\n")
                if user_input in genres:
                    break              
    return user_input


def get_text_input(input_title, min_len=1):
    """
    Function to validate text-input from user for event_title_info function.
    Text fields can not be empty so at least some characters required.
    """
    input_is_valid = False
    while input_is_valid is False:
        user_input = input(input_title)
        if user_input:
            if len(user_input) >= min_len:
                input_is_valid = True
                return user_input
            else:
                print(f"Input should be at least {min_len} chars")
        else:
            print("Can't be empty")


def get_url():
    """
    Learned about "django url validation regex" via this thread on Stackoverflow:
    https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
    Function for URL input from user. In this case a preview track of artists performing.
    """
    input_is_valid = False
    while input_is_valid is False:
        user_input = input("Enter artist music link \
(enter 'skip' to skip this step) \n")
        input_is_valid = re.match(url_regex, user_input) is not None
        if input_is_valid:
            return user_input
        else:
            if user_input == "skip":  # enables user to skip step.
                return "Link not provided."
            else:
                print("Invalid url. Type skip to skip this option.")


def get_url_map():  #Event location via map
    """
    Function for URL input from user. In this case, a location map.
    """
    input_is_valid = False
    while input_is_valid is False:
        user_input = input("Enter venue/event location map link (Google Maps) \
(enter 'skip map' to skip this step) \n")
        input_is_valid = re.match(url_regex, user_input) is not None
        if input_is_valid:
            return user_input
        else:
            if user_input == "skip":  # enables user to skip step.
                return "Link not provided."
            else:
                print("Invalid url. Type skip to skip this option")


def add_data():
    SHEET.append_row([get_event_date()], table_range = "A2")


def main():
    """
    Run all functions.
    """
    event_day = get_event_date()
    print(f"{genres}.")
    event_genre = select_genre()
    event_title = get_text_input("\nEnter artist(s)/event:\n", 1)
    event_venue = get_text_input("Enter location/venue:\n", 1)
    venue_map = get_url_map()
    event_location = get_text_input("Enter city\n", 3)
    artist_url = get_url()
    print(f"On the menu today! A delicious serving of {event_genre}!")
    print(f"The Mayhem will occur on: {event_day}, \
{event_title} live at {event_venue},({venue_map}), {event_location}. \
You can listen to them at {artist_url}")


print("Welcome to Aunty Acid's Guide to Mayhem, a gig guide!")
print("This app intends to function as a simplistic way \
to create and upload events.")
print("Let's get started! \n")
main()
