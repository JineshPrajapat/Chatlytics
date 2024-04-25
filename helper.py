import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import emoji
from urlextract import URLExtract
extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] ==selected_user]
    
    # fetching of number of messages
    num_messages = df.shape[0]

    #fetching length of words
    words = []
    for message in df['user_messages']:
        words.extend(message.split())

    # fetching media 
    num_media_messages = df[df['user_messages'] == '<Media omitted>\n'].shape[0]

    # fetching links shared
    links = []
    for message in df['user_messages']:
        links.extend(extract.find_urls(message))
    
    #fetching num of emojis
    emojis = []
    for message in df['user_messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    
    # emoji_df  = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return num_messages, len(words), num_media_messages, len(links), len(emojis)


def most_busy_user(df):
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns = {"index": "name", "users":"percentage"})
    return x, df


def create_wordcloud(selected_user, df):

    f = open('stop_hinglish.txt')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['users'] ==selected_user]

    temp = df[df['users'] != "Group Notifications"]
    temp = temp[temp["user_messages"] != "<Media omitted>\n"]

    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color="white")
    temp['user_messages'] = temp['user_messages'].apply(remove_stop_words)
    df_wc = wc.generate(temp['user_messages'].str.cat(sep=""))

    return df_wc


def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['user_messages'] != '<Media omitted>\n']
    
    date_pattern = '\d{2}/\d{2}/\d{2}'
    temp = temp[~temp['user_messages'].str.contains(date_pattern)]

    words = []

    for message in temp['user_messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def common_emoji(selected_user, df):

    if selected_user != "Overall":
            df = df[df['users'] ==selected_user]

    emojis = []
    for message in df['user_messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    
    emoji_df  = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
            df = df[df['users'] ==selected_user]

    timeline = df.groupby(['year', 'month']).count()['user_messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != "Overall":
            df = df[df['users'] ==selected_user]

    daily_timeline = df.groupby('only_date').count()['user_messages'].reset_index()
    return daily_timeline


def week_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
        
    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
        
    return df['month'].value_counts()