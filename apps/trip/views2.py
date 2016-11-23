from django.shortcuts import render, redirect
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import rauth
import time

# def main():
# 	locations = [(39.98,-82.98),(42.24,-83.61),(41.33,-89.13)]
# 	api_calls = []
# 	for lat,long in locations:
# 		params = get_search_parameters(lat,long)
# 		api_calls.append(get_results(params))
# 		#Be a good internet citizen and rate-limit yourself
# 		time.sleep(1.0)


def get_results(request):
    
  	session = rauth.OAuth1Session(
	    consumer_key='szjwl0hfTZEnIZ0YMR3K7g',
	    consumer_secret='OjSOA4XoTyzr5VG_lDwu1L2vbkE',
	    access_token='NE6ro_inbWdOSnxEranZJHFhN3BDwuMw',
	    access_token_secret='rnaMfpdRLKWKM0t1ezNkFmY8wt4'
  	)

  	params = {}
	params["term"] = "restaurant"
	params["location"] = "San Francisco"
	params["radius_filter"] = "2000"
	params["limit"] = "10"

 	request = session.get("http://api.yelp.com/v2/search",params=params)
   
  	#Transforms the JSON API response into a Python dictionary
  	data = request.json()
  	session.close()
   
  	return data

# def get_search_parameters(lat,long):
# 	#See the Yelp API for more details
# 	params = {}
# 	params["term"] = "restaurant"
# 	params["ll"] = "{},{}".format(str(lat),str(long))
# 	params["radius_filter"] = "2000"
# 	params["limit"] = "10"

# 	return params

# if __name__=="__main__":
# 	main()

def index(request):
	return render(request, 'trip/index4.html')

