#This file contains all the database models, stored in SQLITE 3

#---LIBRARIES----------------------------------------------------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from datetime import *


#Stores the user's username, password and user_type to determine if their role is a student or a professor
class User(AbstractUser):
    user_type_data=(('New', "New"), ('Student', "Student"), ('Professor', "Professor"), ('New_Professor', "New_Professor"))
    user_type=models.CharField(default='New', choices=user_type_data, max_length=15)


#Stores the students details
class Student(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False)

    email = models.EmailField(max_length=50, blank=False)

    student_id = models.CharField(max_length=10, blank=False, unique=True)
    course = models.CharField(default="CASE", max_length=10, blank=False)
    year = models.IntegerField(default=3, blank=False)

    def student_url(self):
        return self.pk


#Stores the professors details
class Professor(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False)

    email = models.EmailField(max_length=50, blank=False)

    def professor_url(self):
        return self.pk
        

#Stores the proposal forms student user, time created and text input by the student
class Proposal(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    staff = models.CharField(max_length=50, blank=False)
    time = models.DateTimeField(auto_now=True)
	
    introduction = models.TextField(default="")
    outline = models.TextField(default="")
    background = models.TextField(default="")
    goals = models.TextField(default="")
    tools = models.TextField(default="")


##Stores the files submitted by the specific user
class Files(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    srs = models.FileField(upload_to='media/srs', blank=True, null=True)
    documentation = models.FileField(upload_to='media/docs', blank=True, null=True)


#Acts as a link between the student and professor to determine which professor has undertaken which students and records whether
#the professor has accepted a student proposal or not, also stores a message if the professor has rejected a proposal
class Accepted(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, null=True)
    accepted = models.BooleanField(default=False)
    default = models.BooleanField(default=False)
    message = models.TextField(default="No Reason Provided")


#Stores the details of a meeting whether it was sent, accepted or rejected
class Meeting(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    date = models.DateField()
    time = models.TimeField()
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    tostudent = models.BooleanField(default=False)


#Stores the necessary information of when a professor is available for project demonstration
class Timetable(models.Model):
    TIME_CHOICES = (
        ("09:00", "09:00"),
        ("10:00", "10:00"),
        ("11:00", "11:00"),
        ("12:00", "12:00"),
        ("14:00", "14:00"),
        ("15:00", "15:00"),
        ("16:00", "16:00"),
        ("17:00", "17:00"),
    )

    id = models.AutoField(primary_key=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=20, choices=TIME_CHOICES, default = '09:00')


#Stores the status of all student projects
class Status(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    files = models.ForeignKey(Files, on_delete=models.CASCADE, null=True)
    submitted = models.BooleanField(default=True)
    accepted = models.BooleanField(default=False)
    srs = models.BooleanField(default=False)
    documentation = models.BooleanField(default=False)
    mark = models.BooleanField(default=False)


#Stores the input by the admin to start generating the Demonstration Timetable
class Demonstration(models.Model):
    id = models.AutoField(primary_key=True)
    start_date = models.DateField()
    number_of_assessors = models.IntegerField(default=2)


#Stores the list of added Venues by the admin
class Venues(models.Model):
    id = models.AutoField(primary_key=True)
    demo = models.ForeignKey(Demonstration, on_delete=models.CASCADE, null=True)
    venue = models.CharField(max_length=50)
    places = models.IntegerField()


#Stores the list of created Demonstration Timetable Slots
class DemonstrationItem(models.Model):

    TIME_CHOICES = (
        ("09:00", "09:00"),
        ("10:00", "10:00"),
        ("11:00", "11:00"),
        ("12:00", "12:00"),
        ("14:00", "14:00"),
        ("15:00", "15:00"),
        ("16:00", "16:00"),
        ("17:00", "17:00"),
    )

    id = models.AutoField(primary_key=True)
    demo = models.ForeignKey(Demonstration, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=20, choices=TIME_CHOICES, default='09:00')
    venue = models.ForeignKey(Venues, on_delete=models.SET_NULL, blank=True, null=True)


#Stores the assesors for a timetable slot per Demonstration Item slot
class Assessors(models.Model):
    id = models.AutoField(primary_key=True)
    demoItem = models.ForeignKey(DemonstrationItem, on_delete=models.CASCADE)
    assesor = models.ForeignKey(Professor, on_delete=models.CASCADE)


#Stores the input given by the professor to mark a student project
class Marking(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    submitted = models.BooleanField(default=False)
    title = models.CharField(max_length=100, blank=False)

    srs_report = models.TextField(default="", blank=False)
    srs_mark = models.IntegerField(default=0)

    design_report = models.TextField(default="", blank=False)
    design_mark = models.IntegerField(default=0)
    
    implementation_report = models.TextField(default="", blank=False)
    implementation_mark = models.IntegerField(default=0)
    
    testing_report = models.TextField(default="", blank=False)
    testing_mark = models.IntegerField(default=0)
    
    documentation_report = models.TextField(default="", blank=False)
    documentation_mark = models.IntegerField(default=0)
    
    demonstration_report = models.TextField(default="", blank=False)
    demonstration_mark = models.IntegerField(default=0)

    video_report = models.TextField(default="", blank=False)
    video_mark = models.IntegerField(default=0)

    def total_marks(self):
        marks = (self.srs_mark * (10/100)) + (((self.design_mark * (20/100)) + (self.implementation_mark * (40/100)) + (self.testing_mark * (20/100)) + (self.documentation_mark * (10/100)) + (self.demonstration_mark * (5/100)) + (self.video_mark * (5/100))) * (90/100))
        marks = round(marks, 2)
        return marks


#Stores the deadlines for each aspect of the project by the admin
class Deadline(models.Model):
    id = models.AutoField(primary_key=True)
    proposal = models.DateField(null=True)
    srs = models.DateField(null=True)
    documentation = models.DateField(null=True)