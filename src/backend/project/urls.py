#This file contains all the url paths provided by the views.py, studentviews.py and professorviews.py files
#This file contains all the API paths provided by the routers and url paths from views.py

#---LIBRARIES----------------------------------------------------------------------------------------------------------------
from django.urls import path, include
from . import views, adminviews, studentviews, professorviews, forms
from django.urls import path, include 
from rest_framework import routers



#---ROUTERS-FOR-API'S--------------------------------------------------------------------------------------------------------
router = routers.DefaultRouter() 
router.register(r'users', views.UserViewSet)
router.register(r'admincheck', views.AdminViewSet)
router.register(r'deadline', views.DeadlineViewSet)
router.register(r'd_students', views.DefaultStudentViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'newprofessors', views.NewProfessorViewSet)
router.register(r'time_professors', views.NoTimeProfessorViewSet)
router.register(r'd_professors', views.DefaultProfessorViewSet)
router.register(r'professors', views.ProfessorViewSet)
router.register(r'venues', views.VenuesViewSet)
router.register(r'demo', views.DemoViewSet)
router.register(r'demonstration', views.DemonstrationViewSet)
router.register(r'venue', views.VenueViewSet)
router.register(r'proposals', views.ProposalViewSet)
router.register(r'files', views.FilesViewSet)
router.register(r'accepted', views.AcceptedViewSet)
router.register(r'meetings', views.MeetingViewSet)
router.register(r'upmeetings', views.UpcomingMeetingViewSet)
router.register(r'timetable', views.TimetableViewSet)
router.register(r'status', views.StatusViewSet)
router.register(r'marking', views.MarkingViewSet)



urlpatterns = [
    #---API's----------------------------------------------------------------------------------------------------------------
    path('api/', include(router.urls)),
    path('apiregister/', views.UserRegistrationAPIView.as_view(), name="api_register"),

    path('apistudent/', views.StudentProfileAPIView.as_view(), name="StudentProfile"),
    path('apieditstudent/', views.EditStudentProfileAPIView.as_view(), name="EditStudentProfile"),
    path('apiprofessor/', views.ProfessorProfileAPIView.as_view(), name="ProfessorProfile"),

    path('apiacceptnewprofessor/', views.AcceptNewProfessorAPIView.as_view(), name="AcceptNewProfesspr"),
    path('apirejectnewprofessor/', views.RejectNewProfessorAPIView.as_view(), name="RejectNewProfessor"),
    path('apisetdeadline/', views.SetDeadlineAPIView.as_view(), name="SetDeadline"),
    path('apiassignstudent/', views.AssignStudentAPIView.as_view(), name="AssignStudent"),
    path('apiaddvenue/', views.AddVenueAPIView.as_view(), name="AddVenue"),
    path('apiremovevenue/', views.RemoveVenueAPIView.as_view(), name="RemoveVenue"),
    path('apieditvenue/', views.EditVenueAPIView.as_view(), name="EditVenue"),
    path('apicreatetimetable/', views.CreateTimetableAPIView.as_view(), name="CreateTimetable"), 
    path('deletedata/', views.DeleteDataAPIView.as_view(), name="DeleteData"),  

    path('apiproposal/', views.ProposalFormAPIView.as_view(), name="Proposal"),
    path('apisubmitproposal/', views.SubmitProposalAPIView.as_view(), name="SubmitProposal"),
    path('apisubmitsrs/', views.SubmitSRSAPIView.as_view(), name="SubmitSRS"),
    path('apisubmitdoc/', views.SubmitDOCAPIView.as_view(), name="SubmitDOC"),
    path('apistudentsendmeeting/', views.StudendSendMeetingAPIView.as_view(), name="StudentSendMeeting"),
    path('apistudentacceptmeeting/', views.StudendAcceptMeetingAPIView.as_view(), name="StudentAcceptMeeting"),
    path('apistudentrejectmeeting/', views.StudendRejectMeetingAPIView.as_view(), name="StudentRejectMeeting"),

    path('apiacceptproposal/', views.AcceptProposalAPIView.as_view(), name="AcceptProposal"),
    path('apirejectproposal/', views.RejectProposalAPIView.as_view(), name="RejectProposal"),
    path('apisendmeeting/', views.SendMeetingAPIView.as_view(), name="SendMeeting"),
    path('apiacceptmeeting/', views.AcceptMeetingAPIView.as_view(), name="AcceptMeeting"),
    path('apirejectmeeting/', views.RejectMeetingAPIView.as_view(), name="RejectMeeting"),
    path('apimeetingform/', views.MeetingFormAPIView.as_view(), name="MeetingForm"),
    path('apiaddtime/', views.AddTimeAPIView.as_view(), name="AcceptTime"),
    path('apiremovetime/', views.RemoveTimeAPIView.as_view(), name="RemoveTime"),
    path('apimark/', views.MarkProjectAPIView.as_view(), name="MarkProject"),
]





