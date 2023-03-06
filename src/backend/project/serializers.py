#This file contains all the serializers to display what the user can view when fetching a GET requests and functions to do 
#Something when fetching a POST request

#---LIBRARIES----------------------------------------------------------------------------------------------------------------
from rest_framework import serializers 
from django.http import JsonResponse
from .models import * 
from .timetable import *
from django.core.mail import send_mail
import datetime



#---VIEWS--------------------------------------------------------------------------------------------------------------------

#Serialisers to display the following fields from the following models as GET requests
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'user_type']

class AdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'user_type']

class NewProfessorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Professor
        fields = ['name', 'email']

class DeadlineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Deadline
        fields = ['proposal', 'srs', 'documentation']

class NoTimeProfessorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Professor
        fields = ['name', 'email']

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'email', 'student_id', 'course', 'year']

class DefaultStudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'email', 'student_id', 'course', 'year', 'student_url']

class ProfessorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Professor
        fields = ['name', 'email', 'professor_url']

class DefaultProfessorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Professor
        fields = ['name', 'email']

class VenuesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Venues
        fields = ['id', 'venue', 'places']

class ProposalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Proposal
        fields = ['id', 'student', 'title', 'staff', 'time', 'introduction', 'outline', 'background', 'goals', 'tools']

class FilesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Files
        fields = ['id', 'student', 'proposal', 'srs', 'documentation']

class AcceptedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Accepted
        fields = ['id', 'student', 'professor', 'proposal', 'accepted']

class MeetingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Meeting
        fields = ['id', 'student', 'professor', 'title', 'date', 'time', 'accepted', 'rejected', 'tostudent']

class UpcomingMeetingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Meeting
        fields = ['id', 'student', 'professor', 'title', 'date', 'time', 'accepted', 'rejected', 'tostudent']

class TimetableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Timetable
        fields = ['id', 'professor', 'date', 'time']

class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'student', 'professor', 'proposal', 'files', 'submitted', 'accepted', 'srs', 'documentation', 'mark']

class DemoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Demonstration
        fields = ['id', 'start_date', 'number_of_assessors']

class AssessorsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Assessors
        fields = ['assesor']

class DemonstrationSerializer(serializers.HyperlinkedModelSerializer):
    assessors = AssessorsSerializer(many=True, read_only=True, source='assessors_set')
    class Meta:
        model = DemonstrationItem
        fields = ['id', 'demo', 'student', 'date', 'time', 'venue', 'assessors']

class VenueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Venues
        fields = ['venue']

class MarkingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Marking
        fields = ['student', 'professor', 'time', 'submitted', 'title', 'srs_report', 'srs_mark', 'design_report', 'design_mark', 'implementation_report', 'implementation_mark', 'testing_report', 'testing_mark', 'documentation_report', 'documentation_mark', 'demonstration_report', 'demonstration_mark', 'video_report', 'video_mark', 'total_marks']





#---Serialisers to complete a function with the provided fields given as POST requests---------------------------------------

#---REGISTER SERIALIZER------------------------------------------------------------------------------------------------------

#Serializer to register a new user given a username and password
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        passsword = validated_data['password']
        existing = User.objects.filter(username=username).first()
        if existing:
            return None
        newUser = User.objects.create_user(username=username, password=passsword)
        newUser.save()
        return newUser



#---PROFILE SERIALIZERS------------------------------------------------------------------------------------------------------

#Serializer to enter a students details into the database
class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'email', 'student_id', 'course', 'year']
    
    def create(self, validated_data):
        name = validated_data['name']
        email = validated_data['email']
        student_id = validated_data['student_id']
        course = validated_data['course']
        year = validated_data['year']
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            existing_email = Student.objects.filter(email=email).first()
            if existing_email:
                raise serializers.ValidationError({'Error': 'Email already in use'})
                return existing_email
            existing_student = Student.objects.filter(user=current_user).first()
            if existing_student is None:
                current_user.user_type = 'Student'
                current_user.save()
                student = Student.objects.create(user=current_user, name=name, email=email, student_id=student_id, course=course, year=year)
                student.save()
                return student
            raise serializers.ValidationError({'Error': 'Already a Student'})
            return existing_student
        return None

#Serializer to edit an existing students details
class EditStudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['course', 'year']
    
    def create(self, validated_data):
        course = validated_data['course']
        year = validated_data['year']
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            student = Student.objects.filter(user=current_user).first()
            student.course = course
            student.year = year
            student.save()
            return student
        return None

