#This file contains all the neccessary functions to display onto the webpage concerned with the students side of the project
#what only students can access

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



#---STUDENT PROFILE SIGN UP--------------------------------------------------------------------------------------------------

#Function to display a webpage where students can fill in a form and enter their student details
def studentsignup(request):
    user = request.user
    student = Student.objects.filter(user=user).first()
    if student:
        return redirect('/studenthomepage')
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = user
            student.save()
            return redirect('/studenthomepage')
        else:
            return render(request, 'signupstudent.html', {'form':form})
    else:
        form = StudentForm()
        return render(request, 'signupstudent.html', {'form':form})



#---STUDENT HOMEPAGE---------------------------------------------------------------------------------------------------------

#Function to display the student's homepage along with a timetable with the demonstration slot and meetings of that day
@is_student
def studentpage(request):
    user = request.user
    student = Student.objects.get(user=user)
    date = datetime.date.today()
    meetings = Meeting.objects.filter(student=student, accepted=True, date__gte=date)
    return render(request, 'studentpage.html', {'student':student, 'meetings':meetings})



#---PROPOSAL-----------------------------------------------------------------------------------------------------------------

#Function to display the student's proposal and a list of all professors
@is_student
def proposals(request):
    user = request.user
    student = Student.objects.get(user=user)
    proposal = Proposal.objects.filter(student=student).first()
    professors = Professor.objects.all()
    if proposal is None:
        Proposal.objects.create(student=student)
        proposal = Proposal.objects.filter(student=student).first()
    sent_proposal = Accepted.objects.filter(proposal=proposal).first()
    if sent_proposal is None:
        return render(request, 'proposals.html', {'proposal':proposal, 'professors':professors})
    else:
        return render(request, 'proposals.html', {'sent':True, 'sent_proposal':sent_proposal})

#PROPOSAL FORM EDITING INSTANCE VIDEO REFERENCE: https://www.youtube.com/watch?v=jCM-m_3Ysqk

#Function to display the student's proposal form with all details already input
@is_student
def individual_proposal(request, pid):
    user = request.user
    student = Student.objects.get(user=user)
    try:
        proposal = Proposal.objects.get(id=pid)
    except:
        return redirect('/proposals')
    if proposal.student != student:
        return redirect ('/proposals')
    sent_proposal = Accepted.objects.filter(proposal=proposal).first()
    if sent_proposal:
        return redirect('/studenthomepage')
    form = ProposalForm(request.POST or None, instance=proposal)
    if form.is_valid():
        form.save()
        return redirect('/proposals')
    return render(request, 'individual_proposal.html', {'proposal':proposal, 'form':form})

#Function to submit the proposal to the specified professor and send an email to the professor
@is_student
def send_proposal(request, name):
    user = request.user
    student = Student.objects.get(user=user)
    professor = Professor.objects.get(name=name)
    proposal = Proposal.objects.filter(student=student).first()
    accepted = Accepted.objects.filter(student=student).first()
    if accepted:
        return redirect('/proposals')
    Accepted.objects.create(student=student, professor=professor, proposal=proposal)
    Status.objects.create(student=student, professor=professor, proposal=proposal)

    send_mail(
        'Project Proposal',
        'You have received a Project Proposal from ' + student.name,
        'sidhur2ca326@gmail.com',
        [professor.email],
    )
    return redirect('/studenthomepage')



#---FILES--------------------------------------------------------------------------------------------------------------------

#Function to display a form where the student can submit their srs and documentation files
@is_student
def files(request):
    user = request.user
    student = Student.objects.get(user=user)
    proposal = Proposal.objects.get(student=student)
    status = Status.objects.get(student=student)
    files = Files.objects.filter().first()
    if files is None:
        if request.method == "POST":
            form = FileForm(request.POST, request.FILES)
            if form.is_valid():
                files = form.save(commit=False)
                files.student = student
                files.proposal = proposal
                files.save()
                status.srs = True
                status.documentation = True
                status.save()
                return redirect('/studenthomepage')
            else:
                return render(request, 'files.html', {'form':form})
        else:
            form = FileForm()
            return render(request, 'files.html', {'form':form})
    else:
        return render(request, 'files.html', {'sent':True})



#---MEETING------------------------------------------------------------------------------------------------------------------

#Function to display the student's accepted meetings in the future, meeting proposals and a form for students to create and
#send a meeting to their professor
@is_student
def student_meeting(request):
    user = request.user
    student = Student.objects.get(user=user)
    link = Accepted.objects.get(student=student)
    date = datetime.date.today()
    meetings = Meeting.objects.filter(student=student, tostudent=True, accepted=False, rejected=False)
    pending = Meeting.objects.filter(student=student, accepted=True, date__gte=date)
    if link is None:
        return redirect('/proposals')
    if request.method == "POST":
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.student = student
            meeting.professor = link.professor
            meeting.save()
            return redirect('/studenthomepage')
        else:
            return render(request, 'student_meeting.html', {'form':form, 'meetings':meetings, 'pending':pending})
    else:
        form = MeetingForm()
        return render(request, 'student_meeting.html', {'form':form, 'meetings':meetings, 'pending':pending})

#Function for students to accept a meeting proposal and send a confirmation email to both the student and the professor
@is_student
def student_accept_time(request, pid):
    user = request.user
    student = Student.objects.get(user=user)
    meeting = Meeting.objects.get(id=pid)
    if meeting.student != student:
        return redirect('/studentmeeting')
    meeting.accepted = True
    meeting.save()

    send_mail(
        'Meeting',
        meeting.professor.name + ' Has a meeting with ' + student.name + '\nReason: ' + meeting.title + '\nDate: ' + meeting.date + '\nTime: ' + meeting.time,
        'sidhur2ca326@gmail.com',
        [meeting.professor.email, student.email],
    )
    return redirect('/studentmeeting')

#Function for students to reject a meeting proposal and send an email to the professor
@is_student
def student_reject_time(request, pid):
    user = request.user
    student = Student.objects.get(user=user)
    meeting = Meeting.objects.get(id=pid)
    if meeting.student != student:
        return redirect('/studentmeeting')
    meeting.rejected = True
    meeting.save()
    send_mail(
        'Student Meeting Rejected',
        'Your Meeting with ' + student.name + ' has been rejected',
        'sidhur2ca326@gmail.com',
        [meeting.professor.email],
    )
    return redirect('/studentmeeting')

#Function for students to view a list of all meetings
@is_student
def student_meeting_history(request):
    user = request.user
    student = Student.objects.get(user=user)
    meetings = Meeting.objects.filter(student=student)
    if meetings:
        accepted = Meeting.objects.filter(student=student, accepted=True)
        pending = Meeting.objects.filter(student=student, accepted=False, rejected=False)
        rejected = Meeting.objects.filter(student=student, rejected=True)
        return render(request, 'student_meeting_history.html', {'accepted':accepted, 'pending':pending, 'rejected':rejected})
    else:
        return render(request, 'student_meeting_history.html', {'empty':True})