'''
    #---AUTHENTICATION VIEWS-------------------------------------------------------------------------------------------------
    path('', views.welcome, name="Welcome"),
    path('signup/', views.UserSignupView.as_view(), name="Sign Up"),
    path('profile/', views.choose_profile, name="Choose User Type"),
    path('login/',views.LoginView.as_view(template_name="login.html", authentication_form=forms.UserLoginForm)), 
    path('logout/', views.logout_user, name="Log Out"),


    #---ADMIN VIEWS----------------------------------------------------------------------------------------------------------
    path('adminhomepage/', adminviews.adminpage, name="Admin Homepage"),
    path('newprofessors/', adminviews.newprofessorlist, name="New Professors"),
    path('acceptnewprofessor/<str:name>', adminviews.acceptnewprofessor, name="Accept Professor"),
    path('rejectnewprofessor/<str:name>', adminviews.rejectnewprofessor, name="Reject Professor"),
    path('professorlist/', adminviews.professorlist, name=""),
    path('professortimelist/', adminviews.professortimelist, name=""),
    path('studentlist/', adminviews.studentlist, name=""),
    path('demonstration/', adminviews.demonstration, name=""),
    path('createtimetable/', adminviews.timetable_function, name="Generating-Timetable"),
    #path('/', adminviews., name=""),


    #---STUDENT VIEWS--------------------------------------------------------------------------------------------------------
    path('signupstudent/', studentviews.studentsignup, name="Student Profile"),

    path('studenthomepage/', studentviews.studentpage, name="Student Homepage"),

    path('proposals/', studentviews.proposals, name="Proposals"),
    path('proposals/<int:pid>', studentviews.individual_proposal, name="Proposal"),
    path('sendproposal/<str:name>', studentviews.send_proposal, name="Send Proposal"),

    path('files/', studentviews.files, name="Files"),

    path('studentmeeting/', studentviews.student_meeting, name="Supervision Meeting"),
    path('studentaccepttime/<int:pid>', studentviews.student_accept_time, name="Student Accept Time"),
    path('studentrejecttime/<int:pid>', studentviews.student_reject_time, name="Student Reject Time"),
    path('studentmeetinghistory/', studentviews.student_meeting_history, name="Supervision Meeting History"),


    #---PROFESSOR VIEWS------------------------------------------------------------------------------------------------------
    path('signupprofessor/', professorviews.professorsignup, name="Professor Profile"),

    path('professorhomepage/', professorviews.professorpage, name="Professor Homepage"),

    path('proposalslist/', professorviews.proposalslist, name="List of Proposals"),
    path('proposalslist/<int:pid>', professorviews.individual_proposalslist, name="Student Proposal"),
    path('acceptproposal/<int:pid>', professorviews.accept_proposal, name="Accept Proposal"),
    path('rejectproposal/<int:pid>', professorviews.reject_proposal, name="Reject Proposal"),

    path('meetstudent/', professorviews.choose_student, name="Choose Student"),
    path('meeting/<int:pid>', professorviews.meeting, name="Supervision Meeting"),
    path('accepttime/<int:pid>', professorviews.accept_time, name="Accept Time"),
    path('rejecttime/<int:pid>', professorviews.reject_time, name="Reject Time"),
    path('meetinghistory/', professorviews.meeting_history, name="Supervision Meeting History"),

    path('addtimetable/', professorviews.add_timetable, name="Add to Timetable"),
    path('removetime/<int:pid>', professorviews.remove_time, name="Remove Time"),

    path('projects/', professorviews.projects, name="Projects status"),
    path('searchprojects/', professorviews.search_projects, name="Search-Projects"),
    path('projects/<int:pid>', professorviews.individual_project, name="Student Project"),

    path('projectmark/<int:pid>', professorviews.mark_project, name="Mark Project"),
]
'''