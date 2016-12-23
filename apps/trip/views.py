from django.shortcuts import render, redirect, HttpResponse
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import rauth, json
from .models import User, Trip, Comment
from django.contrib import messages

def login_check(request):
    login_messages = User.userManager.login(request.session,str(request.POST['user_name']),str(request.POST['password']))
    if login_messages[0]:
		return redirect('/')
    for message in login_messages[1]['errors']:
        messages.add_message(request,messages.ERROR,message,extra_tags='login')
    return redirect('/')

def register(request):
    register_messages = User.userManager.register_check(request.session,str(request.POST['name']),\
            str(request.POST['user_name']),str(request.POST['password']),str(request.POST['confirm']))
    if register_messages[0]:
    	return redirect('/')
    for message in register_messages[1]['errors']:
        messages.add_message(request,messages.ERROR,message,extra_tags='register')
    return redirect('/')

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

def process_save(request):
	post = dict(request.POST)
	if 'waypoints' in post:
		waypoints = post['waypoints']
	else:
		waypoints = []
	route = post['begin'][0]+'->'
	for i in range(len(waypoints)):
		route += waypoints[i]+'->'
	route += post['end'][0]
	trip = Trip.tripManager.add_trip(request.session,route)
	return redirect('/show_route/'+str(trip[1].id))

def show_route(request,trip_id):
	trip = Trip.tripManager.get(id=trip_id)
	comments = Comment.objects.filter(trip=trip)
	route = trip.route.split('->')
	start = route[0]
	waypoints = []
	for i in range(1,len(route)-1):
		waypoints.append(route[i])
	end = route[len(route)-1]
	data = {
		'start':start,
		'waypoints':waypoints,
		'end' : end,
		'comments':comments,
		'trip_id':trip.id
	}
	return render(request,'trip/show_route.html',data)

def add_comment(request, trip_id):
	comment = str(request.POST['comment'])
	data = {}
	if len(comment) != 0:
		user = User.userManager.get(id=request.session['id'])
		trip = Trip.tripManager.get(id=trip_id)
		comment = Comment.objects.create(comment=comment, user=user, trip=trip)
		data['user_name'] = comment.user.user_name
		data['created_at'] = str(comment.created_at)
		data['comment'] = comment.comment
	else:
		data['comment'] = ''
	return HttpResponse(json.dumps(data), content_type="application/json")

def add_image(request, trip_id):
	if request.method == 'POST':
		user = User.userManager.get(id=request.session['id'])
		trip = Trip.tripManager.get(id=trip_id)
		img = Image.objects.create(image=image, user=user, trip=trip)
	return redirect('/wall')

def index(request):
	data = {
		'user_name':''
	}
	if 'id' in request.session:
		user = User.userManager.get(id=request.session['id'])
		data['user_name'] = user.user_name
	return render(request, 'trip/index.html',data)

def wall(request):
	trips = Trip.tripManager.all()
	comments = Comment.objects.all()
	context = {
		'trips':trips,
		'comments':comments
	}
	return render(request, 'trip/wall.html', context)

def delete_trip(request, trip_id):
	trip = Trip.tripManager.filter(id=trip_id)
	if trip:
		trip.delete()
	return redirect('/wall')

def logout(request):
	request.session.pop('id')
	return redirect('/')