#Serializer to enter a professors details into the database
class ProfessorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['name', 'email']
    
    def create(self, validated_data):
        name = validated_data['name']
        email = validated_data['email']
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            existing_email = Professor.objects.filter(email=email).first()
            if existing_email:
                raise serializers.ValidationError({'Error': 'Email already in use'})
                return existing_email
            existing_professor = Professor.objects.filter(user=current_user).first()
            if existing_professor is None:
                current_user.user_type = 'New_Professor'
                current_user.save()
                professor = Professor.objects.create(user=current_user, name=name, email=email)
                professor.save()
                return professor
            raise serializers.ValidationError({'Error': 'Already a Professor'})
            return existing_professor
        return None



#---ADMIN SERIALIZERS--------------------------------------------------------------------------------------------------------

#Serializer to accept a new professor into the system and change their user type to a professor to allow them to use the system
class AcceptNewProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['email']
    
    def create(self, validated_data):
        email = validated_data['email']
        request = self.context.get('request', None)
        if request:
            professor = Professor.objects.filter(email=email).first()
            user = professor.user
            user.user_type = "Professor"
            user.save()
            send_mail(
                'Accepted',
                'You have been accepted into the system by the admin',
                'sidhur2ca326@gmail.com',
                [professor.email],
            )
            return professor
        return None 

#Serializer to reject a new professor entry to system and change their user type to new
class RejectNewProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['email']
    
    def create(self, validated_data):
        email = validated_data['email']
        request = self.context.get('request', None)
        if request:
            professor = Professor.objects.filter(email=email).first()
            user = professor.user
            user.user_type = "New"
            user.save()
            send_mail(
                'Rejected',
                'You have not been accepted into the system by the admin\nYou are not a Professor',
                'sidhur2ca326@gmail.com',
                [professor.email],
            )
            professor.delete()
            return professor
        return None 

#Serializer to set deadlines for each aspect of the project
class SetDeadlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deadline
        fields = ['proposal', 'srs', 'documentation']
    
    def create(self, validated_data):
        proposal = validated_data['proposal']
        srs = validated_data['srs']
        documentation = validated_data['documentation']
        request = self.context.get('request', None)
        if request:
            deadline = Deadline.objects.all().first()
            if deadline is None:
                deadline = Deadline.objects.create(proposal=proposal, srs=srs, documentation=documentation)
                print(deadline)
                return deadline
            
            deadline.proposal = proposal
            deadline.srs = srs
            deadline.documentation = documentation
            deadline.save()
            print(deadline)
            return deadline
        return None 

#Serializer to assign a student to a chosen professor
class AssignStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accepted
        fields = ['student', 'professor']

    def create(self, validated_data):
        student = validated_data['student']
        professor = validated_data['professor']
        request = self.context.get('request', None)
        if request:
            accepted = Accepted.objects.filter(student=student).first()
            if accepted is None:
                proposal = Proposal.objects.create(student=student)
                status = Status.objects.create(student=student, professor=professor, proposal=proposal)
                accepted = Accepted.objects.create(student=student, professor=professor, proposal=proposal, accepted=True, default=True, message="Default")
            return accepted
        return None 


#Serializer to
class AddVenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venues
        fields = ['venue', 'places']

    def create(self, validated_data):
        venue = validated_data['venue']
        places = validated_data['places']

        request = self.context.get('request', None)
        if request:
            existing_ven = Venues.objects.filter(venue=venue).first()
            if existing_ven:
                raise serializers.ValidationError({'Error': 'Venue already Added'})
                return existing_ven
            ven = Venues.objects.create(venue=venue, places=places)
            return ven
        return None

#Serializer to
class RemoveVenueSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Venues.objects.all())
    class Meta:
        model = Venues
        fields = ['id']

    def create(self, validated_data):
        v_id = validated_data['id']

        request = self.context.get('request', None)
        if request:
            ven = Venues.objects.get(id=v_id.id)
            ven.delete()
            return ven
        return None

#Serializer to
class EditVenueSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Venues.objects.all())
    class Meta:
        model = Venues
        fields = ['id', 'venue', 'places']

    def create(self, validated_data):
        v_id = validated_data['id']
        venue = validated_data['venue']
        places = validated_data['places']

        request = self.context.get('request', None)
        if request:
            ven = Venues.objects.get(id=v_id.id)
            ven.venue = venue
            ven.places = places
            ven.save()
            return ven
        return None

