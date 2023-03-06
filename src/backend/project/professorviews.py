#This file contains all the neccessary functions to display onto the webpage concerned with the professors side of the project
#what only professors can access

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

#Sending Email through Django
#Video Reference: https://www.youtube.com/watch?v=xNqnHmXIuzU



#---PROFFESOR PROFILE SIGN UP------------------------------------------------------------------------------------------------

#Function to display a webpage where professors can fill in a form and enter their professor details
def professorsignup(request):
    user = request.user
    professor = Professor.objects.filter(user=user).first()
    if professor:
        return redirect('/professorhomepage')
    if request.method == "POST":

        form = ProfessorForm(request.POST)
        if form.is_valid():
            professor = form.save(commit=False)
            professor.user = user
            user.user_type = "New_Professor"
            user.save()
            professor.save()
            return redirect('/professorhomepage')
        else:
            return render(request, 'signupprofessor.html', {'form':form})
    else:
        form = ProfessorForm()
        return render(request, 'signupprofessor.html', {'form':form})



#---PROFESSOR HOMEPAGE-------------------------------------------------------------------------------------------------------

#Function to display the professors's homepage
@is_professor
def professorpage(request):
    user = request.user
    professor = Professor.objects.get(user=user)
    return render(request, 'professorpage.html', {'professor':professor})



#---PROPOSAL-----------------------------------------------------------------------------------------------------------------

#Function to display a list of submitted student proposals
@is_professor
def proposalslist(request):
    user = request.user
    professor = Professor.objects.get(user=user)
    proposals = Accepted.objects.filter(professor=professor, accepted=False)
    if proposals:
        return render(request, 'proposalslist.html', {'proposals':proposals})
    else:
        return render(request, 'proposalslist.html', {'empty':True})

#Function to display the selected students proposal form
@is_professor
def individual_proposalslist(request, pid):
    user = request.user
    proposal = Proposal.objects.get(id=pid)
    return render(request, 'individual_proposalslist.html', {'proposal':proposal})

#Function to accept a student proposal, assign them as an undertaken project, update the status of the project
#and send the student a confirmation email
@is_professor
def accept_proposal(request, pid):
    user = request.user
    proposal = Proposal.objects.get(id=pid)
    professor = Professor.objects.get(user=user)
    accepted_proposal = Accepted.objects.get(proposal=pid)
    status = Status.objects.get(proposal=pid)
    
    send_mail(
            'Proposal Accepted',
            'Your Proposal has been Accepted by ' + professor.name,
            'sidhur2ca326@gmail.com',
            [proposal.student.email],
    )

    accepted_proposal.accepted = True
    accepted_proposal.save()
    status.accepted = True
    status.save()
    return redirect('/proposalslist')

#Function to reject a student proposal and send the student an email
@is_professor
def reject_proposal(request, pid):
    proposal = Proposal.objects.get(id=pid)
    rejected_proposal = Accepted.objects.get(proposal=pid)
    status = Status.objects.get(proposal=pid)
    rejected_proposal.delete()
    status.delete()
    if request.method == "POST":
        message = request.POST['message']
        send_mail(
            'Proposal Rejected',
            'Your Proposal has been Rejected\nReason:' + message,
            'sidhur2ca326@gmail.com',
            [proposal.student.email],
        )
        return redirect('/proposalslist')
    else:
        return redirect('/proposalslist/' + pid)



#---MEETING------------------------------------------------------------------------------------------------------------------

#Function to choose which undertaken to create and send a meeting to, display the professors's accepted meetings in the future
#and meeting proposals from students
@is_professor
def choose_student(request):
    user = request.user
    professor = Professor.objects.get(user=user)
    students = Accepted.objects.filter(professor=professor)
    meetings = Meeting.objects.filter(professor=professor, tostudent=False, accepted=False, rejected=False)
    date = datetime.date.today()
    pending = Meeting.objects.filter(professor=professor, accepted=True, date__gte=date)
    return render(request, 'choose_students.html', {'students':students, 'meetings':meetings, 'pending':pending})

#Function to create and send a meeting to the specified student
@is_professor
def meeting(request, pid):
    user = request.user
    professor = Professor.objects.get(user=user)
    link = Accepted.objects.get(id=pid)
    if request.method == "POST":
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.student = link.student
            meeting.professor = professor
            meeting.tostudent = True
            meeting.save()
            return redirect('/professorhomepage')
        else:
            return render(request, 'meeting.html', {'form':form, 'pid':pid})
    else:
        form = MeetingForm()
        return render(request, 'meeting.html', {'form':form, 'pid':pid})

#Function for professors to accept a meeting proposal and send a confirmation email to both the student and the professor
@is_professor
def accept_time(request, pid):
    user = request.user
    professor = Professor.objects.get(user=user)
    meeting = Meeting.objects.get(id=pid)
    if meeting.professor != professor:
        return redirect('/meetstudent')
    meeting.accepted = True
    meeting.save()
    
    send_mail(
        'Meeting',
        professor.name + ' Has a meeting with ' + meeting.student.name + '\nReason: ' + meeting.title + '\nDate: ' + meeting.date + '\nTime: ' + meeting.time,
        'sidhur2ca326@gmail.com',
        [professor.email, meeting.student.email],
    )
    return redirect('/meetstudent')

