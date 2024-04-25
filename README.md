# WhatsApp Chat Analyzer

This Python application is built with Streamlit for analyzing WhatsApp chat conversations. It provides insights into various aspects of the chat, including message statistics, timelines, activity maps, word clouds, and more.

## Features

1. **Message Statistics:**
    - Total number of messages
    - Total words exchanged
    - Number of media messages shared
    - Number of links shared

2. **Monthly and Daily Timelines:**
    - Visualization of message activity over months and days respectively.

3. **Activity Map:**
    - Visualization of the busiest days and months.

4. **Most Active User:**
    - Identification of the most active user in the chat.

5. **Word Cloud:**
    - Visualization of most frequently used words, excluding stop words.

6. **Most Common Words:**
    - Tabular display of the most commonly used words.

7. **Emoji Analysis:**
    - Visualization and analysis of the most commonly used emojis.

## Usage

### Installation

- Ensure you have Python installed.
- Install the required packages listed in `requirements.txt`.

### Running the Application

- Run `streamlit run app.py` in your terminal.
- Upload your WhatsApp chat text file (without media) to the platform.
- Click on the "Analyse" button to generate insights.

## Variables

1. `uploaded_file`: Uploaded WhatsApp chat file.
2. `bytes_data`: File content in bytes.
3. `data`: Decoded file content as UTF-8.
4. `df`: Processed DataFrame containing chat data.
5. `user_list`: List of unique users in the chat.
6. `selected_user`: User selected for analysis.
7. `num_messages`: Total number of messages.
8. `words`: Total number of words exchanged.
9. `num_media_messages`: Number of media messages shared.
10. `num_links`: Number of links shared.
11. `timeline`: Monthly timeline data.
12. `daily_timeline`: Daily timeline data.
13. `busy_day`: Busiest day data.
14. `busy_month`: Busiest month data.
15. `x`: Most busy user data.
16. `new_df`: DataFrame for most busy user analysis.
17. `df_wc`: WordCloud data.
18. `most_common_df`: DataFrame for most common words analysis.
19. `emoji_df`: DataFrame for emoji analysis.

## Note

- Ensure that the WhatsApp chat text file is exported without media to ensure accurate analysis.
- The application provides both overall analysis and user-specific analysis for group chats.
- Some features such as word clouds may require additional stop word lists for different languages.

## Contributors

- Jinesh Prajapat

## Ack
- This application utilizes Streamlit for the web interface and various Python libraries for data processing and visualization.
