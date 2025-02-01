import pandas as pd
import regex as re
import datetime

def preprocess(raw_data, device):
    """
    Preprocesses raw WhatsApp chat data to extract structured information.

    Parameters:
    - raw_data (str): Raw chat data as a single string
    - device (str): Device type ('ios' or 'android')

    Returns:
    - pd.DataFrame: Processed DataFrame with date/time features
    """
    
    # iOS pattern (with brackets)
    ios_pattern = r'''
        \s*‎?\[?                           # Optional whitespace and invisible character and opening bracket
        (\d{1,2}/\d{1,2}/\d{2}),\s*       # Date in DD/MM/YY format
        (\d{1,2}:\d{1,2}:\d{1,2})\s*      # Time in HH:MM:SS format
        ([APMapm]{2})\]?\s*               # AM/PM
        (.+?):\s*                         # Sender name
        (.+)                              # Message content
    '''
    
    # Android pattern (without brackets)
    android_pattern = r'''
        (\d{1,2}/\d{1,2}/\d{2,4}),\s*    # Date
        (\d{1,2}:\d{2})\s*([AaPpMm]{2})\s*   # Time and AM/PM
        -\s*
        ([^:]+):\s*                       # Sender name
        (.+)                              # Message content
    '''
    
    # Select pattern based on device
    pattern = ios_pattern if device.lower() == "ios" else android_pattern
    
    # Initialize lists
    dates, times, senders, messages = [], [], [], []
    no_match = 0
    
    # Compile the pattern
    regex = re.compile(pattern, re.VERBOSE)
    
    # Process each entry
    for entry in raw_data:
        entry = entry.strip()
        if not entry:  # Skip empty lines
            continue
            
        match = regex.match(entry)
        
        if match:
            date, time, ampm, sender, message = match.groups()
            dates.append(date)
            times.append(f"{time} {ampm}")
            senders.append(sender.strip())
            messages.append(message.strip())
        else:
            no_match += 1
            dates.append(None)
            times.append(None)
            senders.append("Unknown")
            messages.append(entry.strip())
    
    # Create initial DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Time': times,
        'Sender': senders,
        'Message': messages
    })
    
    # Clean data: Remove rows with None values
    df = df.dropna()
    
    try:
        # Convert Date to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Convert Time based on device format
        if device.lower() == "ios":
            # For iOS format (HH:MM:SS AM/PM)
            df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S %p').dt.time
        else:
            # For Android format (HH:MM AM/PM)
            df['Time'] = pd.to_datetime(df['Time'], format='%H:%M %p').dt.time
        
        # Extract additional time/date components
        df['month'] = df['Date'].dt.month_name()
        df['day'] = df['Date'].dt.day
        df['day_name'] = df['Date'].dt.day_name()
        df['year'] = df['Date'].dt.year
        
        # Convert Time to string and then back to datetime for consistent formatting
        df['hour_with_ampm'] = pd.to_datetime(df['Time'].astype(str)).dt.strftime('%I %p')
        df['minute'] = pd.to_datetime(df['Time'].astype(str)).dt.minute
        
    except Exception as e:
        print(f"Error during datetime processing: {str(e)}")
        # Print a sample of the time data for debugging
        print("Sample time values:", df['Time'].head())
        return None
    
    return df
