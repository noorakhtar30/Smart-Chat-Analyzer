import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import pdf
import base64
import pandas as pd
from chatbot import WhatsAppChatBot
from datetime import datetime
from streamlit.components.v1 import html
import json
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()


# Page Configuration
st.set_page_config(page_title="Smart Chat Analyzer", layout="wide")


# Function to convert local image to Base64
def get_base64_from_local(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


# Specify the local image file (make sure it's in the same folder)
local_image_path = "5.jpg"  # Ensure this file exists
logo_image_path = "logo.png"  # Add your logo file path here

# Convert images to Base64
bg_image_base64 = get_base64_from_local(local_image_path)
logo_base64 = get_base64_from_local(logo_image_path)

# Inject custom CSS for background image and styling
st.markdown(
    f"""
    <style>
        .stApp {{
            background: url("data:image/jpg;base64,{bg_image_base64}");
            background-size: cover;
            background-position: center;
        }}

        .header-container {{
            text-align: center;
            background-color: #25D366;
            padding: 40px 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .header {{
            font-size: 2.5em;
            font-weight: bold;
            color: white;
            margin-left: 15px;
        }}

        .sub-header {{
            font-size: 1.2em;
            color: white;
        }}

        .logo-img {{
            height: 100px;
            width: auto;
        }}

        .upload-button {{
            background-color: #25D366 !important;
            color: white !important;
            border-radius: 5px;
            font-size: 16px;
            padding: 10px;
        }}

        .note {{
            margin-top: 10px;
            font-size: 14px;
            color: black;
        }}

        .highlight {{
            background-color: #c8f7c5;
            padding: 2px 6px;
            font-weight: bold;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Title Section with Logo
st.markdown(
    f"""
    <div class="header-container">
        <img src="data:image/png;base64,{logo_base64}" class="logo-img">
        <div>
            <div class="header">Smart Chat Analyzer</div>
            <div class="sub-header">chat analytics and insights</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# First declare the file uploader
import streamlit as st
import time

uploaded_file = st.sidebar.file_uploader("Upload Exported Text File", type=["txt"], key="chat_uploader")

# Create a container for the welcome message
welcome_container = st.empty()

# Only show welcome message if no file is uploaded
if uploaded_file is None:
    welcome_container.markdown("""\
    <div style='background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); \
padding: 30px; border-radius: 16px; margin: 25px 0; \
border-left: 5px solid #16a34a; box-shadow: 0 4px 12px rgba(0,0,0,0.05); \
font-family: "Segoe UI", sans-serif;'>\
<h3 style='color: #052e16; margin-top: 0; font-weight: 600; font-size: 24px; \
display: flex; align-items: center; gap: 10px;'>\
<span style='background: #16a34a; color: white; width: 36px; height: 36px; \
border-radius: 50%; display: inline-flex; align-items: center; \
justify-content: center; font-size: 20px;'></span>\
Welcome to Smart Chat Analyzer</h3>\
<p style='color: #14532d; line-height: 1.6; font-size: 16px; margin: 20px 0;'>\
<b>Discover powerful insights from your WhatsApp conversations.</b> Our analyzer transforms your chat exports into visual reports showing:\
<ul style='color: #14532d; padding-left: 20px; margin: 10px 0;'>\
<li>Your most active days and times</li>\
<li>Sentiment trends in conversations</li>\
<li>Most used words and emojis</li>\
<li>Response patterns between participants</li>\
</ul>\
Perfect for understanding group dynamics, personal communication habits, or customer service analysis.\
</p>\
<div style='background: rgba(22, 163, 74, 0.1); padding: 15px; \
border-radius: 8px; margin: 20px 0 10px; border-left: 3px solid #16a34a;'>\
<p style='color: #166534; margin: 0; font-weight: 500; \
display: flex; align-items: center; gap: 8px;'>\
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" \
xmlns="http://www.w3.org/2000/svg"><path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM13 17H11V15H13V17ZM13 13H11V7H13V13Z" fill="#166534"/></svg>\
<b>Complete Privacy:</b> Your chats never leave your browser - all processing happens locally</p></div>\
<div style='display: flex; flex-wrap: wrap; gap: 15px; margin: 20px 0 10px;'>\
<div style='flex: 1; min-width: 200px; background: rgba(22, 163, 74, 0.08); \
padding: 12px; border-radius: 8px; border-left: 3px solid #16a34a;'>\
<p style='color: #166534; margin: 0; font-weight: 500;'>\
<b>Visual Reports</b><br>\
Generate beautiful PDF reports with all your chat statistics</p></div>\
<div style='flex: 1; min-width: 200px; background: rgba(22, 163, 74, 0.08); \
padding: 12px; border-radius: 8px; border-left: 3px solid #16a34a;'>\
<p style='color: #166534; margin: 0; font-weight: 500;'>\
<b>Time Analysis</b><br>\
See when you're most active and response times</p></div>\
</div>\
<p style='color: #4d7c0f; font-size: 14px; margin-bottom: 0; \
display: flex; align-items: center; gap: 6px;'>\
<svg width="16" height="16" viewBox="0 0 24 24" fill="none" \
xmlns="http://www.w3.org/2000/svg"><path d="M12 4V6C16.42 6 20 9.58 20 14C20 14.55 19.55 15 19 15C18.45 15 18 14.55 18 14C18 10.69 15.31 8 12 8V10C12 10.55 11.55 11 11 11C10.45 11 10 10.55 10 10V5C10 4.45 10.45 4 11 4H16C16.55 4 17 4.45 17 5C17 5.55 16.55 6 16 6H12ZM6 19C5.45 19 5 18.55 5 18C5 17.45 5.45 17 6 17H8V15C8 14.45 8.45 14 9 14C9.55 14 10 14.45 10 15V20C10 20.55 9.55 21 9 21H4C3.45 21 3 20.55 3 20C3 19.45 3.45 19 4 19H6Z" fill="#4d7c0f"/></svg>\
<b>How to use:</b> Export your WhatsApp chat (without media), then upload the .txt file here</p>\
</div>\
""", unsafe_allow_html=True)
else:
    # Clear the welcome message immediately
    welcome_container.empty()

    # Show temporary success message
    success_message = st.success("File uploaded successfully!")
    time.sleep(5)
    success_message.empty()

    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Filter analysis by user", user_list)
    # Initialize chatbot

    import streamlit as st
    import base64
    from datetime import datetime

    # Initialize chatbot
    chatbot = WhatsAppChatBot()

    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # ===== SIDEBAR CHATBOT =====
    with st.sidebar:
        # Function to convert local image to base64
        def get_base64_of_image(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()


        # Load background image
        bg_image_base64 = get_base64_of_image("5.jpg")

        # Sidebar chat UI styles
        st.markdown(f"""
            <style>
            .chat-container {{
                height: 400px;
                overflow-y: auto;
                padding: 10px;
                background: url("data:image/jpg;base64,{bg_image_base64}");
                background-size: cover;
                background-position: center;
                border-radius: 10px;
            }}
            .message-wrapper {{
                display: flex;
                align-items: flex-start;
                margin: 6px 0;
            }}
            .user-message, .bot-message {{
                padding: 8px 12px;
                margin: 0 8px;
                max-width: 75%;
                font-size: 14px;
                word-wrap: break-word;
                border-radius: 18px;
                font-family: Arial, sans-serif;
                box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .user-message {{
                background: #25D366; /* WhatsApp green */
                text-align: right;
                color: #fff;
            }}
            .bot-message {{
                background: #ECECEC; /* Light gray */
                text-align: left;
                color: #000;
            }}
            .user-icon, .bot-icon {{
                width: 40px;
                height: 40px;
                border-radius: 50%;
            }}
            </style>
        """, unsafe_allow_html=True)

        st.markdown("Chat Assistant")

        # Chat container with dynamic messages
        chat_html = "<div class='chat-container'>"
        for message in st.session_state.chat_history:
            if message['is_user']:
                chat_html += "<div class='message-wrapper' style='justify-content: flex-end;'>"
                chat_html += "<div class='user-message'>{}</div><img class='user-icon' src='https://cdn-icons-png.flaticon.com/512/2202/2202112.png'/>".format(
                    message['message'])
            else:
                chat_html += "<div class='message-wrapper'>"
                chat_html += "<img class='bot-icon' src='https://cdn-icons-png.flaticon.com/512/4712/4712105.png'/><div class='bot-message'>{}</div>".format(
                    message['message'])
            chat_html += "</div>"
        chat_html += "</div>"

        st.markdown(chat_html, unsafe_allow_html=True)


        # Function to handle user input
        def handle_chat():
            user_input = st.session_state.chat_input.strip()
            if user_input:
                st.session_state.chat_history.append({
                    "message": user_input,
                    "is_user": True
                })

                # Get bot response
                response = chatbot.generate_response(user_input, selected_user, df)

                st.session_state.chat_history.append({
                    "message": response,
                    "is_user": False
                })

                # Clear input
                st.session_state.chat_input = ""


        # User input field
        st.text_input("Type your question:",
                      key="chat_input",
                      placeholder="Ask about your data...",
                      on_change=handle_chat)

    # Show Analysis button
    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
                <div style="background-color: #25D366; padding: 20px; border-radius: 10px; text-align: center;">
                    <h3 style="color: white; margin: 0;">ðŸ“¨ Total Messages</h3>
                    <h1 style="color: white; margin: 0;">{num_messages}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div style="background-color: #128C7E; padding: 20px; border-radius: 10px; text-align: center;">
                    <h3 style="color: white; margin: 0;">ðŸ“ Total Words</h3>
                    <h1 style="color: white; margin: 0;">{words}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <div style="background-color: #34B7F1; padding: 20px; border-radius: 10px; text-align: center;">
                    <h3 style="color: white; margin: 0;">ðŸ–¼ï¸ Media Shared</h3>
                    <h1 style="color: white; margin: 0;">{num_media_messages}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                f"""
                <div style="background-color: #075E54; padding: 20px; border-radius: 10px; text-align: center;">
                    <h3 style="color: white; margin: 0;">ðŸ”— Links Shared</h3>
                    <h1 style="color: white; margin: 0;">{num_links}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Monthly Timeline
        st.title("ðŸ“… Monthly Timeline")
        st.markdown("Explore the trend of messages over time.")
        timeline = helper.monthly_timeline(selected_user, df)

        try:
            # Create a figure with a larger size and transparent background
            fig, ax = plt.subplots(figsize=(12, 6), facecolor='none')  # Transparent background

            # Plot the data with a thicker line and markers
            ax.plot(timeline['time'], timeline['message'],
                    color='#25D366',  # WhatsApp green color
                    linewidth=2.5,  # Thicker line
                    marker='o',  # Add markers
                    markersize=8,  # Marker size
                    markerfacecolor='white',  # White fill for markers
                    markeredgecolor='#25D366')  # Green border for markers

            # Add gridlines for better readability
            ax.grid(True, linestyle='--', alpha=0.7, color='gray')  # Light gray gridlines

            # Rotate x-axis labels for better visibility
            plt.xticks(rotation=45, ha='right')

            # Add labels and title with contrasting colors
            ax.set_xlabel("Month-Year", fontsize=12, labelpad=10, color='black')  # Black text for labels
            ax.set_ylabel("Number of Messages", fontsize=12, labelpad=10, color='black')  # Black text for labels
            ax.set_title("Monthly Message Timeline", fontsize=14, pad=20, color='black')  # Black text for title

            # Highlight the peak month
            peak_month = timeline.loc[timeline['message'].idxmax()]
            ax.annotate(f"Peak: {peak_month['message']} messages",
                        xy=(peak_month['time'], peak_month['message']),
                        xytext=(10, 10), textcoords='offset points',
                        arrowprops=dict(arrowstyle='->', color='red'),
                        fontsize=10, color='red')

            # Set transparent background for the axes
            ax.set_facecolor('none')  # Transparent background for the plot area

            # Set color for tick labels
            ax.tick_params(colors='black')  # Black text for tick labels

            # Adjust layout to prevent clipping of labels
            plt.tight_layout()

            # Save the figure with a transparent background
            fig.patch.set_alpha(0.0)  # Fully transparent background for the figure

            # Display the plot in Streamlit
            st.pyplot(fig)

        except Exception as e:
            st.error(f"An error occurred while plotting the monthly timeline: {e}")

        #   Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)

        try:
            # Create a figure with a larger size and transparent background
            fig, ax = plt.subplots(figsize=(12, 6), facecolor='none')  # Transparent background

            # Plot the data with a thicker line and markers
            ax.plot(daily_timeline['only_date'], daily_timeline['message'],
                    color='#25D366',  # WhatsApp green color
                    linewidth=2.5,  # Thicker line
                    marker='o',  # Add markers
                    markersize=8,  # Marker size
                    markerfacecolor='white',  # White fill for markers
                    markeredgecolor='#25D366')  # Green border for markers

            # Add gridlines for better readability
            ax.grid(True, linestyle='--', alpha=0.7, color='gray')  # Light gray gridlines

            # Rotate x-axis labels for better visibility
            plt.xticks(rotation=45, ha='right')

            # Add labels and title with contrasting colors
            ax.set_xlabel("Date", fontsize=12, labelpad=10, color='black')  # Black text for labels
            ax.set_ylabel("Number of Messages", fontsize=12, labelpad=10, color='black')  # Black text for labels
            ax.set_title("Daily Message Timeline", fontsize=14, pad=20, color='black')  # Black text for title

            # Highlight the peak day
            peak_day = daily_timeline.loc[daily_timeline['message'].idxmax()]
            ax.annotate(f"Peak: {peak_day['message']} messages",
                        xy=(peak_day['only_date'], peak_day['message']),
                        xytext=(10, 10), textcoords='offset points',
                        arrowprops=dict(arrowstyle='->', color='red'),
                        fontsize=10, color='red')

            # Set transparent background for the axes
            ax.set_facecolor('none')  # Transparent background for the plot area

            # Set color for tick labels
            ax.tick_params(colors='black')  # Black text for tick labels

            # Adjust layout to prevent clipping of labels
            plt.tight_layout()

            # Save the figure with a transparent background
            fig.patch.set_alpha(0.0)  # Fully transparent background for the figure

            # Display the plot in Streamlit
            st.pyplot(fig)

        except Exception as e:
            st.error(f"An error occurred while plotting the daily timeline: {e}")

        # Activity Maps
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            try:
                # Create a figure with a transparent background
                fig, ax = plt.subplots(figsize=(8, 5), facecolor='none')  # Transparent background

                # Plot the bar chart
                ax.bar(busy_day.index, busy_day.values, color='#25D366', alpha=0.8)  # WhatsApp green color

                # Add gridlines for better readability
                ax.grid(True, linestyle='--', alpha=0.5, color='gray')  # Light gray gridlines

                # Rotate x-axis labels for better visibility
                plt.xticks(rotation=45, ha='right')

                # Add labels and title with contrasting colors
                ax.set_xlabel("Day of the Week", fontsize=12, labelpad=10, color='black')  # Black text for labels
                ax.set_ylabel("Number of Messages", fontsize=12, labelpad=10, color='black')  # Black text for labels
                ax.set_title("Most Busy Day", fontsize=14, pad=20, color='black')  # Black text for title

                # Set transparent background for the axes
                ax.set_facecolor('none')  # Transparent background for the plot area

                # Set color for tick labels
                ax.tick_params(colors='black')  # Black text for tick labels

                # Adjust layout to prevent clipping of labels
                plt.tight_layout()

                # Save the figure with a transparent background
                fig.patch.set_alpha(0.0)  # Fully transparent background for the figure

                # Display the plot in Streamlit
                st.pyplot(fig)

            except Exception as e:
                st.error(f"An error occurred while plotting the most busy day: {e}")

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            try:
                # Create a figure with a transparent background
                fig, ax = plt.subplots(figsize=(8, 5), facecolor='none')  # Transparent background

                # Plot the bar chart
                ax.bar(busy_month.index, busy_month.values, color='#128C7E', alpha=0.8)  # Darker WhatsApp green color

                # Add gridlines for better readability
                ax.grid(True, linestyle='--', alpha=0.5, color='gray')  # Light gray gridlines

                # Rotate x-axis labels for better visibility
                plt.xticks(rotation=45, ha='right')

                # Add labels and title with contrasting colors
                ax.set_xlabel("Month", fontsize=12, labelpad=10, color='black')  # Black text for labels
                ax.set_ylabel("Number of Messages", fontsize=12, labelpad=10, color='black')  # Black text for labels
                ax.set_title("Most Busy Month", fontsize=14, pad=20, color='black')  # Black text for title

                # Set transparent background for the axes
                ax.set_facecolor('none')  # Transparent background for the plot area

                # Set color for tick labels
                ax.tick_params(colors='black')  # Black text for tick labels

                # Adjust layout to prevent clipping of labels
                plt.tight_layout()

                # Save the figure with a transparent background
                fig.patch.set_alpha(0.0)  # Fully transparent background for the figure

                # Display the plot in Streamlit
                st.pyplot(fig)

            except Exception as e:
                st.error(f"An error occurred while plotting the most busy month: {e}")

        # Weekly Activity Heatmap
        st.title("Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)

        try:
            # Convert heatmap values to integers
            user_heatmap = user_heatmap.fillna(0).astype(int)

            # Create a figure with a transparent background
            fig, ax = plt.subplots(figsize=(10, 6), facecolor='none')

            # Use a custom color palette (light to dark green)
            cmap = sns.light_palette("#25D366", as_cmap=True)

            # Plot the heatmap
            sns.heatmap(
                user_heatmap,
                cmap=cmap,
                annot=True,
                fmt="d",  # Now safe to use as all values are integers
                linewidths=0.5,
                linecolor='gray',
                annot_kws={"size": 10, "color": "black"},
                ax=ax
            )

            # Add labels and title with contrasting colors
            ax.set_xlabel("Hour of the Day", fontsize=12, labelpad=10, color='black')
            ax.set_ylabel("Day of the Week", fontsize=12, labelpad=10, color='black')
            ax.set_title("Weekly Activity Heatmap", fontsize=14, pad=20, color='black')

            ax.tick_params(colors='black')

            ax.set_facecolor('none')
            plt.tight_layout()
            fig.patch.set_alpha(0.0)

            # Display the plot in Streamlit
            st.pyplot(fig)

        except Exception as e:
            st.error(f"An error occurred while plotting the weekly activity heatmap: {e}")

        # Most Busy Users (Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')

            x, new_df = helper.most_busy_users(df)

            try:
                # Create figure and axis
                fig, ax = plt.subplots(figsize=(8, 5), facecolor='none')  # Transparent background

                col1, col2 = st.columns(2)

                with col1:
                    # Use a gradient color scheme (WhatsApp Green Shades)
                    colors = sns.color_palette("Reds", len(x))

                    # Create the bar plot
                    ax.bar(x.index, x.values, color=colors, edgecolor='black', linewidth=1.2)

                    # Customize appearance
                    ax.set_xlabel("Users", fontsize=12, labelpad=10, color='black')
                    ax.set_ylabel("Message Count", fontsize=12, labelpad=10, color='black')
                    ax.set_title("Most Busy Users", fontsize=14, pad=15, color='black')

                    # Rotate x-axis labels and set transparency
                    plt.xticks(rotation=45, ha='right', color='black')
                    plt.yticks(color='black')

                    # Add a subtle grid for readability
                    ax.grid(axis='y', linestyle='--', alpha=0.7)

                    # Set transparent background for axes
                    ax.set_facecolor('none')

                    # Adjust layout
                    plt.tight_layout()

                    # Display the improved bar chart
                    st.pyplot(fig)

                with col2:
                    # Style the dataframe
                    st.dataframe(new_df.style.set_properties(**{
                        'background-color': 'white',
                        'color': 'black',
                        'border': '1px solid black'
                    }))

            except Exception as e:
                st.error(f"An error occurred while plotting the most busy users: {e}")

        # WordCloud
        import random
        import streamlit as st
        import matplotlib.pyplot as plt
        from helper import create_wordcloud

        st.title("Chat Analysis Word Cloud")

        # Add some padding and styling
        st.markdown("""
        <style>
        .wordcloud-container {
            padding: 20px;
            background-color: rgba(255,255,255,0.1);
            border-radius: 10px;
            margin: 20px 0;
        }
        </style>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="wordcloud-container">', unsafe_allow_html=True)

            try:
                df_wc = create_wordcloud(selected_user, df)
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(df_wc, interpolation='bilinear')
                ax.axis('off')
                fig.patch.set_alpha(0)
                st.pyplot(fig, transparent=True)

            except Exception as e:
                st.error(f"Error generating word cloud: {e}")

            st.markdown('</div>', unsafe_allow_html=True)

        # Emoji Analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis ðŸŽ¨")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)  # Display the emoji dataframe

        with col2:
            try:
                # Create a smaller figure and axis
                fig, ax = plt.subplots(figsize=(5, 5))  # Smaller figure size

                # Remove the background (spines and grid)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.grid(False)
                ax.set_facecolor('none')  # Transparent background

                # Define a list of vibrant, distinct colors
                colors = ['#FF6F61', '#6B5B95', '#88B04B', '#FFA500', '#92A8D1', '#F7CAC9', '#955251', '#B565A7',
                          '#009B77', '#DD4124']

                # Explode the most used emoji slice for emphasis
                explode = [0.1 if i == 0 else 0 for i in range(len(emoji_df[1].head()))]

                # Create a pie chart
                wedges, texts, autotexts = ax.pie(
                    emoji_df[1].head(),  # Emoji frequencies
                    labels=emoji_df[0].head(),  # Emoji labels
                    autopct="%0.2f%%",  # Display percentages
                    colors=colors,  # Apply distinct colors
                    startangle=90,  # Rotate the pie chart for better readability
                    textprops={'fontsize': 10, 'fontweight': 'bold', 'fontfamily': 'Segoe UI Emoji'},
                    # Emoji-compatible font
                    wedgeprops={'edgecolor': 'black', 'linewidth': 1.5},  # Add borders to slices
                    shadow=True,  # Add shadow for a 3D effect
                    explode=explode  # Explode the most used emoji slice
                )

                # Set a title for the pie chart
                # ax.set_title("Top Emojis Used ðŸŽ‰", fontsize=14, pad=20, fontweight='bold', color='white')

                # Customize percentage text
                plt.setp(autotexts, size=8, weight="bold", color="white")

                # Make the chart background transparent
                fig.patch.set_alpha(0.0)

                # Center the pie chart in the column
                st.markdown(
                    """
                    <style>
                    .stPlot {
                        display: flex;
                        justify-content: center;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                # Display the plot in Streamlit with a transparent background
                st.pyplot(fig, bbox_inches='tight', transparent=True)

            except Exception as e:
                st.error(f"An error occurred while plotting the emoji analysis: {e}")

        # Message Length Distribution
        st.title("Message Length Distribution")
        try:
            fig = helper.message_length_distribution(selected_user, df)

            # Display the plot with adjusted size and transparent background
            st.pyplot(fig, transparent=True)

            # Close the figure properly
            plt.close(fig)
        except Exception as e:
            st.error(f"An error occurred while plotting the message length distribution: {e}")

        # Most Active Days
        st.title("Most Active Days")
        try:
            fig = helper.most_active_days(selected_user, df)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"An error occurred while plotting the most active days: {e}")

        # Sentiment Analysis
        st.title("Sentiment Analysis")
        try:
            # Get both figure and metrics
            fig, metrics = helper.sentiment_analysis(selected_user, df)

            col1, col2 = st.columns([3, 1])

            with col1:
                st.pyplot(fig, transparent=True)
                plt.close(fig)

            with col2:
                st.metric("Positive Messages", f"{metrics['positive_pct']:.1f}%")
                st.metric("Negative Messages", f"{metrics['negative_pct']:.1f}%")
                st.metric("Average Polarity", f"{metrics['avg_polarity']:.2f}")

        except Exception as e:
            st.error(f"An error occurred: {e}")

        # Inactive Users Analysis
        st.title("ðŸ‘¥ User Activity Dashboard")

        # Get inactive users data
        inactive_users, activity_df = helper.find_inactive_users(df, days=60)

        col1, col2 = st.columns(2)

        with col1:
            # Status summary card
            active_count = len(activity_df[activity_df['status'] == 'Active'])
            inactive_count = len(inactive_users)

            st.metric("Active Users", active_count,
                      help="Users active in the last 60 days")
            st.metric("Inactive Users", inactive_count,
                      delta=f"-{inactive_count}" if inactive_count else None,
                      delta_color="inverse",
                      help="Users inactive for 60 days")

        with col2:
            # Last activity heatmap
            st.write("### Last Activity Days Ago")
            fig, ax = plt.subplots(figsize=(6, 3), facecolor='none')
            sns.histplot(data=activity_df, x='days_inactive', bins=20,
                         kde=True, color='#FF6B6B', ax=ax)
            ax.set_facecolor('none')
            ax.set_xlabel('Days Since Last Activity')
            ax.set_ylabel('User Count')
            sns.despine()
            st.pyplot(fig, transparent=True)
            plt.close(fig)

    if st.sidebar.button("Generate PDF Report"):
        with st.spinner("Generating comprehensive report..."):
            try:
                report_file = pdf.generate_pdf_report(selected_user, df)

                with open(report_file, "rb") as f:
                    st.sidebar.download_button(
                        label="Download Full Report",
                        data=f,
                        file_name=report_file,
                        mime="application/pdf",
                        help="Download a comprehensive PDF report with all analyses"
                    )

                # Clean up the temporary file
                os.remove(report_file)

            except Exception as e:
                st.error(f"Failed to generate report: {str(e)}")