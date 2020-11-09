import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
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
        city = input("Enter city name you like to explore :\n").lower()  # get input from user to get the city to explore

        if city in ['chicago', 'new york city', 'washington']:
            break

        else:
            print("Invalid city name, Please enter valid city name.")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter month name to get details of particular month or else type 'all' to get details of all months :\n ").lower()   # get month from user to get the city to explore

        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break

        else:
            print("Invalid month, Please enter a valid month or 'all'")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter day name to get details of particular day or else type 'all' to get details of all days :\n ").lower()  # get day from user to get the city to explore

        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break

        else:
            print("invalid input. Please enter a valid input")

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
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])  # load data file into a dataframe

    df['Start Time'] = pd.to_datetime(df['Start Time'])  # converting 'Start Time' column to datetime

    df['month'] = df['Start Time'].dt.month  # extract month from 'Start Time' and create new column
    df['weekday'] = df['Start Time'].dt.weekday_name  # extract day of week from 'Start Time' and create new column

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]  # filter by month to create the new dataframe

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['weekday'] == day.title()]  # filter by day of week to create the new dataframe

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month : ", df['month'].mode()[0], "\n")

    # display the most common day of week
    print("The most common day of week : ", df['weekday'].mode()[0], "\n")

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hour : ", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station : ", df['Start Station'].mode()[0], "\n")

    # display most commonly used end station
    print("The most commonly used end station : ", df['End Station'].mode()[0], "\n")

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + " " + df['End Station']
    print("The most frequent combination of start station and end station trip is: ", df['combination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time: ", df['Trip Duration'].sum(), "\n")

    # display mean travel time
    print("The total mean time: ", df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    usertypes = df.groupby(['User Type'])['User Type'].count()
    print(usertypes, "\n")

	# Washington does not have gender birth year columns, so skipping from this statistics
    if city != 'washington':  
        # Display counts of gender
        gender = df.groupby(['Gender'])['Gender'].count()
        print(gender)

        # Display earliest, most recent, and most common year of birth
        recent = sorted(df.groupby(['Birth Year'])['Birth Year'], reverse=True)[0][0]
        earliest = sorted(df.groupby(['Birth Year'])['Birth Year'])[0][0]
        common = df['Birth Year'].mode()[0]
        print("Earliest birth year    : ", earliest, "\n")
        print("Most recent birth year : ", recent, "\n")
        print("Most common birth year : ", common, "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    x = 1

    while True:
        raw = input('Would you like to see some raw data? Enter y OR n \n').lower()   # get input from user whether to show raw data or not
        if raw == 'y':
            print(df[x:x + 5])
            x = x + 5

        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        restart = input('Would you like to restart? Enter y or n \n').lower()  # get input from user whether to restart data exploration

        if restart != 'y':
            break


if __name__ == "__main__":
	main()
