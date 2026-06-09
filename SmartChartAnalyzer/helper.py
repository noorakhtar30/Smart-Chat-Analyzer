from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import matplotlib.pyplot as plt
import seaborn as sns

extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df
from wordcloud import WordCloud
import random
import matplotlib.colors as mcolors

def create_wordcloud(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[(df['user'] != 'group_notification') &
              (df['message'] != '<Media omitted>\n')]

    def remove_stop_words(message):
        return ' '.join(word for word in message.lower().split()
                       if word not in stop_words)

    # Professional color palette with harmonious colors
    def professional_color_func(word, **kwargs):
        colors = [
            "#2596BE",  # Sophisticated blue
            "#26BF53",  # Elegant purple
            "#5FBF26",  # Warm orange
            "#26BF83",  # Nature green
            "#26BF99",  # Rich violet
            "#26B5BF"   # Muted green
        ]
        return random.choice(colors)

    wc = WordCloud(
        width=800,
        height=400,
        background_color=None,
        mode='RGBA',
        min_font_size=14,
        max_font_size=120,
        relative_scaling=0.5,
        prefer_horizontal=0.75,
        font_path='arialbd.ttf',
        color_func=professional_color_func,
        collocations=False,
        contour_width=1,
        contour_color='rgba(255,255,255,0.2)',
        margin=2,
        random_state=42
    )

    temp['message'] = temp['message'].apply(remove_stop_words)
    return wc.generate(temp['message'].str.cat(sep=" "))



def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap

def plot_and_return_fig(plt_func, *args, **kwargs):
    """Helper function to create, plot, and return a matplotlib figure."""
    fig = plt.figure(figsize=(7, 5))  # Set default figure size
    plt_func(*args, **kwargs)
    plt.tight_layout()  # Adjust layout
    return fig


def message_length_distribution(selected_user, df):
    """Plot the distribution of message lengths with a modern style."""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['message_length'] = df['message'].apply(len)

    # Create smaller figure with transparent background
    fig, ax = plt.subplots(figsize=(5, 3), facecolor='none')

    # Custom styling
    sns.set_style("whitegrid", {'grid.color': '.9'})
    sns.histplot(df['message_length'], bins=30, kde=True,  # Reduced bins for smaller plot
                 color='#4B8BBE', edgecolor='#306998', linewidth=0.5, ax=ax)

    # Styling the plot with smaller fonts
    ax.set_xlabel('Message Length', fontsize=8, color='#333333')
    ax.set_ylabel('Frequency', fontsize=8, color='#333333')

    # Customize spines and grid
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#dddddd')
    ax.spines['bottom'].set_color('#dddddd')

    # Customize ticks
    ax.tick_params(colors='#666666', which='both', labelsize=8)

    # Make background transparent
    ax.set_facecolor('none')

    plt.tight_layout()
    return fig


def user_contribution_over_time(selected_user, df):
    """Visualize user contribution trends over time."""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_trend = df.groupby(['only_date', 'user']).count()['message'].unstack().fillna(0)
    plt.figure(figsize=(7,5))
    user_trend.plot()
    plt.title('User Contribution Over Time')
    plt.xlabel('Date')
    plt.ylabel('Message Count')
    plt.legend(title="Users")
    plt.grid()
    return plt


def most_active_days(selected_user, df):
    """Show top 10 most active specific dates with modern styling."""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Convert to datetime if not already
    df['only_date'] = pd.to_datetime(df['only_date'])

    # Get top 10 active dates
    active_dates = df['only_date'].value_counts().head(10)

    # Create figure with transparent background
    fig, ax = plt.subplots(figsize=(7, 4), facecolor='none')

    # Create bar plot with custom styling
    sns.barplot(
        x=active_dates.index.astype(str),  # Convert dates to strings for cleaner display
        y=active_dates.values,
        palette="viridis",
        edgecolor='black',
        linewidth=0.5,
        ax=ax
    )

    # Styling
    ax.set_title('Top 10 Most Active Dates', fontsize=12, pad=15, color='#333333')
    ax.set_xlabel('Date', fontsize=10, color='#333333')
    ax.set_ylabel('Message Count', fontsize=10, color='#333333')
    plt.xticks(rotation=45, ha='right')

    # Remove spines and customize
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color('#dddddd')

    # Customize grid and ticks
    ax.grid(axis='y', color='#eeeeee')
    ax.tick_params(colors='#666666')

    # Transparent background
    ax.set_facecolor('none')

    plt.tight_layout()
    return fig


from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
import re


def sentiment_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Internal helper functions
    def preprocess_text(text):
        text = str(text)
        text = re.sub(r'http\S+|www\S+|@\w+', '', text)  # Remove URLs/mentions
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        return text.strip().lower()

    def get_sentiment_percentage(sentiment_df, sentiment_type):
        """Calculate percentage of messages with specific sentiment."""
        if sentiment_type == 'Positive':
            count = sentiment_df[sentiment_df['sentiment'].isin(['Positive', 'Very Positive'])].shape[0]
        elif sentiment_type == 'Negative':
            count = sentiment_df[sentiment_df['sentiment'].isin(['Negative', 'Very Negative'])].shape[0]
        else:
            count = sentiment_df[sentiment_df['sentiment'] == sentiment_type].shape[0]
        return (count / len(sentiment_df)) * 100

    def get_average_polarity(sentiment_df):
        """Calculate average polarity score."""
        return sentiment_df['polarity'].mean()

    # Text preprocessing
    df['clean_msg'] = df['message'].apply(preprocess_text)

    # Calculate polarity
    df['polarity'] = df['clean_msg'].apply(lambda x: TextBlob(x).sentiment.polarity)

    # Sentiment analysis with intensity
    def get_sentiment(text):
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity

        # Enhanced categorization
        if polarity > 0.3:
            return 'Very Positive'
        elif polarity > 0:
            return 'Positive'
        elif polarity < -0.3:
            return 'Very Negative'
        elif polarity < 0:
            return 'Negative'
        else:
            return 'Neutral'

    df['sentiment'] = df['clean_msg'].apply(get_sentiment)

    # Sentiment counts with order
    sentiment_order = ['Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive']
    sentiment_counts = df['sentiment'].value_counts().reindex(sentiment_order).fillna(0)

    # Create figure with transparent background
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='none')
    plt.rcParams['axes.facecolor'] = 'none'

    # Custom color palette
    colors = ['#ff6666', '#ff9999', '#cccccc', '#99ff99', '#66ff66']

    # Create plot
    sns.barplot(x=sentiment_counts.values, y=sentiment_counts.index,
                palette=colors, edgecolor='black', linewidth=0.5)

    # Add percentage labels
    total = len(df)
    for i, value in enumerate(sentiment_counts.values):
        percentage = f'{(value / total) * 100:.1f}%'
        plt.text(value + 5, i, f'{value}\n({percentage})', va='center')

    # Styling
    ax.set_title('Sentiment Distribution', fontsize=14, pad=15, color='#333333')
    ax.set_xlabel('Number of Messages', fontsize=10, color='#333333')
    ax.set_ylabel('Sentiment', fontsize=10, color='#333333')
    ax.grid(axis='x', color='#eeeeee')

    # Remove spines
    sns.despine(left=True, bottom=True)

    # Transparent background
    ax.set_facecolor('none')
    fig.patch.set_alpha(0.0)

    plt.tight_layout()

    # Return both figure and calculated metrics
    metrics = {
        'positive_pct': get_sentiment_percentage(df, 'Positive'),
        'negative_pct': get_sentiment_percentage(df, 'Negative'),
        'avg_polarity': get_average_polarity(df)
    }

    return fig, metrics



