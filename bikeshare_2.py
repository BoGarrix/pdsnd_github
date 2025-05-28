import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': './chicago.csv',
              'New York City': './new_york_city.csv',
              'Washington': './washington.csv' }

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

    city = input('\nPlease Enter The name of the City You Want To Analyze (Chicago, New York City, Washington) :\n')
    isValid_city = False
    while isValid_city == False:
        if city.strip().title() in CITY_DATA.keys():
            isValid_city = True
            print(f'\nAlright, You Choose {city.strip().title()} as the city to analyzed.')
        else : 
            city = input('\nplease enter a valid city name!\n')

    # get user input for month (january, february, ... , june)
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    
    choice = input('\nDo you want to filter by Month, Day or Both ? (Enter None if you don\'t want to use any filter)\n')
    isValid_choice = False
    while isValid_choice == False:
        if(choice.title().strip() in ['Month', 'Day', 'Both','None']):
             isValid_choice = True
        else:
             choice = input('\nplease Renter a Valid Choice!\n')
        
        
    if(choice.strip().title() == 'Month'):
        month = input('\nplease enter the month you want to filter by (January, February, March, April, May, June):\n')
        day = 'all'
        isValid_month = False
        while isValid_month == False:
            if month.strip().title() in months:
                isValid_month = True
            else : 
                month = input('\nPlease Enter a Valid Month!\n')

    
    # get user input for day of week (monday, tuesday, ... sunday)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    if(choice.strip().title() == 'Day'):
        day = input('\nplease enter the Day you want to filter by (Monday, Tuesday, ... Sunday)\n')
        month = 'all'
        isValid_day = False
        while isValid_day == False:
            if (day.strip().title() in days):
                isValid_day = True
            else : 
                day = input('\nPlease Enter a Valid Day!\n')

    # get user input for both day and month filter
    if(choice.strip().title() == 'Both'):

        isValid_day = False
        day = input('\nplease enter the Day you want to filter by (Monday, Tuesday, ... Sunday\n')
        while isValid_day == False :
            if (day.strip().title() in days):
                isValid_day = True
            else : 
                day = input('\nPlease Enter a Valid Day\n')

        month = input('\nplease enter the month you want to filter by (january, february, march, april, may, june)\n')
        isValid_month = False
        while  isValid_month == False:
            if  (month.strip().title() in months):
                isValid_month = True
                
            else : 
                month = input('\nPlease Enter a Valid Month!\n')
    
    # set the day and month to all if the user choose None
    if(choice.strip().title() == 'None'):
        day = 'all'
        month = 'all'
    


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
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.strip().title()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month.strip().title()) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Start_Time_Month'] = df['Start Time'].dt.month
    most_month = df['Start_Time_Month'].mode()[0]
    print(f'\nthe most common month: {most_month}\n')

    # display the most common day of week
    df['Start_Time_DayofWeek'] = df['Start Time'].dt.day_name()
    most_DayofWeek = df['Start_Time_DayofWeek'].mode()[0]
    print(f'\nthe most common day of week: {most_DayofWeek}\n')


    # display the most common start hour
    df['Start_Time_Hour'] = df['Start Time'].dt.hour
    most_hour = df['Start_Time_Hour'].mode()[0]
    print(f'\nthe most common Hour: {most_hour}\n')



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start_station = df['Start Station'].mode()[0]
    print(f'\nthe most commonly used start station: {most_start_station} \n')

    # display most commonly used end station
    most_end_station = df['End Station'].mode()[0]
    print(f'\nthe most commonly used end station: {most_end_station} \n')

    # display most frequent combination of start station and end station trip
    most_SE_station = df[['Start Station','End Station']].mode()
    most_SE_station = most_SE_station.iloc[0]['Start Station']
    print(f'\nthe most frequent combination of start station and end station trip: {most_SE_station} \n')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'\ntotal travel time : {total_travel_time}\n')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f'\ntotal travel time : {mean_travel_time}\n')



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_dict()
    print(f'\ncounts of user types: {user_types}\n')

    # Display counts of gender
    try:
        counts_of_gender = df['Gender'].value_counts().to_dict()
        print(f'\ncounts of gender: \n{counts_of_gender}')
    except:
        print('\nthe data set has no info about the gender.\n')

    # Display earliest, most recent, and most common year of birth
    try:
        min = int(df['Birth Year'].min())
        max = int(df['Birth Year'].max())
        mode = int(df['Birth Year'].mode()[0])
        print(f'\nearliest year : {min}\n')
        print(f'\nmost recent : {max}\n')
        print(f'\nmost recent : {mode}\n')
    except:
        print('\nthe data set has no info about the birth year.\n')
        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    n = 0
    msg = '\nAre you interested in viewing raw data (y/n) ?\n'
    while True : 

        choice = input(msg)
        
        if(choice.strip().lower() == 'y'):
            print(df.iloc[n:n+5])
            n = n+5
        if(choice.strip().lower() == 'n'):
            break
        
        if choice.strip().lower() not in ['y','n']:
            choice = input('\ninter a valid choice (y/n) ?\n')
        msg = '\ndo you want more raw data (y/n) ?\n'
    
def main():
    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
