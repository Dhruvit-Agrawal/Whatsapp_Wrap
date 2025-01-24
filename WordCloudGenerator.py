from wordcloud import WordCloud
from collections import Counter
import emoji
import pandas as pd
import re

#stopwords
f=open(".\stop_hinglish.txt", "r")
stop_words=f.read().splitlines()

def generate_wc(df,selected_user):

    #specific user
    if selected_user!="Whole Group":
        df = df[df['Sender'] == selected_user]
    
    #removing stopwords from message column
    words = df['Message'].apply(lambda x: ' '.join([word.lower() for word in x.split() if word not in stop_words])) 

    #removing "." "," "?" in words
    punctuations=[',','.','?']
    for p in punctuations:
        words = words.apply(lambda x: x.replace(p,''))

    #wc instance
    wc= WordCloud(background_color='#020400',min_font_size=10)
    wc_file=wc.generate(words.str.cat(sep=' '))                 #convert to string then concatinate with seperator as " "

    ##finding frequencies of each word occured
    all_words = []
    for message in words:
        all_words.extend(message.split())  # Split each message and add its words to the list

    word_freq = Counter(all_words).most_common(20) # Create the Counter object after collecting all word

    return wc_file.to_image(), word_freq



def emoji_analysis(df, selected_user):
    # Filter for the specific user
    if selected_user != "Whole Group":
        df = df[df['Sender'] == selected_user]

    # Extract emojis from messages
    all_emojis = []
    df['Message'].apply(lambda x: all_emojis.extend([char for char in x if char in emoji.EMOJI_DATA]))

    # Calculate emoji frequencies
    emoji_freq = Counter(all_emojis)

    emojis, frequencies = zip(*emoji_freq.items())  # Use .items() to get (emoji, frequency) pairs
    emoji_df = pd.DataFrame({'Emoji': emojis, 'Frequency': frequencies})

    
    return emoji_df