def top_chat_partners(df):
    """Iden

    tify top chat partners based on the number of interactions."""
    chat_counts = df['user'].value_counts().head(10)
    plt.figure(figsize=(7,5))
    sns.barplot(x=chat_counts.values, y=chat_counts.index, palette="coolwarm")
    plt.title('Top 10 Active Chat Partners')
    plt.xlabel('Message Count')
    plt.ylabel('User')
    plt.grid()
    return plt


def word_frequency_analysis(selected_user, df):
    """Analyze the most frequently used words."""
    from collections import Counter
    import string

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    words = []
    for message in df['message']:
        words.extend(message.lower().translate(str.maketrans('', '', string.punctuation)).split())

    word_counts = Counter(words).most_common(20)
    words, counts = zip(*word_counts)

    plt.figure(figsize=(7,5))
    sns.barplot(x=counts, y=words, palette='mako')
    plt.title('Top 20 Most Frequent Words')
    plt.xlabel('Count')
    plt.ylabel('Words')
    plt.grid()
    return plt


def response_time_analysis(selected_user, df):
    """Analyze response times between consecutive messages."""
    import pandas as pd

    # Check if 'date' column exists
    if 'date' not in df.columns:
        raise KeyError("The expected 'date' column is missing. Please check preprocessing.")

    # Convert to datetime if not already in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Sort messages by time
    df = df.sort_values('date')

    # Calculate response times (difference between consecutive messages)
    df['response_time'] = df['date'].diff().dt.total_seconds()

    # Drop NaN values resulting from the difference calculation
    df = df.dropna(subset=['response_time'])

    # Plot response time distribution
    plt.figure(figsize=(7,5))
    sns.histplot(df['response_time'], bins=50, kde=True, color='blue')
    plt.title('Response Time Distribution')
    plt.xlabel('Response Time (seconds)')
    plt.ylabel('Frequency')
    plt.grid()

    return plt