#Serializer to generate a timetable for the Demonstration Schedule with the given Start date and number of assessors
#from the input
class CreateTimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demonstration
        fields = ['start_date', 'number_of_assessors']

    def create(self, validated_data):
        start_date = validated_data['start_date']
        assessor = validated_data['number_of_assessors']

        request = self.context.get('request', None)
        if request:
            result = checkTimeSlots(start_date, assessor)
            if (result == True):
                demonstration = Demonstration.objects.create(start_date=start_date, number_of_assessors=assessor)
                generateTimetable(start_date, assessor)
                return ({'start_date': start_date, 'number_of_assessors': assessor})
            else:
                s, lst = result
                raise serializers.ValidationError({'Error': 'Not Enough Available Time Slots', 'Students': s, 'Timeslots': lst})
                return ({'start_date': start_date, 'number_of_assessors': assessor})
        return None

class DeleteDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accepted
        fields = ['message']

    def create(self, validated_data):
        message = validated_data['message']

        request = self.context.get('request', None)
        if request:
            if message == "I confirm to delete all data":
                Proposal.objects.all().delete()
                Files.objects.all().delete()
                Accepted.objects.all().delete()
                Meeting.objects.all().delete()
                Timetable.objects.all().delete()
                Status.objects.all().delete()
                Demonstration.objects.all().delete()
                Venues.objects.all().delete()
                DemonstrationItem.objects.all().delete()
                Assessors.objects.all().delete()
                Marking.objects.all().delete()
                return message
            raise serializers.ValidationError({'Error': 'Invalid Confirmation'})
            return message
        return None



#---STUDENT SERIALIZERS------------------------------------------------------------------------------------------------------

#Serializer to enter the proposal forms details into the database, assign it to the requested student 
#and create a new proposal form if it does not exist
class ProposalFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = ['title', 'staff', 'introduction', 'outline', 'background', 'goals', 'tools']
    
    def create(self, validated_data):
        title = validated_data['title']
        staff = validated_data['staff']
        introduction = validated_data['introduction']
        outline = validated_data['outline']
        background = validated_data['background']
        goals = validated_data['goals']
        tools = validated_data['tools']
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            if current_user.user_type != "Student":
                return None
            student = Student.objects.get(user=current_user)
            sent = Accepted.objects.filter(student=student).first()
            if sent:
                return None
            proposal = Proposal.objects.filter(student=student).first()
            if proposal is None:
                Proposal.objects.create(student=student)
                proposal = Proposal.objects.filter(student=student).first()
            if proposal.student != student:
                return None
            proposal.title = title
            proposal.staff = staff
            proposal.introduction = introduction
            proposal.outline = outline
            proposal.background = background
            proposal.goals = goals
            proposal.tools = tools
            proposal.save()
            return proposal
        return None

#Serializer to submit the student's proposal to the specified professor, create an Accepted model object, send an email to
#the professor and update the status of the students project
class SubmitProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['email']
    
    def create(self, validated_data):
        professor_email = validated_data['email']
        request = self.context.get('request', None)
        if request:
            deadline = Deadline.objects.all().first()
            currentDate = date.today()
            if deadline.proposal < currentDate:
                raise serializers.ValidationError({'Error': 'Deadline for Submitting Proposal reached'})
                return professor_email

            current_user = request.user
            if current_user.user_type != "Student":
                return None
            student = Student.objects.get(user=current_user)
            professor = Professor.objects.filter(email=professor_email).first()
            proposal = Proposal.objects.filter(student=student).first()
            sent = Accepted.objects.filter(proposal=proposal).first()
            if sent:
                return None
            accepted = Accepted.objects.create(student=student, professor=professor, proposal=proposal)
            Status.objects.create(student=student, professor=professor, proposal=proposal)
            send_mail(
                'Project Proposal',
                'You have received a Project Proposal from ' + student.name,
                'sidhur2ca326@gmail.com',
                [professor.email],
            )
            return professor
        return None

#Serializer to add the srs file submitted by the student into the media folder and update the status of the students project
class SubmitSRSSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ['srs']
    
    def create(self, validated_data):
        srs = validated_data['srs']
        request = self.context.get('request', None)
        if request:
            deadline = Deadline.objects.all().first()
            currentDate = date.today()
            if deadline.srs < currentDate:
                raise serializers.ValidationError({'Error': 'Deadline for Functional Specification reached'})
                return srs

            current_user = request.user
            if current_user.user_type != "Student":
                return None
            student = Student.objects.get(user=current_user)
            proposal = Proposal.objects.filter(student=student).first()
            status = Status.objects.filter(student=student).first()
            files = Files.objects.filter(student=student).first()
            if files is None:
                Files.objects.create(student=student, proposal=proposal, srs=srs)
                files = Files.objects.filter(student=student).first()
                status.files = files
                status.srs = True
                status.save()
                return files
            status.files = files
            status.srs = True
            status.save()
            files.srs = srs
            files.save()
            return files
        return None

