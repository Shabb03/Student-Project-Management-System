#This file contains all the decorators, similar to @login_required, to ensure the user is of the specified type, otherwise
#do not let that user access that webpage/function

#Video Reference: https://www.youtube.com/watch?v=eBsc65jTKvw

#---LIBRARIES----------------------------------------------------------------------------------------------------------------
from django.http import HttpResponse
from django.shortcuts import redirect


#Decorator function to check if the user is not logged in, otherwise redirect the user elsewhere
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if user.user_type == 'Student':
                return redirect('/studenthomepage')
            elif user.user_type == 'Professor':
                return redirect('/professorhomepage')
        return view_func(request, *args, **kwargs)
    return wrapper_func


def is_admin(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            pass
        else:
            return redirect('/welcome')
        return view_func(request, *args, **kwargs)
    return wrapper_func


#Decorator function to check if the user's type is Student, otherwise redirect the user elsewhere
def is_student(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if user.user_type == 'Professor':
                return redirect('/professorhomepage')
        else:
            return redirect('/login')
        return view_func(request, *args, **kwargs)
    return wrapper_func


#Decorator function to check if the user's type is Professor, otherwise redirect the user elsewhere
def is_professor(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if user.user_type == 'Student':
                return redirect('/studenthomepage')
        else:
            return redirect('/login')
        return view_func(request, *args, **kwargs)
    return wrapper_func