def conversation_starters(df, time_threshold=30):
    """
    Identify which user starts the most conversations.

    Args:
    df (pd.DataFrame): WhatsApp chat data with 'user' and 'date' columns.
    time_threshold (int): Time gap in minutes to define a new conversation.

    Returns:
    pd.DataFrame: Users with their conversation start counts.
    """
    df = df.sort_values(by="date")  # Ensure messages are sorted by time
    df["time_diff"] = df["date"].diff().dt.total_seconds().div(60)  # Time gap in minutes
    df["new_conversation"] = df["time_diff"] > time_threshold  # Identify new conversations
    starters = df[df["new_conversation"]]["user"].value_counts().reset_index()
    starters.columns = ["User", "Conversations Started"]
    return starters


def response_time_analysis(df):
    """
    Calculate the average response time for each user.

    Args:
    df (pd.DataFrame): WhatsApp chat data with 'user' and 'date' columns.

    Returns:
    pd.DataFrame: Users with their average response times in minutes.
    """
    df = df.sort_values(by="date")  # Ensure messages are sorted by time
    df["response_time"] = df["date"].diff().dt.total_seconds().div(60)  # Calculate response time in minutes
    df["prev_user"] = df["user"].shift(1)  # Previous message's sender

    # Exclude cases where the same user sends consecutive messages
    response_df = df[df["user"] != df["prev_user"]]

    # Calculate average response time per user
    avg_response_time = response_df.groupby("user")["response_time"].mean().reset_index()
    avg_response_time.columns = ["User", "Avg Response Time (min)"]

    # Fill NaN values with 0 (if a user never got a response)
    avg_response_time["Avg Response Time (min)"] = avg_response_time["Avg Response Time (min)"].fillna(0)

    # Sort users by response time (fastest first)
    avg_response_time = avg_response_time.sort_values(by="Avg Response Time (min)")

    return avg_response_time


def find_inactive_users(df, days=60):
    """Identify inactive users with visualization support."""
    recent_date = df["date"].max()
    cutoff_date = recent_date - pd.Timedelta(days=days)

    # Get activity status
    active_users = df[df["date"] > cutoff_date]["user"].unique()
    all_users = df["user"].unique()
    inactive_users = list(set(all_users) - set(active_users))

    # Prepare data for visualization
    user_activity = []
    for user in all_users:
        last_active = df[df['user'] == user]['date'].max()
        days_inactive = (recent_date - last_active).days
        user_activity.append({
            'user': user,
            'last_active': last_active,
            'days_inactive': days_inactive,
            'status': 'Inactive' if user in inactive_users else 'Active'
        })

    activity_df = pd.DataFrame(user_activity)

    return inactive_users, activity_df
