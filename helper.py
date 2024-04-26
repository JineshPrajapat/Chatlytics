import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import emoji
from urlextract import URLExtract
extract = URLExtract()
import io
from zipfile import ZipFile
import base64

def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['User'] ==selected_user]
    
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
    x = df['User'].value_counts().head()
    df = round((df['User'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns = {"index": "name", "User":"Users", "count":"Contribution(%)"})
    return x, df


def create_wordcloud(selected_user, df):

    f = open('stop_hinglish.txt')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['User'] ==selected_user]

    temp = df[df['User'] != "Group Notifications"]
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
        df = df[df['User'] == selected_user]

    temp = df[df['User'] != 'group_notification']
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
        df = df[df['User'] == selected_user]

    emojis = []
    for message in df['user_messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    if len(emojis)>0:
        emoji_counts = Counter(emojis)
        emoji_df = pd.DataFrame(emoji_counts.most_common(len(emoji_counts)))
        
        # Add a new column 'emojidescription' containing the code of each emoji
        emoji_df['emojidescription'] = emoji_df[0].apply(lambda x: emoji.demojize(x))

        # Rename the columns
        emoji_df.columns = ['emoji', 'counts', 'emojidescription']
    else:
        return emojis
    
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
            df = df[df['User'] ==selected_user]

    timeline = df.groupby(['Year', 'Month']).count()['user_messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))
    
    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != "Overall":
            df = df[df['User'] ==selected_user]

    daily_timeline = df.groupby('Date').count()['user_messages'].reset_index()
    return daily_timeline


def week_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]
        
    return df['Day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]
        
    return df['Month'].value_counts()


# Function to generate a zip file containing all plots
# Args plot_data (list): A list of Matplotlib figures to be included in the zip file.
# Returns str: Base64-encoded binary data of the zip file containing the plots.
def generate_all_plots_zip(plot_data):
    # Create a BytesIO buffer to hold the zip file
    with io.BytesIO() as zip_buffer:
        # Create a ZipFile object for writing the zip file
        with ZipFile(zip_buffer, "w") as zipf:
            for name, fig in plot_data:
                # Create a BytesIO buffer for each image
                with io.BytesIO() as img_buffer:
                    fig.savefig(img_buffer, format="png")
                    img_buffer.seek(0)
                    # Write the image to the zip file with a unique name
                    zipf.writestr(f"{name}.png", img_buffer.read())
        
        # Move the buffer cursor to the beginning and encode the zip file in base64
        zip_buffer.seek(0)
        b64 = base64.b64encode(zip_buffer.read()).decode()
        
        return b64
