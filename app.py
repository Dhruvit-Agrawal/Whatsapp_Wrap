import streamlit as st
import pandas as pd
from preprocessor import preprocess
from analyser import activity_heatmap, daily_timeline, fetch_stats, most_active_user, week_activity_map
import plotly.express as px
import numpy as np
from WordCloudGenerator import generate_wc, emoji_analysis
import analyser

# Title of project
st.title('WHATSAPP WRAP')

st.sidebar.title("Sidebar")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:

    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # Convert stream to string
    string_data = bytes_data.decode("utf-8")

    # Preprocessing the string_data
    preprocessed_data = preprocess(string_data)


    # Fetching the sender list
    sender_list = preprocessed_data['Sender'].unique().tolist()
    sender_list.insert(0, "Whole Group")
    
    # Displaying the sender list
    selected_user = st.sidebar.selectbox("Get the WhatsApp Wrap with respect to", sender_list)

    # Show analysis button
    if st.sidebar.button("Show Analysis"):
        ########################## Analysis of the selected user and fetching the statistics ##########################
        total_message, total_word, total_media = fetch_stats(df=preprocessed_data, selected_user=selected_user)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Messages", total_message)
        col2.metric("Total Words", total_word)
        col3.metric("Total Media Files", total_media)
        #col4.metric("Total Links Shared",total_links)

        ######################### FINDING THE MOST ACTIVE USER IN THE GROUP ###################
        if selected_user == "Whole Group":
            # Finding the most active user in the group
            most_active_users, most_active_users_df = most_active_user(df=preprocessed_data)
            st.header("Most Active Users")
            col1,col2=st.columns(2)

            # Bar graph of the most active users using Plotly
            fig = px.bar(most_active_users_df, y=most_active_users_df.index, x='Message Count', orientation='h',labels={'x': 'Senders', 'y': 'Messages'}, title='Most Active Users')
            
            col1.plotly_chart(fig)
            col2.dataframe(most_active_users_df)

        ################################# WORDCLOUD ###################################
        # Wordcloud of the selected user
        wc_file, word_freq = generate_wc(df=preprocessed_data, selected_user=selected_user)
        
        # Displaying the wordcloud on the app
        
        st.header(f"Wordcloud of {selected_user}")
        #increase the size of image
        st.image(wc_file, width=340)

        # Display top 20 common words using Plotly
        words, frequencies = zip(*word_freq)  # Unpack tuples into two lists
        common_words_df = pd.DataFrame({'Words': words, 'Frequency': frequencies})
        
        st.header(f"Top 20 Common Words of {selected_user}")
        fig = px.bar(common_words_df.head(20), y='Words', x='Frequency', orientation='h',title='Top 20 Common Words', labels={'Words': 'Words', 'Frequency': 'Frequency'})
        st.plotly_chart(fig)

        ############################ Emoji Data Analysis #################################
        emoji_data = emoji_analysis(df=preprocessed_data, selected_user=selected_user)
        st.title("Emojis Shared")
        
        if not emoji_data.empty:  # Check if emoji_data is not empty
            col1, col2 = st.columns(2)

            emoji_df = pd.DataFrame(emoji_data)
            col1.dataframe(emoji_df)

            # Pie chart of top 8 emojis using Plotly
            n = 8
            top_n_emoji = emoji_df.nlargest(n=n, columns=['Frequency'])
            fig = px.pie(top_n_emoji, values='Frequency', names='Emoji', title='Top Emojis Shared')
            fig.update_traces(textposition='inside', textinfo='percent+label')
            col2.plotly_chart(fig)
        else:
            st.header("No emojis found")

        ############################## Timeline Analysis #####################
        # Monthly timeline analysis of the selected user
        timeline_data = analyser.monthly_timeline(df=preprocessed_data, selected_user=selected_user)

        if not timeline_data.empty:
            st.header("Monthly Activity")
            fig = px.line(timeline_data, x="time", y="Message")
            st.plotly_chart(fig)
        else:
            st.header("No data available")

        # Weekly timeline analysis of the selected user
        daily_activity = analyser.daily_timeline(df=preprocessed_data, selected_user=selected_user)
        
        if not daily_activity.empty:
            st.header("Daily Activity")
            fig = px.line(daily_activity, x="Date", y="Message")
            st.plotly_chart(fig)
        else:
            st.header("No data available")

        ############ Daywise and Monthwise Activity ####
        col1, col2 = st.columns(2)

        # Daywise activity of selected user
        daywise_activity = analyser.week_activity_map(df=preprocessed_data, selected_user=selected_user)
        
        if not daywise_activity.empty:
            col1.header("Day-wise Activity")
            fig = px.bar(x=daywise_activity.index, y=daywise_activity.values, labels={'x': 'Days', 'y': 'Messages'})
            col1.plotly_chart(fig)
        else:
            st.header("No data available")

        
        # Monthwise activity
        monthwise_activity = analyser.month_activity_map(df=preprocessed_data, selected_user=selected_user)
        
        if not monthwise_activity.empty:
            col2.header("Month-wise Activity")
            fig = px.bar(x=monthwise_activity.index, y=monthwise_activity.values, labels={'x': 'Months', 'y': 'Messages'})
            col2.plotly_chart(fig)
        else:
            st.header("No data available")

        ############### Activity Heatmap ############
        activity_map = activity_heatmap(df=preprocessed_data, selected_user=selected_user)
        
        if not activity_map.empty:
            st.header("Activity Heatmap")
            
            # Create a heatmap using Plotly Express
            fig = px.imshow(activity_map.values,
                            labels=dict(x="Hour of the Day", y="Days"),
                            x=list(activity_map.columns),
                            y=list(activity_map.index),
                            color_continuous_scale='Viridis')
            
            st.plotly_chart(fig)
    else:
 

        # Enhanced Header and Instructions
        st.header("✨ Select a User for Analysis")

        st.write("""
        To get started, please choose a user from the dropdown menu present in the sidebar and click the **"Show Analysis"** button
        """)

else:
    
    # Welcome Header
    st.header("Welcome to WhatsApp Wrap!")

    # Introduction
    st.write("""
    WhatsApp Wrap is a powerful tool designed to provide you with a **comprehensive analysis** of your WhatsApp chat data. 
    By uploading your exported chat file, you can gain valuable insights into your messaging behavior and communication patterns.
    """)

    # Instructions for Exporting WhatsApp Chat
    st.subheader("How to Export Your WhatsApp Chat")
    st.markdown("""
    Follow these simple steps to export your chat for analysis:
    1. **Open the desired chat**: Navigate to the conversation you wish to analyze.
    2. **Access the DropDown Menu**: Tap on the three dots in the upper right corner of the chat screen.
    3. **Select "More"**: This option will expand additional settings.
    4. **Choose "Export Chat"**: You will be given options for exporting your chat.
    5. **Select "Without Media"**: Currently, our tool does not support media analysis, so please choose this option.
    """)

    # Additional Features
    st.subheader("Why Use WhatsApp Wrap?")
    st.write("""
    Here are some of the exciting features you can explore:
    - 📊 **Participant Analysis**: Discover who messages the most and when.
    - ☁️ **Word Cloud Generation**: Visualize frequently used words in your chats.
    - 😀 **Emoji Analysis**: Gain insights into your emoji usage and trends.
    - 📈 **Interactive Visualizations**: Explore your data through engaging charts and graphs.

    Upload your WhatsApp chat file throught upload button present in the sidebar tab now and unlock insights that help you better understand your messaging habits!
    """)
