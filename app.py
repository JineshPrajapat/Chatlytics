import streamlit as st
import preprocessor, helper 
import pandas as pd
import matplotlib.pyplot as plt
import math
import datetime
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Chatlytics", page_icon=":signal_strength:", layout="wide")

st.sidebar.title("Welcome to WhatsApp Chat Analyser!")
st.title(":signal_strength: Chatlytics | The WhatsApp Chat Analyzer")
st.markdown("##")

st.write("👉 WhatsApp > Chat > Three dots > More > Export chat > Without media > Send or save the exported .txt file to your device.")

uploaded_file = st.file_uploader(":file_folder: Upload a WhatsApp Chat Exported (*.txt) File to Get Insights:",type=["txt"])
st.markdown("##")

if uploaded_file is None:
    st.markdown('''Please export your WhatsApp chat (without media), whether it be a group chat or an individual/private chat, then click on "Browse Files" and upload it to this platform.''')
    st.markdown('''Afterward, kindly proceed to click on the "Analyse" button. This action will generate a variety of insights concerning your conversation.''')
    st.markdown(''' You will have the option to select the type of analysis, whether it is an overall analysis or one that specifically focuses on particular participants' analysis.''')


if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.write("")

    with st.expander("Processed WhatsApp Chat Data"):
        st.dataframe(df)

    # st.dataframe(df)

    #fetch unique user
    user_list = df['users'].unique().tolist()
    user_list.remove('Group Notifications')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Users", user_list)

    # setting up buttons
    if st.button("Show Analysis"):
        
        st.title("Top Statistics")
        num_messages, words, num_media_messages, num_links, num_emojis = helper.fetch_stats(selected_user,df)
        col1, col2, col3 = st.columns(3)
        st.markdown("##")
        col4, col5, col6 = st.columns(3)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        
        with col2:
            st.header("Total words")
            st.title(words)

        with col3:
            st.header("Media shared")
            st.title(num_media_messages)
        
        with col4:
            st.header("Links shared")
            st.title(num_links)
        
        with col5:
            st.header("Average Words per Message")
            st.title(math.ceil(words/num_messages))
        
        with col6:
            st.header("Emojis shared")
            st.title(num_emojis)

        st.markdown("##")

        
        #Monthly timeline
        st.title("Monthly TimeLine")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(timeline['time'], timeline['user_messages'], color="green")
        plt.xticks(rotation="vertical")
        ax.set_xlabel('Month')
        ax.set_ylabel('Message Count')
        ax.set_title('Message Count Over Month')
        st.pyplot(fig)

        st.markdown("##")

        #daily timeline
        st.title("Daily TimeLine")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(daily_timeline['only_date'], daily_timeline['user_messages'], color="black")
        plt.xticks(rotation="vertical")
        ax.set_xlabel('Date')
        ax.set_ylabel('Message Count')
        ax.set_title('Message Count Over Date')
        st.pyplot(fig)

        st.markdown("##")

        #activit map
        st.title("Activity_Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            ax.set_xlabel('Days of the week')
            ax.set_ylabel('Message Count')
            ax.set_title('Top messaging day')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color="orange")
            plt.xticks(rotation='vertical')
            ax.set_xlabel('Month')
            ax.set_ylabel('Message Count')
            ax.set_title('Top messaging months')
            st.pyplot(fig)

        st.markdown("##")

        # Most active user
        if selected_user == "Overall":
            st.title("User Who Chats the Most")
            x, new_df = helper.most_busy_user(df)
            
            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color="red")
                plt.xticks(rotation = "vertical")
                ax.set_xlabel('User')
                ax.set_ylabel('Message Count')
                ax.set_title('Top Users by Message Count')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)

        if df_wc is not None:
                fig, ax = plt.subplots()
                # Remove the axis and tick labels
                ax.set_axis_off()
                ax.imshow(df_wc)
                st.pyplot(fig)
                # plot_data.append(("WordCloud", fig))

                st.markdown("##")
        
        else:
            st.warning("Insufficient chat text for creating a meaningful word cloud.")

        # most common words
        st.title('Most commmon words')
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.pyplot(fig)

        st.markdown("##")

        #most common emojis analysis
        st.title("Emoji Analysis")
        emoji_df = helper.common_emoji(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1], labels = emoji_df[0], autopct="%0.2f")
            st.pyplot(fig)
        
        st.markdown("##")


#---- Footer Area----

hide_st_style = """
    <style>
    #MainMenu {visibility : hidden;}
    header {visibility : hidden;}
    </style>
"""
st.markdown(hide_st_style,unsafe_allow_html=True)

# Get the current date and time
now = datetime.datetime.now()

# Format the copyright information
copyright = f"&copy; {now.year} Chatlytics"

footer = """
    <style>
        .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
        }
    </style>
    <footer class="footer">
        \U0001F512  We do not share or store your data beyond the scope of this application.<br>
        """+ copyright +""".
        Developed with \U00002764 by Jinesh Prajapat
    </footer>
    """
st.markdown(footer,unsafe_allow_html=True)

