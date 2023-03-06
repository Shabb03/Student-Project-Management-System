#This file contains all the neccessary functions to display onto the webpage concerned with the admin side of the project
#what only admins can access

#---LIBRARIES----------------------------------------------------------------------------------------------------------------
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import datetime

from .models import *
from .forms import *
from .decorators import *
from .timetable import *

#Sending Email through Django
#Video Reference: https://www.youtube.com/watch?v=xNqnHmXIuzU



#---ADMIN HOMEPAGE------------------------------------------------------------------------------------------------------------

#Function to display the admin's homepage
@is_admin
def adminpage(request):
    return render(request, 'adminpage.html')



#---NEW PROFESSORS LIST------------------------------------------------------------------------------------------------------

#Function to display the list of all professors and sort by professors who have undertaken students and those who have not
@is_admin
def newprofessorlist(request):
    professors = Professor.objects.filter(user__user_type="New_Professor")
    return render(request, 'newprofessorlist.html', {'professors': professors})

@is_admin
def acceptnewprofessor(request, name):
    professor = User.objects.filter(username=name).first()
    professor.user_type = "Professor"
    professor.save()
    prof = Professor.objects.get(user=professor)
    send_mail(
            'Accepted',
            'You have been accepted into the system by the admin',
            'sidhur2ca326@gmail.com',
            [prof.email],
    )
    return redirect('/newprofessors')

@is_admin
def rejectnewprofessor(request, name):
    professor = User.objects.filter(username=name).first()
    professor.user_type = "New"
    professor.save()
    prof = Professor.objects.get(user=professor)
    send_mail(
            'Rejected',
            'You have not been accepted into the system by the admin\nYou are not a Professor',
            'sidhur2ca326@gmail.com',
            [prof.email],
    )
    prof.delete()
    return redirect('/newprofessors')



#---PROFESSORS LIST----------------------------------------------------------------------------------------------------------

#Function to display the list of all professors and sort by professors who have undertaken students and those who have not
@is_admin
def professorlist(request):
    professors = Professor.objects.all()
    links = Accepted.objects.filter(accepted=True).order_by('professor')

    a = [link.professor for link in links]
    b = [p for p in professors if p not in a]

    return render(request, 'professorlist.html', {'links': links, 'b': b})



#---PROFESSORS TIME LIST-----------------------------------------------------------------------------------------------------

#Function to display a list of all the added time slots by each professor
@is_admin
def professortimelist(request):
    times = Timetable.objects.all().order_by('professor')
    return render(request, 'professortimelist.html', {'times': times})



#---STUDENTS LIST------------------------------------------------------------------------------------------------------------

#Function to display the list of all students and sort by students who have been accepted and those who have not
@is_admin
def studentlist(request):
    students = Student.objects.all()
    accepted_students = Accepted.objects.filter(accepted=True)

    a = [accepted.student for accepted in accepted_students]
    b = [s for s in students if s not in a]

    return render(request, 'studentlist.html', {'accepted_students': accepted_students, 'b': b})



#---TIMETABLE----------------------------------------------------------------------------------------------------------------

#Function for admin to click a button and generate a timetable for demonstration scheduling
@is_admin
def demonstration(request):
    return render(request, 'demonstration.html')


#Function to take the input date from the demonstration page and call the generateTimetable function in timetable.py to create the demonstration schedule using the given start date
@is_admin
def timetable_function(request):
    if request.method == "POST":
        date = request.POST['date']
        #print("DATE: ", date, "\n\n")
        generateTimetable(date)
        return redirect('/professorhomepage')
    else:
        return redirect('/demonstration')