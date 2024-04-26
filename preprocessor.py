import  re
import pandas as pd

def preprocess(data):
    pattern = '\d{2}/\d{2}/\d{2}, \d{2}:\d{2}'
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({"user_message" : message, "message_date":dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format = '%d/%m/%y, %I:%M')
    df.rename(columns = {'message_date':'DateTime'}, inplace=True)

    # spliting date into year, month, date, hours, minutes
    df['Date'] = df['DateTime'].dt.date
    df['Year']=df['DateTime'].dt.year
    df['Month']=df['DateTime'].dt.month_name()
    # df['Day']=df['DateTime'].dt.day
    df['Day_name'] = df['DateTime'].dt.day_name()
    df['Hours']=df['DateTime'].dt.hour
    # df['minutes']=df['DateTime'].dt.minute
    df['time'] = df['DateTime'].dt.time

    # Separating am/pm from text message
    am_pm=[]
    messages=[]
    for message in df['user_message']:
            entry =re.split('(\S+)', message,maxsplit=1)
            if entry[1:]: #am/pm
                am_pm.append(entry[1])
                messages.append(entry[2])

        
    df['am_pm']= am_pm
    df['messages'] = messages

    # No need user_message column so removing it
    df.drop(columns = ['user_message'], inplace = True)

    # Remove hyphens present before every message in the 'messages' column
    df['messages'] = df['messages'].str.replace(r'-', '', regex=True)

    #extracting user from messages
    message_list = []
    user = []

    for message in df['messages']:
        # Check if the message starts with "Your security code with"
        if message.startswith("Your security code with"):
            # If the message starts with this content, append None to the user list
            user.append("Group Notifications")
            message_list.append(message)
        else:
            # Split the message at the first occurrence of ": "
            user_message_split = message.split(": ", 1)

            # Check if the split resulted in two parts
            if len(user_message_split) == 2:
                # Append only the first part of the split to the user list
                user.append(user_message_split[0])
                message_list.append(user_message_split[1])
            else:
                # If the split didn't occur, set user to None and use the original message
                user.append("Group Notifications")
                message_list.append(message)

    df['user_messages'] = message_list
    df['User'] = user

    # No need of messages column as split into two columns user_message and users
    df.drop(columns = ['messages'], inplace=True)

    # Remove rows where the length of the 'users' column is greater than 30 characters
    df = df[df['User'].str.len() <= 30]

    return df