#Function for professors to reject a meeting proposal and send an email to the student
@is_professor
def reject_time(request, pid):
    user = request.user
    professor = Professor.objects.get(user=user)
    meeting = Meeting.objects.get(id=pid)
    if meeting.professor != professor:
        return redirect('/meetstudent')
    meeting.rejected = True
    meeting.save()

    send_mail(
        'Student Meeting Rejected',
        'Your Meeting with ' + professor.name + ' has been rejected',
        'sidhur2ca326@gmail.com',
        [meeting.student.email],
    )
    return redirect('/meetstudent')

#Function for professors to view a list of all meetings
@is_professor
def meeting_history(request):
    user = request.user
    professor = Professor.objects.get(user=user)
    meetings = Meeting.objects.filter(professor=professor)
    if meetings:
        accepted = Meeting.objects.filter(professor=professor, accepted=True)
        pending = Meeting.objects.filter(professor=professor, accepted=False, rejected=False)
        rejected = Meeting.objects.filter(professor=professor, rejected=True)
        return render(request, 'meeting_history.html', {'accepted':accepted, 'pending':pending, 'rejected':rejected})
    else:
        return render(request, 'meeting_history.html', {'empty':True})



#---TIMETABLE----------------------------------------------------------------------------------------------------------------

#Function for professors to view their added timetable slots and display a form to add a new available timetable slot
@is_professor
def add_timetable(request):
    user = request.user
    professor = Professor.objects.get(user=user)
    times = Timetable.objects.filter(professor=professor, accepted=False)
    empty = True
    if times:
        empty = False
    if request.method == "POST":
        form = TimetableForm(request.POST)
        if form.is_valid():
            timetable = form.save(commit=False)
            timetable.professor = professor
            timetable.save()
            return redirect('/addtimetable')
        else:
            return render(request, 'add_timetable.html', {'form':form, 'empty':empty, 'times':times})
    else:
        form = TimetableForm()
        return render(request, 'add_timetable.html', {'form':form, 'empty':empty, 'times':times})

#Function for professors to remove an added timetable slot
@is_professor
def remove_time(request, pid):
    user = request.user
    professor = Professor.objects.get(user=user)
    timetable = Timetable.objects.get(id=pid)
    if timetable.professor != professor:
        return redirect('/addtimetable')
    timetable.delete()
    return redirect('/addtimetable')



#---PROJECTS-----------------------------------------------------------------------------------------------------------------

#SEARCH BAR VIDEO REFERENCE: https://www.youtube.com/watch?v=AGtae4L5BbI&list=PLCC34OHNcOtqW9BJmgQPPzUpJ8hl49AGy

#Function for professors to view a list of all undertaken projects and their current status
@is_professor
def projects(request):
    user = request.user
    professor = Professor.objects.get(user=user)
    projects = Status.objects.filter(professor=professor)
    return render(request, 'projects.html', {'projects':projects})

#Function for professors to view a list of all undertaken projects with titles similar to the search quer
#and their current status
@is_professor
def search_projects(request):
    if request.method == "POST":
        user = request.user
        professor = Professor.objects.get(user=user)
        query = request.POST['query']
        projects = Status.objects.filter(professor=professor, proposal__title__contains=query)
        return render(request, 'search_projects.html', {'projects':projects, 'query':query})
    else:
        return render(request, 'search_projects.html')

#Function for professors to view a a detailed description of an undertaken project
@is_professor
def individual_project(request, pid):
    user = request.user
    professor = Professor.objects.get(user=user)
    proposal = Proposal.objects.get(id=pid)
    files = Files.objects.get(student=proposal.student)
    #demonstration = Demonstration.objects.get(student=proposal.student)
    #if demonstration.professor != professor:
    #    return redirect('/projects')
    marked = Marking.objects.filter(student=proposal.student).first()
    if marked is None:
        return render(request, 'individual_project.html', {'proposal':proposal, 'files':files})
    else:
        return render(request, 'individual_project.html', {'proposal':proposal, 'files':files, 'marked':marked, 'mark':True})



#---MARKS--------------------------------------------------------------------------------------------------------------------

#Function for professors to display a marking form to mark a student project and send an email to the student
@is_professor
def mark_project(request, pid):
    user = request.user
    professor = Professor.objects.get(user=user)
    proposal = Proposal.objects.get(id=pid)
    accepted = Accepted.object.get(proposal=proposal)
    if accepted.professor != professor:
        return redirect('/projects')
    if request.method == "POST":
        form = MarkingForm(request.POST)
        if form.is_valid():
            marked = form.save(commit=False)
            marked.student = proposal.student
            marked.professor = professor
            marked.submitted = True
            marked.save()
            status = Status.objects.get(proposal=proposal)
            status.mark = True
            status.save()

            mark = Marking.objects.get(student=proposal.student)
            total = mark.total_marks

            total = (mark.srs_mark * (10/100)) + (((mark.design_mark * (5/100)) + (mark.implementation_mark * (2.5/100)) + (mark.testing_mark * (5/100)) + (mark.documentation_mark * (10/100)) + (mark.demonstration_mark * (20/100)) + (mark.video_mark * (20/100))) * (90/100))
            total = (round(total, 2))
            return redirect('/projects')
        else:
            return render(request, 'mark_project.html', {'proposal':proposal, 'form':form, 'pid':pid})
    else:
        form = MarkingForm()
        return render(request, 'mark_project.html', {'proposal':proposal, 'form':form, 'pid':pid})