#Serializer to add the documentstion file submitted by the student into the media folder and update the status of the students project
class SubmitDOCSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ['documentation']
    
    def create(self, validated_data):
        documentation = validated_data['documentation']
        request = self.context.get('request', None)
        if request:
            deadline = Deadline.objects.all().first()
            currentDate = date.today()
            if deadline.srs < currentDate:
                raise serializers.ValidationError({'Error': 'Deadline for Documentation reached'})
                return documentation

            current_user = request.user
            if current_user.user_type != "Student":
                return None
            student = Student.objects.get(user=current_user)
            proposal = Proposal.objects.filter(student=student).first()
            status = Status.objects.filter(student=student).first()
            files = Files.objects.filter(student=student).first()
            if files is None:
                Files.objects.create(student=student, proposal=proposal, documentation=documentation)
                files = Files.objects.filter(student=student).first()
                status.files = files
                status.documentation = True
                status.save()
                return files
            status.files = files
            status.documentation = True
            status.save()
            files.documentation = documentation
            files.save()
            return files
        return None

#Serializer to send a meeting proposal to the student's project supervisor with the given details
class StudendSendMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['title', 'date', 'time']
    
    def create(self, validated_data):
        title = validated_data['title']
        date = validated_data['date']
        time = validated_data['time']
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            if current_user.user_type != "Student":
                return None
            student = Student.objects.get(user=current_user)
            link = Accepted.objects.filter(student=student).first()
            if link is None:
                return None
            meeting = Meeting.objects.create(student=student, professor=link.professor, title=title, date=date, time=time)
            return meeting
        return None

#Serializer to accept a meeting proposal sent by the professor and send a confirmation email to both the student and the professor
class StudendAcceptMeetingSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Meeting.objects.all())
    class Meta:
        model = Meeting
        fields = ['id']
    
    def create(self, validated_data):
        m_id = validated_data['id']
        meeting_id = m_id.id
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            if current_user.user_type != "Student":
                return None
            student = Student.objects.get(user=current_user)
            meeting = Meeting.objects.get(id=meeting_id)
            if ((meeting.student != student) or (meeting.rejected == True) or (meeting.tostudent == False)):
                return None
            meeting.accepted = True
            meeting.save()

            date = str(meeting.date).split("-")
            time = str(meeting.time).split(":")
            meeting_date = date[2] + "/" + date[1]
            meeting_time = ":".join(time[0:2])

            send_mail(
                'Meeting',
                meeting.professor.name + ' Has a meeting with ' + student.name + '\nReason: ' + meeting.title + '\nDate: ' + meeting_date + '\nTime: ' + meeting_time,
                'sidhur2ca326@gmail.com',
                [meeting.professor.email, student.email],
            )
            return meeting
        return None 

#Serializer to reject a meeting proposal sent by the professor and send an email to the professor
class StudendRejectMeetingSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Meeting.objects.all())
    class Meta:
        model = Meeting
        fields = ['id']

    def create(self, validated_data):
        m_id = validated_data['id']
        meeting_id = m_id.id
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            if current_user.user_type != "Student":
                return None
            student = Student.objects.get(user=current_user)
            meeting = Meeting.objects.get(id=meeting_id)
            if ((meeting.student != student) or (meeting.accepted == True) or (meeting.tostudent == False)):
                return None
            meeting.rejected = True
            meeting.save()
            send_mail(
                'Meeting Rejected',
                'Your Meeting with ' + student.name + ' has been rejected',
                'sidhur2ca326@gmail.com',
                [meeting.professor.email],
            )
            return meeting
        return None



#---PROFESSOR SERIALIZERS----------------------------------------------------------------------------------------------------

