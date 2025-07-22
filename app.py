import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
st.sidebar.title("Whatsapp Chat Analyse")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    st.dataframe(df)
    user_list=df["user"].unique().tolist()
    user_list.remove("group notification")
    user_list.sort()
    user_list.insert(0,"overall")
    select_user = st.sidebar.selectbox("show analysis",user_list)
    if st.sidebar.button("Analylis"):
        total_msg,total_word,total_media_msg,total_link=helper.fetch_states(select_user,df)
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total message")
            st.title(total_msg)
        with col2:
            st.header("Total word")
            st.title(total_word)
        with col3:
            st.header("Total Media")
            st.title(total_media_msg)
        with col4:
            st.header("Total Link")
            st.title(total_link)

        if(select_user=="overall"):
            st.title("Most Busy Users")
            x,busy_user=helper.busyiest_chat(df)
            fig,ax=plt.subplots()
            ax.bar(x.index, x.values, color="red")
            ax.set_xlabel("Users")
            ax.set_ylabel("Message Count")
            plt.xticks(rotation="vertical")
            col1,col2=st.columns(2)
            with col1:
                st.pyplot(fig)
            with col2:
                st.dataframe(busy_user)
    st.title("Most Use Word")
    new_df=helper.most_use_word(select_user, df)
    st.dataframe(new_df)














