"""
Bike Share Python Analysis Project
Feb 2021
"""

import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def input_validation(input_question, input_expected):
    """
    Validates input against standard exception errors and expected values.

    Arg:
        (str) input_question - str containing question to be printed for user
        (list) input_expected - list of expected values to test initial user_input against
    Returns:
        (str) user_input - validated input
    """
    input_expected = [x.lower() for x in input_expected]
    # Use a while loop to handle invalid inputs
    # heavy inspiration from the following excellent stackoverflow post
    # https://stackoverflow.com/questions/23294658/

    while True:
        try:
            user_input = (input(input_question)).lower()
        except KeyboardInterrupt:
            print("Please don't interrupt - no input taken.")
            print()
            continue
        except ValueError:
            print("Sorry, I didn't understand that.")
            print()
            continue

        if user_input not in input_expected:
            # validates input against expected values
            print("Your input was invalid - please try again.")
            print()
            continue
        else:
            break

    print('-' * 40)
    return user_input


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US Bike Share data!')
    cities = ['Chicago', 'New York City', 'Washington']

    while True:
        city = input_valid("Which city would you like to analyze? Chicago, New York City, or Washington: ", cities)
        confirm = input_valid("Just to confirm - {}? Enter y/n ".format(city.title()), ['y', 'n'])
        if confirm == 'y':
            # input is successfully parsed, let's exit the loop
            print("Awesome - time to dive into the data!")
            print()
            break
        else:
            # back to the top, we'll ask again
            print()
            continue

    # get user input for time filters
    # listing out time filters based on what's available with the dataset
    filters = ['month', 'day', 'both', 'none']
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    question = "Would you like to filter the data by month, day, or both? Type 'none' for no time filter: "
    time_filter = input_valid(question, filters)

    if time_filter == 'none':
        month = 'all'
        day = 'all'
        print("Alright, we\'ll move forward with no filters applied.")
        print()
    elif time_filter == 'both':
        month = input_valid("\nWhich month? January, February, March, April, May, or June? ", months)
        day = input_valid("Which weekday? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday? ", days)
        print("Alright, we\'ll filter for {}s in {}.".format(day.title(), month.title()))
        print()
    elif time_filter == 'month':
        month = input_valid("\nWhich month? January, February, March, April, May, or June? ", months)
        day = 'all'
        print("Alright, we\'ll filter only for {}.".format(month.title()))
        print()
    else:
        day = input_valid("Which weekday? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday? ", days)
        month = 'all'
        print("Alright, we\'ll filter only for {}s.".format(day.title()))
        print()
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    filename = (CITY_DATA[city])
    df = pd.read_csv(filename)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month_int = months.index(month.title()) + 1
        # Month goes from 1 to 12 inclusive, need to add 1 to index accordingly

        # filter by month to create the new dataframe
        df = df[(df['month'] == month_int)]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the weekdays list to get the corresponding int
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_int = weekdays.index(day.title())

        # filter by day of week to create the new dataframe
        df = df[(df['day_of_week'] == day_int)]

    # Basic Data Cleaning
    # rename unnamed first column to ride_id
    df = df.rename(columns={'Unnamed: 0': 'ride_id'})
    # Replace null Gender values with 'Undisclosed'
    if 'Gender' in df.columns:
        df['Gender'] = df['Gender'].fillna("Undisclosed")
    return df


