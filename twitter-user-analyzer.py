import tweepy
import cv2
import urllib
import numpy as np
import json

f = open("config.json", 'rb')
config = json.load(f)
consumer_key = config["consumer_key"]
consumer_secret = config.["consumer_secret"]
access_token = config.["access_token"]
access_token_secret = config.["access_token_secret"]
opencv_dir = config.["opencv_dir"]
f.close()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

eye_cascade = cv2.CascadeClassifier(
    opencv_dir + "data/haarcascades/haarcascade_eye.xml")
face_cascade = cv2.CascadeClassifier(
    opencv_dir + "data/haarcascades/haarcascades_frontalface_alt.xml")
profile_face_cascade = cv2.CascadeClassifier(
    opencv_dir + "data/haarcascades/haarcascades_profileface.xml")

public_tweets = tweepy.Cursor(api.search, "ottawa music").items(20)
# result = """<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>"""
for tweet in public_tweets:
  req = urllib.urlopen(tweet.user.profile_image_url.replace("_normal", ""))
  arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
  img = cv2.imdecode(arr, -1)  # 'load it as it is'
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
  profile_face = profile_face_cascade.detectMultiScale(gray, 1.3, 5)
  detected = True if len(faces) or len(eyes) or len(profile_face) else False
  if detected:
    print "https://twitter.com/" + str(tweet.user.screen_name)
