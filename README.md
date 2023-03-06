# Student Project Management System

### Built with Django, Django-REST Framework and Node.js 

The Student Project Management System allows DCU students and project supervisors to organize their proposals, files, projects meetings, reports and deadlines within the system as opposed to working on each individual aspect separately and forgetting some important information in the midst of all the work spread out.


## FUNCTIONS:
### Administrator
* View data on all students, professors and projects
* Set deadlines
* Authorize the entry of professors into the system
* Assign students to a project supervisor
* Create a demonstration timetable
* Reset all data excluding user accounts

### Student
* Sign up and login
* Edit account details
* Submit a project proposal form
* Submit Functional Specification
* Submit Documentation
* Schedule a meeting with their project supervisor
* Accept or reject a meeting
* View their meeting history
* View upcoming meetings and demonstration timetable in homepage

### Professor
* Sign Up and Login
* View number of students undertaken in homepage
* View submitted project proposals
* Accept or reject a project proposal
* Schedule a meeting with a student
* Accept or reject a meeting
* View their meeting history
* Email a project supervision form
* View a list of projects and their status
* Mark a student project
* Add an available timetable slot for demonstration
* View their demonstration timetable


## MANUALS:
Manuals are stored inside docs/3-final-reports
Functional Specification Document is inside docs/2-functional-specification


## CHANGES:
In src/backend/backend/settings.py
Change the following
`EMAIL_HOST_USER = 'youremail@gmail.com'`
`EMAIL_HOST_PASSWORD = '****************'`


## VIDEO WALKTHROUGH:
https://drive.google.com/file/d/1KmAG5mi9KwdOuBgXWBrEVFJSaSqaZmEU/view?usp=share_link