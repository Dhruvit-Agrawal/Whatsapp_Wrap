import pandas as pd
import regex as re
import datetime

def preprocess(raw_data):

    """
    Preprocesses raw WhatsApp chat data to extract structured information.

    Parameters:
    - raw_data (str): Raw chat data as a single string.

    Returns:
    - pd.DataFrame: A DataFrame containing the following columns:
        * Date: Date of the message (datetime object).
        * Time: Time of the message (datetime object).
        * Sender: Name of the message sender.
        * Message: Content of the message.
        * month: Name of the month the message was sent.
        * day: Day of the month the message was sent.
        * day_name: Day of the week the message was sent.
        * year: Year the message was sent.
        * hour_with_ampm: Hour in 12-hour format with AM/PM.
        * minute: Minute of the hour the message was sent.

    Additional Notes:
    - If a line does not match the expected pattern, it is marked with 'Unknown' in the Sender column.
    - Rows with missing or unmatched data are removed before returning the DataFrame.

    """

    
    raw_data=raw_data.split('\n')
    # Define the regular expression pattern to extract date, time, sender, and message
    # The pattern captures:
    # - (\d{1,2}/\d{1,2}/\d{2,4}): Date in DD/MM/YY or DD/MM/YYYY format
    # - (\d{1,2}:\d{2}): Time in HH:MM format
    # - ([APM]{2}): AM or PM
    # - ([\w\s.\p{So}]+): Sender's name (allows for alphanumeric, spaces, special unicode characters)
    # - (.+): The message content
    pattern = r"(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2})\s*([APM]{2}) - ([\w\s.\p{So}]+): (.+)"

    # Prepare lists to hold extracted data
    dates = []
    times = []
    senders = []
    messages = []
    no_match = 0  # Counter for lines that don't match the pattern

    # Loop through each line in the raw chat data
    for entry in raw_data:
        # Try to match the pattern to the current line
        match = re.search(pattern, entry)
        
        # If a match is found, extract the data
        if match:
            dates.append(match.group(1))
            times.append(f"{match.group(2)} {match.group(3)}")  # Combine time and AM/PM
            senders.append(match.group(4))
            messages.append(match.group(5))
        else:
            # If no match, handle unmatched lines 
            # by storing them with None values for other columns
            no_match += 1
            dates.append(None)
            times.append(None)
            senders.append("Unknown")  # Assign "Unknown" as sender
            messages.append(entry.strip())  # Keep the original message content

    # Create a pandas DataFrame from the extracted data
    df = pd.DataFrame({
        'Date': dates,
        'Time': times,
        'Sender': senders,
        'Message': messages
    })

    print(f"Number of unmatched lines: {no_match}")  # Print the number of unmatched lines

    # drop the none rows
    df=df.dropna()

    # Convert the 'Date' column to datetime objects using pandas' to_datetime function
    # pandas automatically infers the date format in most cases
    df['Date'] = pd.to_datetime(df['Date'])  

    # Convert the 'Time' column to datetime objects
    # Specify the format using '%I:%M %p' to handle 12-hour time with AM/PM
    df['Time'] = pd.to_datetime(df['Time'], format='%I:%M %p')

    #month
    df['month']=df['Date'].dt.month_name()
    #day of the month
    df['day']=df['Date'].dt.day
    #day on that date
    df['day_name']=df['Date'].dt.day_name()
    #year
    df['year']=df['Date'].dt.year
    #hour with am/pm
    df['hour_with_ampm']=df['Time'].dt.strftime('%I %p')
    #minute of the hour
    df['minute']=df['Time'].dt.minute


    return df


