#This file contains all the neccessary functions to display onto the webpage concerned with the authentication of the users 
#like registering, logging in or loggin out

#This file contains all the API views to display what fields can be visible or accessible for the API's to fetch or receive


#---LIBRARIES----------------------------------------------------------------------------------------------------------------
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect

from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
from .decorators import *
from .serializers import *
from .timetable import *

import datetime



#---REGISTRATION SERIALIZERS-------------------------------------------------------------------------------------------------

#Function to access the User database for registration and store the user's data into the database
class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()



#---PROFILE SERIALIZERS------------------------------------------------------------------------------------------------------

#Function to access the Student Model to add in details for students
class StudentProfileAPIView(generics.CreateAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.all()

#Function to access the Student Model to edit the current details for students
class EditStudentProfileAPIView(generics.CreateAPIView):
    serializer_class = EditStudentProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.all()

#Function to access the Professor Model to add in details for professors
class ProfessorProfileAPIView(generics.CreateAPIView):
    serializer_class = ProfessorProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = Professor.objects.all()



#---ADMIN SERIALIZERS--------------------------------------------------------------------------------------------------------

#Function for admin to access the User Model to accept a professor into the system
class AcceptNewProfessorAPIView(generics.CreateAPIView):
    serializer_class = AcceptNewProfessorSerializer
    permission_classes = [IsAdminUser]
    queryset = Professor.objects.all()

#Function for admin to access the User Model to reject a professor entry into the system
class RejectNewProfessorAPIView(generics.CreateAPIView):
    serializer_class = RejectNewProfessorSerializer
    permission_classes = [IsAdminUser]
    queryset = Professor.objects.all()

#Function for admin to access the User Model to reject a professor entry into the system
class SetDeadlineAPIView(generics.CreateAPIView):
    serializer_class = SetDeadlineSerializer
    permission_classes = [IsAdminUser]
    queryset = Deadline.objects.all()

#Function for admin to access the User Model to reject a professor entry into the system
class AssignStudentAPIView(generics.CreateAPIView):
    serializer_class = AssignStudentSerializer
    permission_classes = [IsAdminUser]
    queryset = Accepted.objects.all()


#Function to generate a timetable
class AddVenueAPIView(generics.CreateAPIView):
    serializer_class = AddVenueSerializer
    permission_classes = [IsAdminUser]
    queryset = Venues.objects.all()

#Function to generate a timetable
class RemoveVenueAPIView(generics.CreateAPIView):
    serializer_class = RemoveVenueSerializer
    permission_classes = [IsAdminUser]
    queryset = Venues.objects.all()

#Function to generate a timetable
class EditVenueAPIView(generics.CreateAPIView):
    serializer_class = EditVenueSerializer
    permission_classes = [IsAdminUser]
    queryset = Venues.objects.all()

#Function to generate a timetable
class CreateTimetableAPIView(generics.CreateAPIView):
    serializer_class = CreateTimetableSerializer
    permission_classes = [IsAdminUser]
    queryset = Demonstration.objects.all()

#Function to generate a timetable
class DeleteDataAPIView(generics.CreateAPIView):
    serializer_class = DeleteDataSerializer
    permission_classes = [IsAdminUser]
    queryset = Accepted.objects.all()





#---STUDENT SERIALIZERS------------------------------------------------------------------------------------------------------

#Function to access the Proposal Model to add in details for students proposal form
class ProposalFormAPIView(generics.CreateAPIView):
    serializer_class = ProposalFormSerializer
    permission_classes = [IsAuthenticated]
    queryset = Proposal.objects.all()

#Function to access the Accepted Model for students to submit their proposals to the selected professor
class SubmitProposalAPIView(generics.CreateAPIView):
    serializer_class = SubmitProposalSerializer
    permission_classes = [IsAuthenticated]
    queryset = Professor.objects.all()

class SubmitSRSAPIView(generics.CreateAPIView):
    serializer_class = SubmitSRSSerializer
    permission_classes = [IsAuthenticated]
    queryset = Files.objects.all()

class SubmitDOCAPIView(generics.CreateAPIView):
    serializer_class = SubmitDOCSerializer
    permission_classes = [IsAuthenticated]
    queryset = Files.objects.all()

#Function to access the Meeting Model for students to send and create a meeting
class StudendSendMeetingAPIView(generics.CreateAPIView):
    serializer_class = StudendSendMeetingSerializer
    permission_classes = [IsAuthenticated]
    queryset = Meeting.objects.all()

#Function to access the Meeting Model for students to accept an existing meeting
class StudendAcceptMeetingAPIView(generics.CreateAPIView):
    serializer_class = StudendAcceptMeetingSerializer
    permission_classes = [IsAuthenticated]
    queryset = Meeting.objects.all()

#Function to access the Meeting Model for students to reject an existing meeting
class StudendRejectMeetingAPIView(generics.CreateAPIView):
    serializer_class = StudendRejectMeetingSerializer
    permission_classes = [IsAuthenticated]
    queryset = Meeting.objects.all()

#Function to access the Meeting Model for students to reject an existing meeting
#class MeetingFormAPIView(generics.CreateAPIView):
#    serializer_class = MeetingFormSerializer
#    permission_classes = [IsAuthenticated]
#    queryset = Meeting.objects.all()



#---PROFESSOR SERIALIZERS---------------------------------------------------------------------------------------------------

#Function to access the Accepted Model for professors to accept a student proposal
class AcceptProposalAPIView(generics.CreateAPIView):
    serializer_class = AcceptProposalSerializer
    permission_classes = [IsAuthenticated]
    queryset = Accepted.objects.all()

#Function to access the Accepted Model for professors to reject a student proposal
class RejectProposalAPIView(generics.CreateAPIView):
    serializer_class = RejectProposalSerializer
    permission_classes = [IsAuthenticated]
    queryset = Accepted.objects.all()

#Function to access the Meeting Model for professors to send and create a meeting
class SendMeetingAPIView(generics.CreateAPIView):
    serializer_class = SendMeetingSerializer
    permission_classes = [IsAuthenticated]
    queryset = Meeting.objects.all()

#Function to access the Meeting Model for professors to accept an existing meeting
class AcceptMeetingAPIView(generics.CreateAPIView):
    serializer_class = AcceptMeetingSerializer
    permission_classes = [IsAuthenticated]
    queryset = Meeting.objects.all()

#Function to access the Meeting Model for professors to reject an existing meeting
class RejectMeetingAPIView(generics.CreateAPIView):
    serializer_class = RejectMeetingSerializer
    permission_classes = [IsAuthenticated]
    queryset = Meeting.objects.all()

#Function to access the Timetable Model for professors to create a timetable slot for demonstration
class AddTimeAPIView(generics.CreateAPIView):
    serializer_class = AddTimeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Timetable.objects.all()

#Function to access the Timetable Model for professors to delete a created timetable slot
class RemoveTimeAPIView(generics.CreateAPIView):
    serializer_class = RemoveTimeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Timetable.objects.all()

#Function to access the Marking Model for professors to mark a student project
class MarkProjectAPIView(generics.CreateAPIView):
    serializer_class = MarkProjectSerializer
    permission_classes = [IsAuthenticated]
    queryset = Marking.objects.all()

#Function to send details to send the student an email of the project supervision form
class MeetingFormAPIView(generics.CreateAPIView):
    serializer_class = MeetingFormSerializer
    permission_classes = [IsAuthenticated]





#---VIEWS--------------------------------------------------------------------------------------------------------------------

#Function to return a list of all users
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        userinfo = User.objects.filter(username=user.username)
        return userinfo

class AdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        user = self.request.user
        userinfo = User.objects.filter(username=user.username)
        return userinfo

#Function to return a list of all Newly registered professors for the admin to view
class NewProfessorViewSet(viewsets.ModelViewSet):
    serializer_class = NewProfessorSerializer
    queryset = Professor.objects.all()
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Professor.objects.filter(user__user_type="New_Professor")

#Function to return the deadlines for the following fields
class DeadlineViewSet(viewsets.ModelViewSet):
    serializer_class = DeadlineSerializer
    queryset = Deadline.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        deadline = Deadline.objects.all()
        return deadline



#Function to return the user's student details
class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Student.objects.all()
        else:
            if user.user_type == "Professor":
                return Student.objects.all()
            elif user.user_type == "Student":
                student = Student.objects.filter(user=user)
                return student
            return None

#Function to return a list of all students whos proposals have not been accepted by a professor for the admin to view
class DefaultStudentViewSet(viewsets.ModelViewSet):
    serializer_class = DefaultStudentSerializer
    queryset = Student.objects.all()
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        accepted_students = Accepted.objects.all()
        students = Student.objects.all()
        a = [accepted.student for accepted in accepted_students]
        b = [s for s in students if s not in a]

        return b
#Function to return the user's professor details or list of all professors if the user is a student
class ProfessorViewSet(viewsets.ModelViewSet):
    serializer_class = ProfessorSerializer
    queryset = Professor.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Professor.objects.filter(user__user_type="Professor", user__is_superuser=False)
        else:
            if user.user_type == "Professor":
                professor = Professor.objects.filter(user=user)
                return professor
            elif user.user_type == "Student":
                return Professor.objects.filter(user__user_type="Professor", user__is_superuser=False)
            return None

#Function to return the list of professors who have not taken any student projects to supervise
class DefaultProfessorViewSet(viewsets.ModelViewSet):
    serializer_class = DefaultProfessorSerializer
    queryset = Professor.objects.all()
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        professors = Professor.objects.filter(user__user_type="Professor", user__is_superuser=False)
        links = Accepted.objects.filter(accepted=True).order_by('professor')

        a = [link.professor for link in links]
        b = [p for p in professors if p not in a]

        return b

#Function to return the list of all added Venues
class VenuesViewSet(viewsets.ModelViewSet):
    serializer_class = VenuesSerializer
    queryset = Venues.objects.all()
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        venues = Venues.objects.all()
        return venues

#Function to return the Demonstration Timetable constraints
class DemoViewSet(viewsets.ModelViewSet):
    serializer_class = DemoSerializer
    queryset = Demonstration.objects.all()
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Demonstration.objects.all()

#Function to return all Demonstration Time Slots
class DemonstrationViewSet(viewsets.ModelViewSet):
    serializer_class = DemonstrationSerializer
    queryset = DemonstrationItem.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            demo = DemonstrationItem.objects.all().order_by("date")
            return demo
        else:
            if user.user_type == "Student":
                student = Student.objects.get(user=user)
                demo = DemonstrationItem.objects.filter(student=student).order_by("date")
                return demo
            elif user.user_type == "Professor":
                professor = Professor.objects.get(user=user)
                assessors = Assessors.objects.filter(assesor=professor)
                demo = [d.demoItem for d in assessors]
                return demo
            return None

#Function to return the Venues
class VenueViewSet(viewsets.ModelViewSet):
    serializer_class = VenueSerializer
    queryset = Venues.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Venues.objects.all()




#---STUDENT VIEWS------------------------------------------------------------------------------------------------------------

#Function to return the student's proposal form details or create a new proposal form if one does not exist
class ProposalViewSet(viewsets.ModelViewSet):
    serializer_class = ProposalSerializer
    queryset = Proposal.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Proposal.objects.all()
        else:
            if user.user_type == "Student":
                student = Student.objects.get(user=user)
                accepted = Accepted.objects.filter(student=student).first()
                if accepted is None:
                    proposal = Proposal.objects.filter(student=student).first()
                    if proposal is None:
                        Proposal.objects.create(student=student, title="", staff="")
                    proposal = Proposal.objects.filter(student=student)
                    return proposal
                proposal = Proposal.objects.filter(student=student)
                return proposal
            elif user.user_type == "Professor":
                return Proposal.objects.all()
            return None
                

#Function to return the user's files
class FilesViewSet(viewsets.ModelViewSet):
    serializer_class = FilesSerializer
    queryset = Files.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Files.objects.all()
        else:
            if user.user_type == "Student":
                student = Student.objects.get(user=user)
                files = Files.objects.filter(student=student)
                return files
            elif user.user_type == "Professor":
                return Files.objects.all()
            return None

#Function to return the Accepted proposals
class AcceptedViewSet(viewsets.ModelViewSet):
    serializer_class = AcceptedSerializer
    queryset = Accepted.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Accepted.objects.filter(accepted=True).order_by("professor")
        else:
            if user.user_type == "Professor":
                professor = Professor.objects.get(user=user)
                accepted = Accepted.objects.filter(professor=professor)
                return accepted
            elif user.user_type == "Student":
                student = Student.objects.get(user=user)
                accepted = Accepted.objects.filter(student=student)
                return accepted
            return None

#Function to return the user's list of meetings
class MeetingViewSet(viewsets.ModelViewSet):
    serializer_class = MeetingSerializer
    queryset = Meeting.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Meeting.objects.all()
        else:
            if user.user_type == "Professor":
                professor = Professor.objects.get(user=user)
                meetings = Meeting.objects.filter(professor=professor).order_by('date')
                return meetings
            elif user.user_type == "Student":
                student = Student.objects.get(user=user)
                meetings = Meeting.objects.filter(student=student).order_by('date')
                return meetings
            return None

#Function to return the user's list of upcoming meetings today or in the future
class UpcomingMeetingViewSet(viewsets.ModelViewSet):
    serializer_class = UpcomingMeetingSerializer
    queryset = Meeting.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        date = datetime.date.today()
        if user.is_superuser:
            return Meeting.objects.filter(accepted=True, date__gte=date)
        else:
            if user.user_type == "Professor":
                professor = Professor.objects.get(user=user)
                meetings = Meeting.objects.filter(professor=professor, accepted=True, date__gte=date).order_by('date')
                return meetings
            elif user.user_type == "Student":
                student = Student.objects.get(user=user)
                meetings = Meeting.objects.filter(student=student, accepted=True, date__gte=date).order_by('date')
                return meetings
            return None

#Function to return a list of the professors who have not added any available time slots 
class NoTimeProfessorViewSet(viewsets.ModelViewSet):
    serializer_class = NoTimeProfessorSerializer
    queryset = Professor.objects.all()
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        professors = Professor.objects.filter(user__user_type="Professor", user__is_superuser=False)
        times = Timetable.objects.all()

        a = [time.professor for time in times]
        b = [p for p in professors if p not in a]

        return b

#Function to return a list of the professors available time slots
class TimetableViewSet(viewsets.ModelViewSet):
    serializer_class = TimetableSerializer
    queryset = Timetable.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Timetable.objects.all().order_by("professor", "date")
        else:
            if user.user_type == "Professor":
                professor = Professor.objects.get(user=user)
                timetable = Timetable.objects.filter(professor=professor)
                return timetable
            return None

#Function to return the status of all undertaken projects
class StatusViewSet(viewsets.ModelViewSet):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Status.objects.all()
        else:
            if user.user_type != "Professor":
                return None
            professor = Professor.objects.get(user=user)
            projects = Status.objects.filter(professor=professor)
            return projects

#Function to return the marked projects results
class MarkingViewSet(viewsets.ModelViewSet):
    serializer_class = MarkingSerializer
    queryset = Marking.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Marking.objects.all()
        else:
            if user.user_type != "Professor":
                return None
            professor = Professor.objects.get(user=user)
            marking = Marking.objects.filter(professor=professor)
            return marking





'''
#---UNNECESSARY--------------------------------------------------------------------------------------------------------------

#Designed for testing purposes
def welcome(request):
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return redirect('/adminhomepage')
        elif user.user_type == "Student":
            return redirect('/studenthomepage')
        elif user.user_type == "Professor":
            return redirect('/professorhomepage')
    else:
        return redirect('/login')
    return render(request, 'welcome.html')

#Function to display a user signup form and add the user to the database with the provided username and password
class UserSignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/profile')

#Function to display a template webpage
def choose_profile(request):
    return render(request, 'profile.html')

#Function to display a user login form and log in the user if the user exists in the database and correct details were provided
class UserLoginView(LoginView): 
    template_name='login.html'

#Function to log out the user and redirect them to the login page
@login_required
def logout_user(request):
    logout(request) 
    return redirect("/login")
'''