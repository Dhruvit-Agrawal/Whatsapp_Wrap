from urlextract import URLExtract
import matplotlib.pyplot as plt
import pandas as pd

def extract_link(message):

    """
    Extracts URLs from a message and checks if any links are present.

    Parameters:
    - message (str): A single chat message.

    Returns:
    - bool: True if at least one URL is found, None otherwise.
    """
      
        #no of links
    extractor= URLExtract()
    url=extractor.find_urls(message)
    if len(url)>0:
        return True
    else:
        return None
    

def most_active_user(df):

    """
    Identifies the most active users in the chat.

    Parameters:
    - df (pd.DataFrame): DataFrame containing chat data with a 'Sender' column.

    Returns:
    - pd.Series: A series of the top active users and their message counts.
    - pd.DataFrame: DataFrame showing message counts and percentages for all users.
    """

    #most active user
    most_active_users=df['Sender'].value_counts()

    #df of the most_active_user
    most_active_users_df=most_active_users.to_frame('Message Count')
    most_active_users_df['Percentage']=round((most_active_users_df['Message Count']/most_active_users_df['Message Count'].sum())*100,2)
    
    return most_active_users.head(),most_active_users_df




def fetch_stats(df,selected_user):

    """
    Fetches chat statistics including message count, word count, media files, and links.

    Parameters:
    - df (pd.DataFrame): DataFrame containing chat data with 'Sender' and 'Message' columns.
    - selected_user (str): Selected user for which stats are to be fetched. Use 'Whole Group' for group stats.

    Returns:
    - tuple: Contains total messages, total words, total media files, and total links.
    """

    #for specific user:
    if (selected_user!="Whole Group"):
        df=df[df['Sender']==selected_user]

    #total messages
    total_messages = df.shape[0]

    #total words
    total_words = df['Message'].str.split().str.len().sum()

    #no of media files
    media_omitted_messages = df[df['Message'].str.contains("<Media omitted>", na=False)]
    total_media=len(media_omitted_messages)

    #no of links
    # total_link=0
    # for i in range(len(df)):
    #     if extract_link(df['Message'].iloc[i]):
    #         total_link+=1
    
    return total_messages,total_words, total_media #, total_link



def monthly_timeline(selected_user,df):

    """
    Generates a monthly timeline of message counts.

    Parameters:
    - selected_user (str): Selected user for which the timeline is generated. Use 'Whole Group' for group stats.
    - df (pd.DataFrame): DataFrame containing chat data with 'Sender', 'year', and 'month' columns.

    Returns:
    - pd.DataFrame: DataFrame with 'year', 'month', and 'time' columns for the timeline.
    """

    if selected_user != 'Whole Group':
        df = df[df['Sender'] == selected_user]

    timeline = df.groupby(['year', 'month']).count()['Message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):
    """
    Generates a daily timeline of message counts.

    Parameters:
    - selected_user (str): Selected user for which the timeline is generated. Use 'Whole Group' for group stats.
    - df (pd.DataFrame): DataFrame containing chat data with 'Sender' and 'Date' columns.

    Returns:
    - pd.DataFrame: DataFrame with daily message counts.
    """

    if selected_user != 'Whole Group':
        df = df[df['Sender'] == selected_user]

    daily_timeline = df.groupby('Date').count()['Message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    """
    Computes day-of-week activity counts.

    Parameters:
    - selected_user (str): Selected user for which the activity map is generated. Use 'Whole Group' for group stats.
    - df (pd.DataFrame): DataFrame containing chat data with 'Sender' and 'day_name' columns.

    Returns:
    - pd.Series: Series with day-of-week activity counts.
    """


    if selected_user != 'Whole Group':
        df = df[df['Sender'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Whole Group':
        df = df[df['Sender'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    """
    Generates a heatmap of user activity by day and hour.

    Parameters:
    - selected_user (str): Selected user for which the heatmap is generated. Use 'Whole Group' for group stats.
    - df (pd.DataFrame): DataFrame containing chat data with 'Sender', 'day_name', and 'hour_with_ampm' columns.

    Returns:
    - pd.DataFrame: A pivot table with days as rows, hours as columns, and message counts as values.
    """

    if selected_user != 'Whole Group':
        df = df[df['Sender'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='hour_with_ampm', values='Message', aggfunc='count').fillna(0)

    return user_heatmap

