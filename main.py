#importing important libraries
import streamlit as st

import pandas as pd
import numpy as np

from textblob import TextBlob
from wordcloud import WordCloud
from PIL import Image

import tweepy
import re

import matplotlib.pyplot as plt
import seaborn as sns

from streamlit_lottie import st_lottie
#from googletrans import Translator
import requests

#import streamlit.components.v1 as components
import warnings
warnings.filterwarnings('ignore')



df=pd.read_csv("tweeter api key.csv")
feedback_df=pd.read_csv('Feedback.csv')

#Tweeter API credentials
consumer_key=df['Key'][0]
consumer_secret_key=df['Key'][1]
access_token=df['Key'][3]
access_token_secret=df['Key'][4]

#creating the othentication object
authentication=tweepy.OAuthHandler(consumer_key,consumer_secret_key)

#set the access token and access token secret
authentication.set_access_token(access_token,access_token_secret)

#creat the API object while passing the auth information
api=tweepy.API(authentication, wait_on_rate_limit=True)




# Creating a function to clean the tweets
def clean(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', str(text))  # it removes @mentions
    text = re.sub(r'#', '', str(text))  # removeing '#' symbol from text
    text = re.sub(r':', '', str(text))  # removeing ':' symbol from text
    text = re.sub(r'RT[\S]+', '', str(text))  # removing RT(Re Tweet) tagged with the text
    text = re.sub(r'http\S+', '', text)  # remove the hyper link
    # we put '?' after s in 'https' because it can be 'http' so '?' will take 's' as 0 or 1
    # i.e- no matter if 's' condition is fullfilled or not it will remove it
    # r tells the python that it is a raw string
    return text





# Create a function to compute the negetive, positive and nutral analysis
def get_sentiments(polarity):
    if polarity < 0:
        return 'Negetive'
    elif polarity == 0:
        return 'Nutral'
    else:
        return 'Positive'



# creatting a function to create subjectivity
def get_subjectivity(text):
    return TextBlob(text).sentiment.subjectivity


# creating function for checking polarity
def GetPolarity(text):
    return TextBlob(text).sentiment.polarity


#function for animation
def animation(url:str):
    r=requests.get(url)
    if r.status_code!=200:
        return None
    return r.json()



sidebar=st.sidebar.radio('Menu',['Home','Tweeter Analysis','Feedback'])


#st.image('https://images.tv9hindi.com/wp-content/uploads/2022/04/twitter-deal.jpg', width=300)

#calling the animation function


#Architecture of Home page
if sidebar=='Home':

    st.header('Tweeter Analysis home page')
    an = animation('https://assets9.lottiefiles.com/packages/lf20_me2jebk7.json')
    st_lottie(an,height=400,width=400)

    st.title('Home Page')
    st.header('Hello :blush:')

    st.write('Welcome to my tweeter analysis page. Here you can write any tweeter username to fetch there tweets and can do analysis on the same :blush:')
    # Linkdin
    st.write('My name is Bishal you can go to my linkdin account through given link below')
    st.image('https://play-lh.googleusercontent.com/kMofEFLjobZy_bCuaiDogzBcUT-dz3BBbOrIEjJ-hqOabjK8ieuevGe6wlTD15QzOqw',width=100)
    st.write(':point_right:','https://www.linkedin.com/in/bishalkumardas/')
    # Github
    st.write('and the github link is given below this line')
    st.image('https://play-lh.googleusercontent.com/PCpXdqvUWfCW1mXhH1Y_98yBpgsWxuTSTofy3NGMo9yBTATDyzVkqU580bfSln50bFU',width=100)
    st.write(':point_right:','https://github.com/bishalkumardas')
    # Email Id
    st.write('and my email Id is given below this line')
    st.image('https://cdn2.downdetector.com/static/uploads/logo/image21.png',width=100)
    st.write(':point_right:', 'bishalkumardasofficial11@gmail.com')
    # Instagram
    st.write('and the my instagram link is given below this line')
    st.image('https://upload.wikimedia.org/wikipedia/commons/9/95/Instagram_logo_2022.svg',width=100)
    st.write(':point_right:', 'https://www.instagram.com/bishal4real/')



#Architecture of Tweeter Analysis page
if sidebar=='Tweeter Analysis':
    st.image('https://images.tv9hindi.com/wp-content/uploads/2022/04/twitter-deal.jpg', width=300)
    st.info('All the analysis in this page have been done on last 200 tweets of the user if 200 tweets were done')

    #Title of the page
    st.title('Tweeter Analysis')
    #Taking input from the user
    user_name=st.text_input('Write a tweeter handle User name for analysis')


    # extracting last 200 tweets from the tweeter user
    try:
        posts = api.user_timeline(screen_name=user_name, count=200, lang="en", tweet_mode="extended")

        n=st.number_input('Write the number of last tweet you want', min_value=1, step=1, max_value=200)

        # Creating Dataframe of tweet
        df_tweets = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweet'])

        st.write(f"Showing analysis of User Name {user_name} ")
    except Exception:
        n=0
        posts='no post'
        st.text(f'User ({user_name}) not found on tweeter please recheck the user name \nThis error is handled by Bishal')

    #Architecture for last tweet
    last_tweets=st.button(f'Show last {n} tweets')



    if last_tweets==True:
        st.write('If it shows (ConnectTimeout: timed out) click again')
        st.write(f'Last {n} tweets of user {user_name} are')
        num=1
        for i in posts[0:n]:
            st.write(f"{num} -> {i.full_text}")
            num=num+1


    # if st.button('Translate into english if not in english')==True:
    #
    #     # extracting last 100 tweets from the tweeter user
    #     posts = api.user_timeline(screen_name=user_name, count=100, lang="en", tweet_mode="extended")
    #
    #     # Creating Dataframe of tweet
    #     df_tweets = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweet'])
    #
    #
    #     #Translating tweets in english
    #     translator = Translator()
    #     Tweet = []
    #     for i in range(len(df_tweets)):
    #         Tweet.append(translator.translate(df_tweets['Tweet'][i]).text)
    #     df_tweets = pd.DataFrame(Tweet, columns=['Tweet'])
    #     st.write(df_tweets['Tweet'])

    if st.button('Show word cloud'):

        # # Translating tweets in english
        # translator = Translator()
        # Tweet = []
        # for i in range(len(df_tweets)):
        #     Tweet.append(translator.translate(df_tweets['Tweet'][i]).text)
        # df_tweets = pd.DataFrame(Tweet, columns=['Tweet'])

        #Cleaning the text
        try:
            df_tweets['Tweet'] = df_tweets['Tweet'].apply(clean)


            # Creating two new columns
            df_tweets['Subjectivity'] = df_tweets['Tweet'].apply(get_subjectivity)
            df_tweets['Polarity'] = df_tweets['Tweet'].apply(GetPolarity)

            all_words = ' '.join([tweet for tweet in df_tweets['Tweet']])
            mask=mask = np.array(Image.open("pngwing.com.png"))

            word_cloud = WordCloud(width=500, height=300,background_color='white', max_font_size=119,mask=mask,contour_width=1,contour_color='black').generate(all_words)
            fig, ax = plt.subplots()
            ax.imshow(word_cloud, interpolation='bilinear')  # 'plt.imshow' Display data as an image, i.e., on a 2D regular raster.
            plt.axis('off')

            st.pyplot(fig)
        except NameError:
            st.text('Write a valid user name for word cloud')
        except ValueError:
            st.text(f'For word cloud you need at least 1 word.\nThe user name ({user_name}) given by you have zero tweets')

    st.image('https://miro.medium.com/max/689/1*jHzNpL-KagnaHUSHzPTPkA.jpeg',width=340)

    if st.button('Show sentiments'):

        # Creating two new columns
        #df_tweets['Subjectivity'] = df_tweets['Tweet'].apply(get_subjectivity)
        try:
            df_tweets['Polarity'] = df_tweets['Tweet'].apply(GetPolarity)


            # Creating a new sentiments columns
            df_tweets['Sentiments'] = df_tweets['Polarity'].apply(get_sentiments)

            sentiment = df_tweets['Sentiments'].value_counts()


            fig, (bar, pie) = plt.subplots(2,1, figsize=(10,20))

            color = ['green','orangered','red']

            bar.bar(sentiment.index, sentiment.values, color=color)
            bar.set_title('Bar Graph')
            bar.set(xlabel='Sentimants', ylabel='Number of tweets')

            pie.pie(sentiment.values, labels=sentiment.index, explode=[0.03, 0.03, 0.1], shadow=True, autopct='%1.0f%%', startangle=80, colors=color)
            pie.set_title('Pie chart')

            plt.legend()
            st.pyplot(fig)


        except NameError:
            st.write('You have to write a valid user name for this analysis')
        except ValueError:
            st.text('You have to write a user name who have made some tweets for this analysis')

        # except TypeError as e:
        #     print(e)




#Architecture of feedback page
if sidebar=='Feedback':
    feedback_df = pd.read_csv('Feedback.csv')
    st.title('Feedback')
    an=animation('https://assets3.lottiefiles.com/packages/lf20_qq6gioyz.json')
    st_lottie(an)
    name = st.text_input('Write your name')
    email=st.text_input('Write your Email Id (*your email will not be shared on page and is safe with me to contact you if needed)')
    feedback=st.text_input('Write your experience and suggestion as a feedback here')

    if st.button('Send feedback'):
        new_data={'Name':name,'Email Id':email,'Feedback':feedback}
        feedback_df_2=pd.DataFrame(new_data,index=[len(new_data)])
        feedback_df=pd.concat([feedback_df_2,feedback_df],ignore_index=True)
        feedback_df.to_csv('Feedback.csv')
        st.success('Comment successfully submitted')
    st.write('Recent Feedbacks')
    feedback_df = pd.read_csv('Feedback.csv')
    for i,e in zip(feedback_df['Name'],feedback_df['Feedback']):
        st.write('Name: ',i)

        st.write('Feedback:',e)


