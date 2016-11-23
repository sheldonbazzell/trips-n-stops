from django.shortcuts import render, redirect, HttpResponse
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import rauth, json

def yelp(request,location,term='restaurant'):
	params = {}
  	params["term"] = term
  	params["location"] = location
  	params["radius_filter"] = "8000"
  	params["limit"] = "10"
	#Obtain these from Yelp's manage access page
  	consumer_key = "szjwl0hfTZEnIZ0YMR3K7g"
  	consumer_secret = "OjSOA4XoTyzr5VG_lDwu1L2vbkE"
  	token = "NE6ro_inbWdOSnxEranZJHFhN3BDwuMw"
  	token_secret = "rnaMfpdRLKWKM0t1ezNkFmY8wt4"

  	session = rauth.OAuth1Session(
    consumer_key = consumer_key,
    consumer_secret = consumer_secret,
    access_token = token,
    access_token_secret = token_secret)

  	request = session.get("http://api.yelp.com/v2/search",params=params)
  	#Transforms the JSON API response into a Python dictionary
  	data = request.json()
  	session.close()
  	return HttpResponse(json.dumps(data), content_type="application/json")


def index(request):
	return render(request, 'trip/index4.html')
