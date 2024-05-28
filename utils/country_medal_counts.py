import pandas as pd
from .data import load_data

df = load_data('data/athlete_events.csv')

def total_medal_counts(country, start_date, end_date):
    total_medals = df[(df['Team'] == country) & (df['Year'] >= start_date) & (df['Year'] <= end_date)].groupby('Medal').size().reset_index(name='count')['count'].sum()
    return total_medals

def medal_rank(country, start_date, end_date):
    filtered_df = df[(df['Year'] >= start_date) & (df['Year'] <= end_date)]
    medal_counts = filtered_df.groupby('Team')['Medal'].count().reset_index(name='Total_Medals')
    sorted_counts = medal_counts.sort_values(by='Total_Medals', ascending=False)
    sorted_counts['Rank'] = sorted_counts['Total_Medals'].rank(method='dense', ascending=False)
    team_rank = sorted_counts[sorted_counts['Team'] == country]['Rank'].values[0]
    return team_rank

def best_event(country, start_date, end_date):
    filtered_df = df[(df['Year'] >= start_date) & 
                 (df['Year'] <= end_date) & 
                 (df['Team'] == country) & 
                 (df['Medal'].notnull())]  # Exclude rows where Medal is null

    # Group by Team, Event, Sport, and Year, count the occurrences of Medal
    medal_counts = filtered_df.groupby(['Team', 'Event', 'Sport', 'Year'])['Medal'].count().reset_index(name='Medal Count')

    # Group by Sport and sum the medal counts
    top_sports = medal_counts.groupby('Sport')['Medal Count'].sum().reset_index(name='Total Medals')

    # Sort the sports by total medal counts in descending order
    top_sports = top_sports.sort_values(by='Total Medals', ascending=False)

    # Select the top 3 sports
    top_3_sports = top_sports.head(3)

    # Return the top 3 sports
    return top_3_sports

def medals_over_time(country, start_date, end_date):
    filtered_df = df[(df['Team'] == country) & (df['Year'].between(start_date, end_date))]

    pivot_df = filtered_df.pivot_table(index='Year', columns='Season', aggfunc='size').reset_index().fillna(0)

    # Rename the columns for better readability
    pivot_df.columns = ['Year', 'Winter', 'Summer']

    # Convert counts to integers
    pivot_df[['Winter', 'Summer']] = pivot_df[['Winter', 'Summer']].astype(int)

    pivot_df = pivot_df[(pivot_df['Winter'] > 0) | (pivot_df['Summer'] > 0)]

    return pivot_df

