# -- coding: utf-8 --
# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python
import os
import pandas as pd
import json
from textblob import TextBlob
import streamlit as st
import googleapiclient.discovery
id = st.text_input('enter youtube ID')
index = id.rfind("=")
id = id[index+1:]
def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # DO NOT leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyDOPKooAHk_s9ZoFC0izz5Etic9KfcyxhI"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
    request = youtube.commentThreads().list(
        part="id,snippet,replies",
        order="relevance",
        videoId=id
    )
    response = request.execute()
    def create_df_author_comments():
        authorname = []
        comments = []
        for i in range(len(response["items"])):
            authorname.append(response["items"][i]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"])
            comments.append(response["items"][i]["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
        df_1 = pd.DataFrame(comments, index = authorname,columns=["Comments"])
        return df_1 
    df_1 = create_df_author_comments()
    positive = []
    negative = []
    neutral = []
    for i in range(len(df_1)):
        res =  TextBlob(df_1.iloc[i,0])
        result = res.sentiment.polarity
        if result > 0 :
            positive.append(df_1.iloc[i,0]) 
        if result < 0:
            negative.append(df_1.iloc[i,0])  
        if result == 0:
            neutral.append(df_1.iloc[i,0])      
    st.write("Postive Comments")
    st.write(positive)
    st.write("Negative Comments")
    st.write(negative)
    st.write("Neutral Comments")
    st.write(neutral)
if __name__ == "__main__":
    main()