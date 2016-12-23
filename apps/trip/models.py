from __future__ import unicode_literals
from django.db import models
import bcrypt, re

# Create your models here.
class UserManager(models.Manager):
    def login(self,session,user_name,password):
        messages = {'errors':[]}
        if len(user_name) == 0:
            messages['errors'].append('Please enter an user name')
        if len(password) == 0:
            messages['errors'].append('Please enter a password')
        if len(messages['errors']) > 0:
            return (False, messages)
        result = self.filter(user_name=user_name)
        if len(result) == 0:
            messages['errors'].append('Incorrect user name!')
            return (False, messages)
        if not bcrypt.checkpw(str(password),str(result[0].password)):
            messages['errors'].append('Incorrect password!')
            return (False, messages)
        session['id'] = result[0].id
        return (True, messages)

    def register_check(self,session,name,user_name,password,conf_pw):
        messages = {'errors':[]}
        if len(name) < 3:
            messages['errors'].append('Name should be at least 2 characters long')
        elif not str.isalpha(name):
            messages['errors'].append('Name should be letters only')
        if len(user_name) == 0:
            messages['errors'].append('Username cannot be empty')
        elif len(self.filter(user_name=user_name)) > 0:
            messages['errors'].append('The user name you entered is used by another account')
        if len(password) < 8:
            messages['errors'].append('Password should have at least 8 characters')
        if len(conf_pw) == 0:
            messages['errors'].append('Please confirm your password')
        elif password != conf_pw:
            messages['errors'].append('Password and confirm password are not match')
        if len(messages['errors']) > 0:
            return (False, messages)
        result = self.create(name=name,user_name=user_name,password=bcrypt.hashpw(str(password),bcrypt.gensalt()))
        session['id'] = result.id
        return (True, messages)
class TripManager(models.Manager):
    def add_trip(self,session,route):
        user = User.userManager.get(id=session['id'])
        trip = self.create(route=route,user=user)
        return (True,trip)

class User(models.Model):
    name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    userManager = UserManager()

class Trip(models.Model):
    route = models.CharField(max_length=1000, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tripManager = TripManager()

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Image(models.Model):
    image = models.FileField(upload_to='documents/')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)