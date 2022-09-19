import time
import pandas as pd
from scipy import stats
import numpy as np
import random


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    print('\n Hello! Let\'s explore some US bikeshare data!\n')
    while True:    
        try:
	        city = str(input("Would you like to see data for chicago, new york city or washington?: ")).lower()
        except ValueError:
            print("Sorry, invalid input. Better try again.")
            continue
        else:
        #we're ready to exit the loop.
            break
    filter_data = str(input("Would you like to filter the data by month, day, both or all?: ")).lower()
    # TO DO: get user input for month (all, january, february, ... , june)
    if filter_data=="month":   
        month = str(input("Which month? january, february, march, april, may, june or all?: ")).lower()
        day = "all"
    elif filter_data=="day":
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        day = str(input("Which day? monday, tuesday, wednesday, thursday, friday, saturday, sunday:  ")).lower()
        month = "all"
    elif filter_data == "both":
        month = str(input("Which month? january, february, march, april, may, june or all?: ")).lower()
        day = str(input("Which day? monday, tuesday, wednesday, thursday, friday, saturday, sunday: ")).lower()
    else:
        month = "all"
        day = "all"
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
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    #df['day'] = df['Start Time'].dt.strftime("%A")
    df['day'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour
    #     in the examples on udacity they got day of week with other function, 
#     but it didn't worked in my pandas.  
    #df['day'] = df['Start Time'].dt.strftime("%A")
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
        day = days.index(day) + 1
        df = df[df['day'] == day]
    return df

#Defining a function to display data rows by rows
def data_rows(df):
    start = 0
    data_rows = input('\nWould you like to see 5 rows data? Enter yes or no.\n')
    while data_rows.lower() != 'no':
        df_new = df.iloc[start:start+5]
        print(df_new)
        start += 5
        #getting user input in the loop to incremet
        data_rows = input('\nWould you like to see 5 more rows of data? Enter yes or   no.\n')
        #using if to exit the code if user doesn't want to continue
        if data_rows.lower() == 'no':
            break
             
def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # TO DO: display the most common month
    # find the most popular month
    popular_month = df['month'].mode()
    print('Most Popular Month:', popular_month)
   
    # TO DO: display the most common day of week
    popular_day = df['day'].mode()
    print('Most Popular Day:', popular_day)

    # TO DO: display the most common start hour
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    popular_hour = df['hour'].mode()
    print('Most Common Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()
    print('Most Common Start Station:', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()
    print('Most Common End Station:', popular_end_station)
    

    # TO DO: display most frequent combination of start station and end station trip
    print('Most frequent start and end station: ',df.groupby(['Start Station','End Station']).size().nlargest(1) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # TO DO: display total travel time
    print (df['Trip Duration'].sum())
    #finding total travel time

    
    # TO DO: display mean travel time
    print(df['Trip Duration'].mean())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts() 
    print(user_types)

    #Checking wheather the column exits in the dataset
    if 'Gender' not in df.columns:
        print("\n Sorry, Gender data not exist.\n")
    else:
        print(" \n Let's display the data as per the gender \n")
    # TO DO: Display counts of gender
        Gender = df['Gender'].value_counts() 
        print(Gender)

    # TO DO: Display earliest, most recent, and most common year of birth
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        data_rows(df)      
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()