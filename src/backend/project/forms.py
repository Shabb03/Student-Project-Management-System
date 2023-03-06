#This file contains all forms that will be displayed on the webpage and will store all input into the database

#---LIBRARIES----------------------------------------------------------------------------------------------------------------
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, ModelChoiceField
from django.db import transaction
from .models import User, Student, Professor, Proposal, Files, Timetable, Meeting, Marking


#Form for new users to sign up
class UserSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user_type = 'Student'
        user = super().save(commit=False)
        user.is_admin = False
        user.save()
        return user


#Form for registered users to login
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))




#Form for students to fill in their details
class StudentForm(ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'placeholder': 'John Doe'}))
    email = forms.EmailField(label='DCU Email', widget=forms.EmailInput(attrs={'placeholder': 'johndoe3@mail.dcu.ie'}))
    student_id = forms.CharField(label='Student Number', widget=forms.TextInput(attrs={'placeholder': '12345678'}))

    class Meta:
        model=Student
        fields = ['name', 'email', 'student_id']


#Form for professors to fill in their details
class ProfessorForm(ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'placeholder': 'John Doe'}))
    email = forms.EmailField(label='DCU Email', widget=forms.EmailInput(attrs={'placeholder': 'johndoe@mail.dcu.ie'}))

    class Meta:
        model=Professor
        fields = ['name', 'email']


#Form for students to fill in their proposal
class ProposalForm(ModelForm):
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder': 'Shopping Webpage'}))
    staff = forms.CharField(label='Professor Name', widget=forms.TextInput(attrs={'placeholder': 'Jane Doe'}))

    class Meta:
        model=Proposal
        fields = ['title', 'staff', 'introduction', 'outline', 'background', 'goals', 'tools']


#Form for students to submit their files
class FileForm(ModelForm):
    class Meta:
        model=Files
        fields = ['srs', 'documentation']


#Form for both students and professors to create and send a meeting form
class MeetingForm(ModelForm):
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder': 'Reason for meeting'}))
    date = forms.DateField(label='Date (MM/DD/YYYY)', widget=forms.DateInput(attrs={'placeholder': '01/31/2023'}))
    time = forms.TimeField(label='Time (HH:MM)', widget=forms.TimeInput(attrs={'placeholder': '14:30'}))

    class Meta:
        model=Meeting
        fields = ['title', 'date', 'time']


#Form for professors to add in a timetable slot with any date and provided time and venue
class TimetableForm(ModelForm):
    date = forms.DateField(label='Date (MM/DD/YYYY)', widget=forms.DateInput(attrs={'placeholder': '01/31/2023'}))

    class Meta:
        model=Timetable
        fields = ['date', 'time']


#Form for the admin to add in a starting date for the demonstration schedule
class DemonstrationForm(forms.Form):
    date = forms.DateField(label='Date (MM/DD/YYYY)', widget=forms.DateInput(attrs={'placeholder': '03/01/2023'}))


#Form for professors to fill in the marking form for a students project
class MarkingForm(ModelForm):

    class Meta:
        model=Marking
        fields = ['title',
                  'srs_report', 'srs_mark',
                  'design_report', 'design_mark',
                  'implementation_report', 'implementation_mark',
                  'testing_report', 'testing_mark',
                  'documentation_report', 'documentation_mark',
                  'demonstration_report', 'demonstration_mark',
                  'video_report', 'video_mark']