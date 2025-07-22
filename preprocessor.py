import re
import pandas as pd
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s[apAP][mM]\s-\s'
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    dates_list = []
    for i in dates:
        dates_list.append(i.replace("\u202f", " "))

    df = pd.DataFrame({"user_message": message, "message_date": dates})
    df["message_date"] = df["message_date"].str.strip()
    df["message_date"] = pd.to_datetime(df["message_date"], format="%d/%m/%Y, %I:%M %p -")
    df.rename(columns={"message_date": "date"}, inplace=True)
    users = []
    mesages = []
    for i in df["user_message"]:
        entry = re.split(r"([\w\s+]+):\s?(.*)", i)
        if (entry[1:]):
            users.append(entry[1])
            mesages.append(entry[2])
        else:
            users.append("group notification")
            mesages.append(entry[0])
    df["user"] = users
    df["message"] = mesages
    df.drop(columns=["user_message"], inplace=True)
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month_name()
    df["hour"] = df["date"].dt.hour
    df["minutes"] = df["date"].dt.minute

    return df
