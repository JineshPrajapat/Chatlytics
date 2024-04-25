import streamlit as st
import preprocessor, helper 
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="WhatsApp Chat Analyzer", page_icon=":speech_balloon:")

st.sidebar.title("WhatsApp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is None:
    st.markdown('''Please export your WhatsApp chat (without media), whether it be a group chat or an individual/private chat, then click on "Browse Files" and upload it to this platform.''')
    st.markdown('''Afterward, kindly proceed to click on the "Analyse" button. This action will generate a variety of insights concerning your conversation.''')
    st.markdown(''' You will have the option to select the type of analysis, whether it is an overall analysis or one that specifically focuses on particular participants' analysis.''')
    st.markdown('Thank You!')
    st.markdown('Jinesh Prajapat')

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.title("WhatsApp Chat Analysis")
    st.write("")

    # st.dataframe(df)

    #fetch unique user
    user_list = df['users'].unique().tolist()
    user_list.remove('Group Notifications')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    # setting up buttons
    if st.sidebar.button("Show Analysis"):
        
        st.title("Top Statistics")
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)

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

        
        #Monthly timeline
        st.title("Monthly TimeLine")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(timeline['time'], timeline['user_messages'], color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        #daily timeline
        st.title("Daily TimeLine")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(daily_timeline['only_date'], daily_timeline['user_messages'], color="black")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)


        #activit map
        st.title("Activity_Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color="orange")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        # Most active user
        if selected_user == "Overall":
            st.title("Most  Busy User")
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color="red")
                plt.xticks(rotation = "vertical")
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title('Most commmon words')
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.pyplot(fig)

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

