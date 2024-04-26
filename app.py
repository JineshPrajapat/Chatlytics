import streamlit as st
import preprocessor, helper 
import pandas as pd
import matplotlib.pyplot as plt
import math
import datetime
import time
import warnings
import numpy as np
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Chatlytics", page_icon=":signal_strength:", layout="wide")
st.sidebar.title("Welcome to WhatsApp Chat Analyser!")
st.title(":signal_strength: Chatlytics | The WhatsApp Chat Analyzer")
st.markdown("##")

st.write("👉 WhatsApp > Chat > Three dots > More > Export chat > Without media > Send or save the exported .txt file to your device.")
uploaded_file = st.file_uploader(":file_folder: Upload a WhatsApp Chat Exported (*.txt) File to Get Insights:",type=["txt"])
st.markdown("##")

if uploaded_file is None:
    st.sidebar.markdown("##")
    st.sidebar.markdown(''':red_circle:  Export your WhatsApp chat (without media), whether it be a group chat or an individual/private chat, then click on "Browse Files" and upload it to this platform.''')
    st.sidebar.markdown(''':red_circle:  Afterward, kindly proceed to click on the "Analyse" button. This action will generate a variety of insights concerning your conversation.''')
    st.sidebar.markdown(''':red_circle:  You will have the option to select the type of analysis, whether it is an overall analysis or one that specifically focuses on particular participants' analysis.''')