def df_info(df):
    """Displays information on the selected dataset"""
    # Number of rows, first value from shape tuple
    obs = df.shape[0]

    # Covert date range of dataset to a more readable format
    # Doc reference: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
    start_date = df['Start Time'].min().strftime("%d %b, %Y")
    end_date = df['Start Time'].max().strftime("%d %b, %Y")

    print("The selected dataset contains {} observations, ranging from {} to {}.".format(obs, start_date, end_date))


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month utilizing mode()
    popular_month = df['month'].mode().values[0] - 1
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print("The most common month is {}.".format(months[popular_month]))

    # display the most common day of week
    popular_day = df['day_of_week'].mode().values[0]
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    print("The most common day of the week is {}.".format(weekdays[popular_day]))

    # extract hour from the Start Time column to create a start_hour column
    df['start_hour'] = df['Start Time'].dt.hour

    # display the most common start hour
    popular_hour = df['start_hour'].mode().values[0]
    print("The most common start hour is {}.".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_st = df['Start Station'].mode().values[0]
    print("The most popular starting station is {}.".format(popular_start_st))

    # display most commonly used end station
    popular_end_st = df['End Station'].mode().values[0]
    print("The most popular final station is {}.".format(popular_end_st))

    # display most frequent combination of start station and end station trip
    # use of idxmax inspired by https://stackoverflow.com/questions/53037698/
    popular_combo = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("The most popular start-end trip is {}.".format(popular_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # convert the Trip Duration column (seconds) to timedelta
    # Doc Reference: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_timedelta.html
    df['Trip Duration'] = pd.to_timedelta(df['Trip Duration'], unit='s')

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print("The total travel time of the selected trips is {}.".format(total_time))

    # display mean travel time
    avg_time = df['Trip Duration'].mean()
    print("The average travel time of the selected trips is {}".format(avg_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bike share users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # The Chicago dataset has a third unique user type, "Dependent", so we'll have to adjust for that.
    # The New York City dataset has missing values.
    for index, value in df['User Type'].value_counts(dropna=False).items():
        # Doc Reference: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.items.html
        print("There are", value, "users of the", index, "user type.")
    print()

    # Display counts of gender
    # The Washington dataset doesn't include the 'Gender' column so we need to check for it
    if 'Gender' in df.columns:
        for index, value in df['Gender'].value_counts(dropna=False).items():
            print("There are", value, "users of the", index, "gender category.")
        print()

        print("The following is a Gender breakdown by User Type:")
        print(df.groupby(['User Type', 'Gender']).size().reset_index(name='Count'))
        # Group By Count Reference: https://www.statology.org/pandas-groupby-count/
        # including dropna in Group By: https://stackoverflow.com/questions/18429491/
        print()
    else:
        print("Gender is not available for this dataset.")
        print()

    # Display earliest, most recent, and most common year of birth
    # The Washington dataset doesn't include the 'Birth Year' column so we need to check for it
    if 'Birth Year' in df.columns:
        print("The earlier Birth Year in this dataset is", int(df['Birth Year'].min()))
        print("The most recent Birth Year in this dataset is", int(df['Birth Year'].max()))
        print("The most common Birth Year in this dataset is", int(df['Birth Year'].mode()))
    else:
        print("Birth Year is not available for this dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """ Displays raw individual trip data from the selected dataset"""
    print('\nDisplaying Raw Data...\n')
    i = 0
    while i < df.shape[0]:
        print(df[i:i+5])
        view_more = input('\n Would you like to see more? Enter yes or no. ')
        if view_more.lower() == 'yes':
            i += 5
            continue
        else:
            break
    print('-' * 40)


def quest(df):
    """ Asks user to specify what statistics they would like to see, or if they'd like to see raw data"""
    while True:
        try:
            print("""
            What would you like to examine today?
            1 - Display statistics on the most frequent times of travel
            2 - Display statistics on the most popular stations and trip
            3 - Display statistics on the total and average trip duration
            4 - Display statistics on bike share users
            5 - Show me raw trip data
            6 - Exit the program
            """)
            selection = input("Please enter your selection by the corresponding number e.g. 4=bike share users ")
        except KeyboardInterrupt:
            print("Please don't interrupt - no input taken.")
            print()
            continue
        except ValueError:
            print("Sorry, I didn't understand that.")
            print()
            continue

        if selection not in ['1', '2', '3', '4', '5', '6']:
            # validates input against expected values
            print("Your input was invalid - please try again.")
            print()
            continue
        elif selection == '1':
            time_stats(df)
            break
        elif selection == '2':
            station_stats(df)
            break
        elif selection == '3':
            trip_duration_stats(df)
            break
        elif selection == '4':
            user_stats(df)
            break
        elif selection == '5':
            raw_data(df)
            break
        else:
            break


def main():
    """ Main script of program"""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        df_info(df)

        while True:
            quest(df)
            all_done = input('\nWould you like to go back and examine something else? Enter yes or no. ')
            print('-' * 40)
            if all_done.lower() != 'yes':
                break

        restart = input('\nWould you like to restart and change your filters? Enter yes or no. ')
        if restart.lower() != 'yes':
            print("""
             o__         __o       __o
             ,>/_      _ V<_    _ V<_
            (*)`(*)...(_)/(_)...(_)/(_)
            """)
            # Cycling ASCII art from https://www.asciiart.eu/sports-and-outdoors/cycling
            print("Bye for now!")
            break


if __name__ == "__main__":
    main()
