import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']
# the available days of the week are listed below
days = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')


def get_filter_city():
    """
    Asks user to specify the name of the city to analyze
    """
    # build and display the list of cities for which we have datasets
    cities_list = []
    number_cities = 0

    for a_city in CITY_DATA:
        cities_list.append(a_city)
        number_cities += 1
        print(' {0:20}. {1}'.format(number_cities, a_city.title()))

    # ask user to input a number for a city from the list
    while True:
        try:
            city_number = int(input("\n Enter a number for the city (1 - {}):  ".format(len(cities_list))))
        except:
            continue

        if city_number in range(1, 4):
            break

    # get the city's name in string format from the list
    city = cities_list[city_number - 1]
    return city


def get_filter_month():
    """
    Asks user to specify a month to filter on, or choose all.

    """  
    while True:
        try:
            month = input("Enter the month, type '1' for January, '2' for February, '3' for March, '4' for April, '5' for May, '6' for June or 'a' for all:  ")
        except:
            print("I didn\'t get that, Please Try again.")            
            print("Valid inputs:  1, 2, 3, 4, 5, 6, a")
            continue

        if month == 'a':
            month = 'all'
            break
        elif month in {'1', '2', '3', '4', '5', '6'}:
            # reassign the string name for the month
            month = months[int(month) - 1]
            break
        else:
            continue
    
    return month


def get_filter_day():
    """
    Asks user to specify a day to filter on, or choose all.

    """
    while True:
        try:
            day = input("Enter the day type,1 for Monday, 2 for Tuesday, 3 for Wednesday, 4 for Thursday, 5 for Friday, 6 for Saturday, 7 for Sunday or 'a' for all:  ")
        except:
            print("I didn\'t get that, Please Try again.") 
            print("Valid inputs:  1, 2, 3, 4, 5, 6, 7, a")
            continue

        if day == 'a':
            day = 'all'
            break
        elif day in {'1', '2', '3', '4', '5', '6', '7'}:
            # reassign the string name for the day
            day = days[int(day) - 1]
            break
        else:
            continue

    return day



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # note that this fuction will call the get_filter_city(), get_filter_month() and the get_filter_day() functions
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_filter_city()

    # get user input for month (all, january, february, ... , june)
    month = get_filter_month()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_filter_day()

    print('-'*60)
    
    print(' Analyzing statistics for:  ', city)
    print('Month: ', month)
    print('Day: ', day)    
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
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
    df['month'] = df['Start Time'].dt.month
    
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    # filtering by month
    if month != 'all':
   	 	# use the index of the months list to get the corresponding int
        month_index = months.index(month) + 1
    	# filter by month to create the new dataframe
        df = df[df.month == month_index]
        month = month.title()

    # filtering by day of week
    if day != 'all':
        # use the index of the WEEKDAYS list to get the corresponding int
        day_index = days.index(day)
        # filter by day of week to create the new dataframe
        df = df[df.day_of_week == day_index]
        day = day.title()

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    
    # display the most common month
    Most_common_month = months[df['month'].mode()[0] - 1].title()
    print('Most Common Month:', Most_common_month)

    # display the most common day of week
    Most_common_day = days[df['day_of_week'].mode()[0]].title()
    print('Most Common day:', Most_common_day)

    # display the most common start hour
    Most_common_hour = df['hour'].mode()[0]
    print('Most Common Hour:', Most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    Most_Common_Start_Station = df['Start Station'].value_counts().idxmax()
    print('Most Commonly used start station:', Most_Common_Start_Station)

    # display most commonly used end station
    Most_Common_End_Station = df['End Station'].value_counts().idxmax()
    print('\nMost Commonly used end station:', Most_Common_End_Station)

    # display most frequent combination of start station and end station trip
    df['Start-End Combination'] = (df['Start Station'] + ' - ' +
                                   df['End Station'])
    most_common_start_end_combination = str(df['Start-End Combination']
                                            .mode()[0])
    print("Most frequent start-end combination of stations is: " + most_common_start_end_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = sum(df['Trip Duration'])
    print('Total travel time:', total_travel_time/(60*60*24), " Days")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time/60, " Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    # Display counts of gender
    try:
      gender_types = df['Gender'].value_counts()
      print('\nGender Types:\n', gender_types)
    except KeyError:
      print("sorry! There is no available data.")

    # Display earliest, most recent, and most common year of birth
    try:
      Earliest_Year = int(df['Birth Year'].min())
      print('\nEarliest Birth Year:', Earliest_Year)
    except KeyError:
      print("\nEarliest Year:\nNo available data.")

    try:
      Most_Recent_Year = int(df['Birth Year'].max())
      print('\nMost Recent Birth Year:', Most_Recent_Year)
    except KeyError:
      print("\nMost Recent Birth Year:\nNo available data.")

    try:
      Most_Common_Year = int(df['Birth Year'].value_counts().idxmax())
      print('\nMost Common Birth Year:', Most_Common_Year)
    except KeyError:
      print("\nMost Common Birth Year:\nNo available data.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def display_data(df):
    """
    The funtion accepts user responses  and returns raw data of the dataset, 5 rows at a time.
    """
    start_loc = 0
    print("\n would you like to view 5 rows of raw data? Enter yes or no")
    while start_loc < len(df):
        view_data = input('  (yes or no):  ').lower()
        if  view_data == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
        
            print("\n would you like to view the next 5 rows of raw data?")
            continue
        else:
            break
            
            
    print('-'*60)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Thanks for your time.')
            break


if __name__ == "__main__":
	main()
