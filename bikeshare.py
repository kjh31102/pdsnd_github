import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Which city would you like to see data for? (Choose among Chicago or New York or Washington)\n").lower()
        cities = ['chicago', 'new york', 'washington']
        if city in cities:
            break
        else:
            print("\nPlease choose among 'Chicago' or 'New York' or 'Washington'")


    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("which month? January, February, March, April, June or All?\n").lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        if month in months:
            break
        else:
            print("\nPlease choose among January, February, March, April, June or All")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All?\n").lower()
        week_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
        if day in week_days:
            break
        else:
            print("\nPlease choose among Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

     # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month_idx = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    common_month = months[common_month_idx-1]
    if month == 'all':
        print('Most Common Month:', common_month.title())
    # display the most common day of week

    common_day = df['day_of_week'].mode()[0]
    if day == 'all':
        print('Most Common Day:', common_day)
    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    common_start_station_count = df[df['Start Station'] == common_start_station].shape[0]
    print('Most Commonly-used Start Station :', common_start_station)
    print('Count of Most Commonly-used Start Station :', common_start_station_count)
    print()

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    common_end_station_count = df[df['End Station'] == common_end_station].shape[0]
    print('Most Commonly-used End Station:', common_end_station)
    print('Count of Most Commonly-used End Station :', common_end_station_count)
    print()

    # display most frequent combination of start station and end station trip
    df['comb_of_start_end_stn'] = "Start -> " + df['Start Station'] + " End -> " + df['End Station']
    common_start_end_station = df['comb_of_start_end_stn'].mode()[0]
    common_start_end_station_count = df[df['comb_of_start_end_stn'] == common_start_end_station].shape[0]
    print('Most Commonly-used Combination of Start/End Station:\n', common_start_end_station)
    print('Count of Most Commonly-used Combination of Start/End Station:', common_start_end_station_count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    print("The total travel time (seconds):", total_travel_time)

    # display mean travel time
    mean_travel_time = int(df['Trip Duration'].mean())
    print('Mean Travel Time (seconds):', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_of_user_types = df.groupby(['User Type'])['User Type'].count()
    print('Counts of each user types:\n', counts_of_user_types, '\n')

    # Display counts of gender
    if city != "washington":
        counts_of_gender = df.groupby(['Gender'])['Gender'].count()
        print('Counts of gender:\n', counts_of_gender, '\n')
        # Display earliest, most recent, and most common year of birth
        most_earliest_yob = int(df['Birth Year'].min())
        most_recent_yob = int(df['Birth Year'].max())
        most_common_yob = int(df['Birth Year'].mode()[0])
        print('Earliest year of birth: ', most_earliest_yob)
        print('Most recent year of birth: ', most_recent_yob)
        print('Most common year of birth: ', most_common_yob)
    else:
        print("There is no information for gender and birth")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def more_info(df):
    x = 1
    while True:
        raw_data_req = input('\nWould you like to see some raw data? Enter yes or no. (Consecutive five rows of raw data will be shown for each \'yes\')\n')
        if raw_data_req.lower() == 'yes':
            print(df[x:x+5])
            x = x+5
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        more_info(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        print("Thank you for visiting us")

if __name__ == "__main__":
	main()
