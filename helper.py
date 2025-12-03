import numpy as np
import pandas as pd

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    
    if year == 'Overall' and country != 'Overall':
        flag =1 
        temp_df = medal_df[medal_df['region'] == country]
    
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()

    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')

    return x

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country

def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year': 'Editions', 'count': col}, inplace=True)

    return nations_over_time

def most_successful(df, sport):

    df = df.dropna(subset=['Medal'])
    # 1. Convert medal columns to integers
    df[['Gold','Silver','Bronze']] = df[['Gold','Silver','Bronze']].astype(int)

    # 2. Copy required columns
    df[['Gold', 'Silver', 'Bronze']] = df[['Gold', 'Silver', 'Bronze']].astype(int)

    if sport != 'Overall':
        df = df[df['Sport'] == sport]

    df['total'] = df[['Gold', 'Silver', 'Bronze']].sum(axis=1)

    # 4. Group by athlete and sum medals
    result = df.groupby('Name').agg({
    'region': 'first',
    'Sport': 'first',
    'Gold': 'sum',
    'Silver': 'sum',
    'Bronze': 'sum',
    'total': 'sum'
    }).reset_index()

    # 5. Sort by total descending   
    result = result.sort_values(by='total', ascending=False).reset_index(drop=True)                                                                  
    return result

def year_wise_analysis(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    
    return final_df

def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def top_10_athletes_by_country(df, country):
    temp = df.dropna(subset=['Medal']).copy()

    temp.drop_duplicates(
        subset=['Name', 'Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True
    )

    temp = temp[temp['region'] == country]

    if temp.empty:
        return pd.DataFrame()
    
    medal_count = (
        temp.groupby(['Name', 'Sport']).agg(
            Gold = ('Gold', 'sum'),
            Silver = ('Silver', 'sum'),
            Bronze = ('Bronze', 'sum'),
            Total = ('Medal', 'count')
        ).sort_values('Total', ascending=False).head(10).reset_index()
                      
    )

    return medal_count

def weight_v_height(df, sport): 
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])
    athelete_df['Medal'].fillna('No Medal', inplace=True)
    

    if sport != 'Overall':
        temp_df = athelete_df[athelete_df['Sport'] == sport]
        return temp_df
    else:
        return athelete_df
    


def men_vs_women(df):
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athelete_df[athelete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athelete_df[athelete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final




    



    