#Serializer to accept a project proposal and send a confirmation email to the student as well as update the status of the project
class AcceptProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accepted
        fields = ['proposal']
    
    def create(self, validated_data):
        proposal = validated_data['proposal']
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            if current_user.user_type != "Professor":
                return None
            professor = Professor.objects.get(user=current_user)
            accepted = Accepted.objects.filter(proposal=proposal).first()
            status = Status.objects.filter(proposal=proposal).first()
            if ((accepted.professor != professor) or (accepted.accepted == True)):
                return None
            accepted.accepted = True
            accepted.save()
            status.accepted = True
            status.save()

            send_mail(
                'Proposal Accepted',
                'Your Proposal has been Accepted by ' + professor.name,
                'sidhur2ca326@gmail.com',
                [accepted.student.email],
            )
            return accepted
        return None 

#Serializer to reject a project proposal and send an email to the student as well as update the status of the project
class RejectProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accepted
        fields = ['proposal', 'message']
    
    def create(self, validated_data):
        proposal = validated_data['proposal']
        message = validated_data['message']
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            if current_user.user_type != "Professor":
                return None
            professor = Professor.objects.get(user=current_user)
            accepted = Accepted.objects.filter(proposal=proposal).first()
            if ((accepted.professor != professor) or (accepted.accepted == True)):
                return None
            accepted.message = message
            accepted.save()
            status = Status.objects.filter(proposal=proposal).first()

            send_mail(
                'Proposal Rejected',
                'Your Proposal has been Rejected\nReason:' + message,
                'sidhur2ca326@gmail.com',
                [accepted.student.email],
            )
            status.delete()
            accepted.delete()
            return accepted
        return None 

#Serializer to send a meeting proposal to the specified student with the given details
class SendMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['student', 'title', 'date', 'time']
    
    def create(self, validated_data):
        student = validated_data['student']
        title = validated_data['title']
        date = validated_data['date']
        time = validated_data['time']
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            if current_user.user_type != "Professor":
                return None
            professor = Professor.objects.get(user=current_user)
            meeting = Meeting.objects.create(student=student, professor=professor, title=title, date=date, time=time, tostudent=True)
            return meeting
        return None 

#Serializer to accept a meeting proposal sent by the student and send a confirmation email to both the student and the professor
class AcceptMeetingSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Meeting.objects.all())
    class Meta:
        model = Meeting
        fields = ['id']
    
    def create(self, validated_data):
        m_id = validated_data['id']
        meeting_id = m_id.id
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            if current_user.user_type != "Professor":
                return None
            professor = Professor.objects.get(user=current_user)
            meeting = Meeting.objects.get(id=meeting_id)
            if ((meeting.professor != professor) or (meeting.rejected == True) or (meeting.tostudent == True)):
                return None
            meeting.accepted = True
            meeting.save()

            date = str(meeting.date).split("-")
            time = str(meeting.time).split(":")
            meeting_date = date[2] + "/" + date[1]
            meeting_time = ":".join(time[0:2])

            send_mail(
                'Meeting',
                professor.name + ' Has a meeting with ' + meeting.student.name + '\nReason: ' + meeting.title + '\nDate: ' + meeting_date + '\nTime: ' + meeting_time,
                'sidhur2ca326@gmail.com',
                [professor.email, meeting.student.email],
            )
            return meeting
        return None 

#Serializer to reject a meeting proposal sent by the student and send an email to the student
class RejectMeetingSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Meeting.objects.all())
    class Meta:
        model = Meeting
        fields = ['id']
    
    def create(self, validated_data):
        m_id = validated_data['id']
        meeting_id = m_id.id
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            if current_user.user_type != "Professor":
                return None
            professor = Professor.objects.get(user=current_user)
            meeting = Meeting.objects.get(id=meeting_id)
            if ((meeting.professor != professor) or (meeting.accepted == True) or (meeting.tostudent == True)):
                return None
            meeting.rejected = True
            meeting.save()
            send_mail(
                'Meeting Rejected',
                'Your Meeting with ' + professor.name + ' has been rejected',
                'sidhur2ca326@gmail.com',
                [meeting.student.email],
            )
            return meeting
        return None 

#Serializer to add a timetable slot for demonstration with the provided details
class AddTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = ['date', 'time']
    
    def create(self, validated_data):
        date = validated_data['date']
        time = validated_data['time']
        request = self.context.get('request', None)
        if request:

            timedict = {
                "09:00": 1,
                "10:00": 2,
                "11:00": 3,
                "12:00": 4,
                "14:00": 5,
                "15:00": 6,
                "16:00": 7,
                "17:00": 8
            }

            current_user = request.user
            if current_user.user_type != "Professor":
                return None
            professor = Professor.objects.get(user=current_user)
            times = Timetable.objects.filter(professor=professor, date=date)
            if times:
                for t in times:
                    if ((t.time == time)):
                        raise serializers.ValidationError({'Error': 'Time Already Added'})
                        return times
                    if ((timedict[t.time] + 1 == timedict[time]) or (timedict[t.time] - 1 == timedict[time])):
                        raise serializers.ValidationError({'Error': 'Must Have A 1 Hour Gap Between Times'})
                        return times
            timetable = Timetable.objects.create(professor=professor, date=date, time=time)
            return timetable
        return None 

