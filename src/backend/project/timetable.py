#This file contains the functions to automatically generate a timetable for the demonstration schedule using Genetic Algorithms


#---LIBRARIES----------------------------------------------------------------------------------------------------------------
from .models import *
from datetime import *



#Function to check if there are enough appropriate time slots for every student based on the number of student, professors and
#number of assessors per demo
def checkTimeSlots(inputDate, assessor):

    timeDict = {
        1: "09:00",
        2: "10:00",
        3: "11:00",
        4: "12:00",
        5: "14:00",
        6: "15:00",
        7: "16:00",
        8: "17:00"
    }

    count = 0
    loneTimeSlots = []

    timetable = Timetable.objects.filter(date__gte=inputDate).order_by("date", "time")
    lastDate = Timetable.objects.order_by("-date", "-time").first().date

    #d = inputDate.split("-")
    #year, month, day = int(d[0]), int(d[1]), int(d[2])
    #currentDate = date(year, month, day)

    currentDate = inputDate

    while currentDate <= lastDate:
        currentTimetable = [t for t in Timetable.objects.filter(date=currentDate).order_by("time")]
        currentTimetableTime = [t.time for t in currentTimetable]
        for i in range(len(currentTimetable)):
            result = currentTimetableTime.count(currentTimetableTime[i]) // assessor
            if result == 0:
                loneTimeSlots.append(Timetable.objects.get(id=currentTimetable[i].id))
            else:
                count += result

        currentDate = currentDate + timedelta(days=1)

    students = Accepted.objects.filter(accepted=True).count()
    professors = Professor.objects.filter(user__user_type = "Professor", user__is_superuser=False).count()

    if ((students // professors) + 1) * (assessor) > count:
        leftover = students - count
        return (leftover, loneTimeSlots)
    return True



#Function to get two lists:

#1st list returns all the appropriate timetable slots for the number of assessors required, e.g 3 assessors required
#and 3 or more timetable slots match

#2nd list returns all timetable slots that are not suitable based on the number of assessors, e.g 3 assessors required
#but only two timetable slots match instead of 2

def getTimetable(inputDate, assessor):
    t1, t2 = [], []

    timetable = Timetable.objects.filter(date__gte=inputDate).order_by("date", "time")
    lastDate = Timetable.objects.order_by("-date", "-time").first().date

    #d = inputDate.split("-")
    #year, month, day = int(d[0]), int(d[1]), int(d[2])
    #currentDate = date(year, month, day)

    currentDate = inputDate

    while currentDate <= lastDate:
        currentTimetable = [t for t in Timetable.objects.filter(date=currentDate).order_by("time")]
        currentTimetableTime = [t.time for t in currentTimetable]
        for i in range(len(currentTimetable)):
            result = currentTimetableTime.count(currentTimetableTime[i])
            if result >= assessor:
                t1.append(Timetable.objects.get(id=currentTimetable[i].id))
            else:
                t2.append(Timetable.objects.get(id=currentTimetable[i].id))

        currentDate = currentDate + timedelta(days=1)
    return (t1, t2)



#Initialize the list of all students, professors and which students have which professor as their supervisor
def generateTimetable(inputDate, assessor):

    start_date = inputDate
    no_of_assessors = assessor

    timeDict = {
        1: "09:00",
        2: "10:00",
        3: "11:00",
        4: "12:00",
        5: "14:00",
        6: "15:00",
        7: "16:00",
        8: "17:00"
    }

    venues = [v for v in Venues.objects.all()]
    acceptedList = Accepted.objects.filter(accepted=True).order_by("professor")
    studentCount =  Accepted.objects.filter(accepted=True).count()
    professorList = Professor.objects.filter(user__user_type = "Professor", user__is_superuser=False)

    timeList = getTimetable(start_date, no_of_assessors)
    t1, t2 = timeList

    i = 0
    excludeStudentList = []

    t1_length = len(t1)
    while i < t1_length:
        tempList = t1[0:no_of_assessors]

        for j in range(len(tempList)):
            a = acceptedList.filter(professor=tempList[j].professor).exclude(student__in=excludeStudentList).first()
            if a:
                student = a.student

                demoItem = DemonstrationItem.objects.create(demo=Demonstration.objects.all().order_by('-id').first(),
                                                            student=student,
                                                            date=tempList[j].date,
                                                            time=tempList[j].time,
                                                            venue=Venues.objects.all().first()
                                                            )

                for t in tempList:
                    Assessors.objects.create(demoItem=demoItem, assesor=t.professor)
                    #print("assessors = ",t.professor, t.date, t.time)

                '''
                print("#---------------------------------------------------------------")
                print("demoItem:\n")
                print("demo = ", Demonstration.objects.all().order_by('-id').first())
                print("student = ", student)
                print("date = ", tempList[j].date)
                print("time = ", tempList[j].time)
                print("venue = ", Venues.objects.all().first())
                print("#---------------------------------------------------------------\n\n")
                '''

                excludeStudentList.append(student)
                studentCount -= 1
                break

        del t1[0:no_of_assessors]
        i += no_of_assessors

        if studentCount == 0:
            break