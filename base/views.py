from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from datetime import timedelta
from django.db.models import Max
# Create your views here.
from . models import Student, CaseProfile, GoodMoral


def NewCase(request):
    query = request.GET.get('q')
    student = None

    if query:
        try:
            student = Student.objects.get(studentID=query)
        except Student.DoesNotExist:
            student = None

    if request.method == "POST" and student:
        violation = request.POST.get('violation')
        description = request.POST.get('description')
        received_by = request.POST.get('received_by')
        reported_by = request.POST.get('reported_by')
        case_date = request.POST.get('case_date')
        case_class = request.POST.get('classified')
      
        case_profile = CaseProfile.objects.create(
            student = student,
            violation = violation, 
            description = description, 
            received_by = received_by,
            reported_by = reported_by,
            case_date = case_date,
            case_class = case_class,
        )
        case_profile.determine_sanction()
        return render( request, 'modal/SavedCaseProfile.html')
    context = {'student': student, 'query': query}
    return render(request, 'base/newCaseProfile.html', context)

    
def caseList(request):
    query = request.GET.get('q')
    student = None
    cases = CaseProfile.objects.none()  # Initialize cases with an empty queryset
    sanction = None
    community_service_hours = None
    community_service_deadline = None
    suspension_start_date = None
    suspension_end_date = None

    if query:
        try:
            student = Student.objects.get(studentID=query)
        except Student.DoesNotExist:
            student = None

    if student:
        cases = CaseProfile.objects.filter(student=student)
        sanction = student.sanction
        community_service_hours = student.community_service_hours
        community_service_deadline = student.community_service_deadline
        suspension_start_date = student.suspension_start_date
        suspension_end_date = student.suspension_end_date

    context = {
        'cases': cases,
        'sanction': sanction,
        'community_service_hours': community_service_hours,
        'community_service_deadline': community_service_deadline,
        'suspension_start_date': suspension_start_date,
        'suspension_end_date': suspension_end_date
    }
    return render(request, 'base/NewCase-list.html', context)

#GOOD MORAL
def req_goodmoral(request):

    return render(request, 'base/goodmoral_login.html')


def goodmoral(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        return redirect('goodmoral_detail', student_id=student_id)
    return render(request, 'base/goodmoralForm.html')

def goodmoral_detail(request, student_id):
    student = get_object_or_404(Student, studentID=student_id)
    case_profiles = CaseProfile.objects.filter(student=student).select_related('student')

    context = {
        'student': student,
        'case_profiles': case_profiles,
    }
    return render(request, 'base/goodmoralTable.html', context)

def GoodMoralTemplate(request):
    return render(request, 'base/good_moral_certificate.html')

#TRASANCTION REPORT
def transaction(request):
    return render(request, 'base/Transactionreport.html')

def community_service(request):
    return render(request, 'base/CommunityService.html')

#COMPLETING CRUD OPERATIONS
def deletecaserecord(request, pk):
    case = get_object_or_404(CaseProfile, pk=pk)
    if request.method == "POST":
        case.delete()
        case.determine_sanction()
        return redirect('case-list')
    
    return render(request, 'modal/deleteCaseRecord.html', {'obj': case})

def updateCase(request, pk):
    case = get_object_or_404(CaseProfile, pk=pk)
    student = case.student  # Get the associated student for the case

    if request.method == "POST":
        case.violation = request.POST.get('violation')
        case.description = request.POST.get('description')
        case.received_by = ", ".join(request.POST.getlist('received_by[]'))  # Handle multiple checkbox values
        case.reported_by = request.POST.get('reported_by')
        case.case_date = request.POST.get('case_date')
        case.save()
        case.determine_sanction()
        return redirect('case-list')  # Replace 'case-list' with the name of your case list URL pattern

    context = {
        'case': case,
        'student': student,
        'query': student.studentID  # Pass the studentID to the context to keep the search query intact
    }
    return render(request, 'base/update-case.html', context)


#MODALS
def savedcaseprofile(request):
    return render(request, 'modal/SavedCaseProfile.html')

#def deletecaserecord(request):
#    return render(request, 'modal/deleteCaseRecord.html')