if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.write("")

    with st.expander("Processed WhatsApp Chat Data"):
        st.dataframe(df)


    # fetch unique user
    user_list = df['User'].unique().tolist()
    user_list.remove('Group Notifications')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("User", user_list)


    # setting up buttons
    if st.button("Show Analysis"):
        plot_data=[]
        with st.spinner("Analysing Data..."):
            time.sleep(2)
        with st.spinner("Getting Data..."):
            time.sleep(2)
            

        col9 = st.sidebar.tabs(["OVERALL CHAT ANALYSIS"])
        tab1 ,tab2 ,tab3 ,tab4, tab5, tab6, tab7, tab8 = st.tabs(["Top Statisctics", "Monthly TimeLine", "Daily TimeLine", "Activity Map", "User Who Chats the Most", "Wordcloud", "Most commmon words", "Emoji Analysis" ])

        with tab1:
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
        with tab2:
            st.title("Monthly TimeLine")
            timeline = helper.monthly_timeline(selected_user, df)
            fig_monthly_timeline, ax = plt.subplots()
            plt.plot(timeline['time'], timeline['user_messages'], color="green")
            plt.xticks(rotation="vertical")
            ax.set_xlabel('Month')
            ax.set_ylabel('Message Count')
            ax.set_title('Message Count Over Month')
            st.pyplot(fig_monthly_timeline)

            st.markdown("##")


        #daily timeline
        with tab3:
            st.title("Daily TimeLine")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig_daily_timeline, ax = plt.subplots()
            plt.plot(daily_timeline['Date'], daily_timeline['user_messages'], color="green")
            plt.xticks(rotation="vertical")
            ax.set_xlabel('Date')
            ax.set_ylabel('Message Count')
            ax.set_title('Message Count Over Date')
            st.pyplot(fig_daily_timeline)

            st.markdown("##")


        #activit map
        with tab4:
            st.title("Activity_Map")
            col1, col2 = st.columns(2)

            with col1:
                st.header("Most Busy Day")
                busy_day = helper.week_activity_map(selected_user, df)
                fig_week_activity_map, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values)
                plt.xticks(rotation='vertical')
                ax.set_xlabel('Days of the week')
                ax.set_ylabel('Message Count')
                ax.set_title('Top messaging day')
                st.pyplot(fig_week_activity_map)

            with col2:
                st.header("Most Busy Month")
                busy_month = helper.month_activity_map(selected_user, df)
                fig_month_activity_map, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color="orange")
                plt.xticks(rotation='vertical')
                ax.set_xlabel('Month')
                ax.set_ylabel('Message Count')
                ax.set_title('Top messaging months')
                st.pyplot(fig_month_activity_map)

            st.markdown("##")


        # Most active user
        with tab5:
            st.title("User Who Chats the Most")
            if selected_user == "Overall":
                x, new_df = helper.most_busy_user(df)
                
                col1, col2 = st.columns(2)

                with col1:
                    fig_most_active_user, ax = plt.subplots()
                    ax.bar(x.index, x.values, color="red")
                    plt.xticks(rotation = "vertical")
                    ax.set_xlabel('User')
                    ax.set_ylabel('Message Count')
                    ax.set_title('Top Users by Message Count')
                    st.pyplot(fig_most_active_user)

                with col2:
                    st.dataframe(new_df)
            else:
                st.markdown("Only applied in group chats")


        # WordCloud
        with tab6:
            st.title("Wordcloud")
            df_wc = helper.create_wordcloud(selected_user, df)

            if df_wc is not None:
                    fig, ax = plt.subplots()
                    # Remove the axis and tick labels
                    ax.set_axis_off()
                    ax.imshow(df_wc)
                    st.pyplot(fig)

                    st.markdown("##")
            
            else:
                st.warning("Insufficient chat text for creating a meaningful word cloud.")

        
        # most common words
        with tab7:
            st.title('Most commmon words')
            most_common_df = helper.most_common_words(selected_user,df)

            col1, col2 = st.columns(2)

            if len(most_common_df)>0:
                with col1:
                    fig_most_common_words,ax = plt.subplots()
                    ax.barh(most_common_df[0],most_common_df[1])
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig_most_common_words)

                with col2:
                    st.dataframe(most_common_df)
            else:
                st.markdown("No common words are present")

            st.markdown("##")


        #most common emojis analysis
        with tab8:
            st.title("Emoji Analysis")
            emoji_df = helper.common_emoji(selected_user, df)

            col1, col2 = st.columns(2)
            
            if len(emoji_df) > 0:
                with col1:
                    emojis = emoji_df['emojidescription'].head()
                    counts = emoji_df['counts'].head()

                    fig_common_emoji, ax = plt.subplots()
                    ax.barh(emojis,counts, color="red")
                    ax.set_yticks(np.arange(len(emojis)))
                    ax.set_yticklabels(emojis)
                    ax.set_xlabel('Counts')
                    ax.set_title('Emoji Analysis')
                    st.pyplot(fig_common_emoji)
            
                with col2:
                    st.dataframe(emoji_df)
            
            else:
                st.markdown("No emojis are shared by user")

            st.markdown("##")


        # Add a new tab for combined data in sidebar
        with col9[0]:
            st.title("Top Statistics")
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

            st.subheader("Monthly Timeline")
            st.pyplot(fig_monthly_timeline)
            plot_data.append(("MonthlyTimeLine", fig_monthly_timeline))

            st.subheader("Daily Timeline")
            st.pyplot(fig_daily_timeline)
            plot_data.append(("DailyTimeLine", fig_daily_timeline))

            st.subheader("Activity Map")
            st.pyplot(fig_week_activity_map)
            plot_data.append(("MostBusyDay", fig_week_activity_map))
            st.pyplot(fig_month_activity_map)
            plot_data.append(("MostBusyMonth", fig_month_activity_map))

            if selected_user == "Overall":
                st.subheader("Most Active User")
                st.pyplot(fig_most_active_user)
                plot_data.append(("MostActiveUsers", fig_most_active_user))
                st.write(new_df)
            

            st.subheader("Wordcloud")
            if df_wc is not None:
                st.image(df_wc.to_array(), use_column_width=True)
            else:
                st.warning("Insufficient chat text for creating a meaningful word cloud.")

            st.subheader("Most Common Words")
            most_common_df = helper.most_common_words(selected_user,df)
            if len(most_common_df)>0:
                st.pyplot(fig_most_common_words)
                plot_data.append(("Mostcommmonwords", fig_most_common_words))
            else:
                st.markdown("No common words are present")


            st.subheader("Emoji Analysis")
            emoji_df = helper.common_emoji(selected_user, df)
            if len(emoji_df)>0:
                st.write(emoji_df)
                st.pyplot(fig_common_emoji)
                plot_data.append(("MostcommonEmoji", fig_common_emoji))
            else:
                st.markdown("No emojis are shared by user")

        # Fetch data from individual tabs
        fig_monthly_timeline = plt.gcf()
        fig_daily_timeline = plt.gcf()
        fig_week_activity_map = plt.gcf()
        fig_month_activity_map = plt.gcf()
        fig_most_common_words = plt.gcf()
        fig_common_emoji = plt.gcf()
        fig_most_active_user = plt.gcf()


#========================== DOWNLOAD BUTTON ==========================
        if plot_data:
            all_plots_zip_data = helper.generate_all_plots_zip(plot_data)
    
            # Define button CSS
            button_style = """
                background-color: #24A19C;
                color: #fff;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
            """

            st.markdown(f'<a href="data:file/zip;base64,{all_plots_zip_data}" download="all_plots.zip"><button style="{button_style}">Download All Plots</button></a>', unsafe_allow_html=True)

        st.markdown("##")


#========================== FOOTER ==========================

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

