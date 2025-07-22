from urlextract import URLExtract
from nltk.corpus import stopwords
import string
from collections import Counter
import pandas as pd

def fetch_states(select_user,df):
     global media_msg1,df1
     if(select_user=="overall"):
         word = []
         for i in df["message"]:
             word.extend(i.split())
         media_msg=df[df["message"]=="<Media omitted>"].shape[0]
         extraxt = URLExtract()
         link = []
         for i in df["message"]:
             link.extend(extraxt.find_urls(i))
         item_to_remove = "B.Tech"
         while item_to_remove in link:
             link.remove(item_to_remove)
         return df["message"].shape[0],len(word),media_msg,len(link)
     else:
         if not df[df["user"]==select_user].empty:
             df1=df[df["user"]==select_user]
             word = []
             for i in df1["message"]:
                 word.extend(i.split())
             media_msg1=df1[df1["message"] == "<Media omitted>"].shape[0]
             link1 = []
             extraxt = URLExtract()
             for i in df1["message"]:
                 link1.extend(extraxt.find_urls(i))
             return df1.shape[0],len(word),media_msg1,len(link1)

def busyiest_chat(df):
    new_df=df[df["user"] != "group notification"]
    x=new_df["user"].value_counts().head()
    busy_user = round(new_df["user"].value_counts() / new_df.shape[0] * 100, 2).reset_index().rename(
        columns={"user": "Name", "count": "Percentage"})
    return x,busy_user

def most_use_word(select_user,df):
    f = open("stop_hinglish.txt", "r")
    hinglish_stop_word = f.read()
    if select_user=="overall":
        words_2 = []
        temp = df[df["user"] != "group notification"]
        temp = temp[temp["message"] != "<Media omitted>"]
        for text in temp["message"]:
            text = text.lower()
            for i in text.split():
                if i not in stopwords.words("english") and i not in string.punctuation and i not in hinglish_stop_word:
                    words_2.append(i)
        return(pd.DataFrame(Counter(words_2).most_common(20),columns=["words","Frequency"]))
    else:
        words_2 = []
        df1 = df[df["user"] == select_user]
        temp = df1[df1["message"] != "<Media omitted>"]
        for text in temp["message"]:
            text = text.lower()
            for i in text.split():
                if i not in stopwords.words("english") and i not in string.punctuation and i not in hinglish_stop_word:
                    words_2.append(i)
        return(pd.DataFrame(Counter(words_2).most_common(20),columns=["words","Frequency"]))

