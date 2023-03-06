#This file contains all the registered models to be displayed onto the admin page, only accessible by the super user

#---LIBRARIES----------------------------------------------------------------------------------------------------------------
from django.contrib import admin
from .models import *

#---DISPLAY REGISTERED MODELS IN THE ADMIN PAGE------------------------------------------------------------------------------
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Deadline)
admin.site.register(Proposal)
admin.site.register(Files)
admin.site.register(Accepted)
admin.site.register(Meeting)
admin.site.register(Timetable)
admin.site.register(Demonstration)
admin.site.register(Venues)
admin.site.register(DemonstrationItem)
admin.site.register(Assessors)
admin.site.register(Status)
admin.site.register(Marking)