#Serializer to remove an added timetable slot
class RemoveTimeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Timetable.objects.all())
    class Meta:
        model = Timetable
        fields = ['id']
    
    def create(self, validated_data):
        t_id = validated_data['id']
        timetable_id = t_id.id
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            if current_user.user_type != "Professor":
                return None
            professor = Professor.objects.get(user=current_user)
            timetable = Timetable.objects.get(id=timetable_id)
            if timetable.professor != professor:
                return None
            timetable.delete()
            return timetable
        return None 

#Serializer to enter the marking forms details into the database for the specified student, update the status of the project and
#send an email to the student
class MarkProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marking
        fields = ['student', 'title',
                  'srs_report', 'srs_mark',
                  'design_report', 'design_mark',
                  'implementation_report', 'implementation_mark', 
                  'testing_report', 'testing_mark', 
                  'documentation_report', 'documentation_mark', 
                  'demonstration_report', 'demonstration_mark', 
                  'video_report', 'video_mark']
    
    def create(self, validated_data):
        student = validated_data['student']
        title = validated_data['title']

        srs_report = validated_data['srs_report']
        srs_mark = validated_data['srs_mark']
        design_report = validated_data['design_report']
        design_mark = validated_data['design_mark']
        implementation_report = validated_data['implementation_report']
        implementation_mark = validated_data['implementation_mark']
        testing_report = validated_data['testing_report']
        testing_mark = validated_data['testing_mark']
        documentation_report = validated_data['documentation_report']
        documentation_mark = validated_data['documentation_mark']
        demonstration_report = validated_data['demonstration_report']
        demonstration_mark = validated_data['demonstration_mark']
        video_report = validated_data['video_report']
        video_mark = validated_data['video_mark']

        request = self.context.get('request', None)
        if request:
            current_user = request.user
            if current_user.user_type != "Professor":
                return None
            professor = Professor.objects.get(user=current_user)
            status = Status.objects.filter(student=student).first()
            if status.professor != professor:
                return None
            status.mark = True
            status.save()
            print(status)
            marked = Marking.objects.create(student=student, professor=professor, submitted=True, title=title,
                                            srs_report=srs_report, srs_mark=srs_mark,
                                            design_report=design_report, design_mark=design_mark,
                                            implementation_report=implementation_report, implementation_mark=implementation_mark,
                                            testing_report=testing_report, testing_mark=testing_mark,
                                            documentation_report=documentation_report, documentation_mark=documentation_mark,
                                            demonstration_report=demonstration_report, demonstration_mark=demonstration_mark,
                                            video_report=video_report, video_mark=video_mark
            )
            marked = Marking.objects.filter(student=student)
            print(marked, "\n\n")
            print(video_mark, "\n\n")
            print(marked.video_mark, "\n\n")
            #total = (srs_mark * (10/100)) + (((design_mark * (20/100)) + (implementation_mark * (40/100)) + (testing_mark * (20/100)) + (documentation_mark * (10/100)) + (demonstration_mark * (5/100)) + (video_mark * (5/100))) * (90/100))
            #total = (round(total, 2))
            return marked
        return None 

#class to store the contents of the MeetingFormSerializer
class MeetingForm(object):
    def __init__(self, email, students, comments, progress):
        self.email = email
        self.students = students
        self.comments = comments
        self.progress = progress

#Serializer to send the student email with the project supervision form details
class MeetingFormSerializer(serializers.Serializer):
    email = serializers.EmailField()
    students = serializers.CharField(max_length=100)
    comments = serializers.CharField(max_length=500)
    progress = serializers.CharField(max_length=50)
    def create(self, validated_data):
        email = validated_data['email']
        students = validated_data['students']
        comments = validated_data['comments']
        progress = validated_data['progress']

        send_mail(
            'Project Dashboard Activity:',
            '\nStudent(s): ' + students + '\n\n\nProgress and Comments:\n' + comments + '\n\n\nProgress: ' + progress,
            'sidhur2ca326@gmail.com',
            [email],
        )

        return MeetingForm(**validated_data)