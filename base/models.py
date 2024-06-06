from django.db import models
from django.contrib.auth.models import User 
from datetime import timedelta, datetime
from django.utils.dateparse import parse_date
from django.db.models import Max
# Create your models here.

class Student(models.Model):
    studentID = models.IntegerField(primary_key=True)
    lrn = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100, null=True, blank=True)
    degree = models.CharField(max_length=100)
    year_level = models.PositiveIntegerField()
    sex = models.CharField(max_length=6)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)

    
    SANCTION_CHOICES = [
        ('apology_letter', 'Apology Letter'),
        ('community_service', 'Community Service'),
        ('suspension', 'Suspension'),
        ('expulsion', 'Expulsion'),
    ]
    sanction = models.CharField(max_length=50, choices=SANCTION_CHOICES, null=True, blank=True)
    apology_letter = models.FileField(upload_to='apology_letters/', null=True, blank=True)
    community_service_hours = models.IntegerField(null=True, blank=True)
    community_service_deadline = models.DateField(null=True, blank=True)
    suspension_start_date = models.DateField(null=True, blank=True)
    suspension_end_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.lastname}, {self.firstname}'

class CaseProfile(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    violation = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    received_by = models.CharField(max_length=100)
    reported_by = models.CharField(max_length=100)
    case_date = models.DateField()
    case_class = models.CharField(max_length=100)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.student.lastname

    def determine_sanction(self):
        highest_case_class = self.get_highest_case_class()

        if highest_case_class == '1':
            self.apply_sanction(1)
        elif highest_case_class == '2':
            self.apply_sanction(2)
        elif highest_case_class == '3':
            self.apply_sanction(3)

    def apply_sanction(self, highest_case_class):
        num_case_profiles = self.student.caseprofile_set.count()
        case_date = self.case_date
        if isinstance(case_date, str):
            case_date = parse_date(case_date)
        if isinstance(case_date, datetime):
            case_date = case_date.date()

        community_service_hours = 0
        community_service_deadline = None
        suspension_start_date = None
        suspension_end_date = None

        if highest_case_class == 1:
            if num_case_profiles == 1:
                self.student.sanction = "apology_letter"
                community_service_hours = 0
                community_service_deadline = case_date + timedelta(weeks=8)
            elif num_case_profiles == 2:
                self.student.sanction = "community_service"
                community_service_hours = 10
                community_service_deadline = case_date + timedelta(weeks=2)
            elif num_case_profiles == 3:
                self.student.sanction = "community_service"
                community_service_hours = 40
                community_service_deadline = case_date + timedelta(weeks=4)
            elif num_case_profiles == 4:
                self.student.sanction = "suspension"
                suspension_start_date = case_date
                suspension_end_date = case_date + timedelta(weeks=3)
            elif num_case_profiles == 5:
                self.student.sanction = "expulsion"
                
        elif highest_case_class == 2:
            if num_case_profiles == 1:
                self.student.sanction = "apology_letter"
                community_service_hours = 0
                community_service_deadline = case_date + timedelta(weeks=6)
            elif num_case_profiles == 2:
                self.student.sanction = "community_service"
                community_service_hours = 10
                community_service_deadline = case_date + timedelta(weeks=4)
            elif num_case_profiles == 3:
                self.student.sanction = "community_service"
                community_service_hours = 40
                suspension_start_date = case_date
                suspension_end_date = case_date + timedelta(weeks=3)
            elif num_case_profiles == 4:
                self.student.sanction = "suspension"
                suspension_start_date = case_date
                suspension_end_date = case_date + timedelta(weeks=3)
            elif num_case_profiles == 5:
                self.student.sanction = "expulsion"
               

        elif highest_case_class == 3:
            if num_case_profiles == 1:
                self.student.sanction = "apology_letter"
                community_service_hours = 10
                community_service_deadline = case_date + timedelta(weeks=4)
            elif num_case_profiles == 2:
                self.student.sanction = "community_service"
                community_service_hours = 20
                community_service_deadline = case_date + timedelta(weeks=8)
            elif num_case_profiles == 3:
                self.student.sanction = "suspension"
                suspension_start_date = case_date
                suspension_end_date = case_date + timedelta(weeks=26)  # 1 semester (approx. 6 months)
            elif num_case_profiles == 4:
                self.student.sanction = "suspension"
                suspension_start_date = case_date
                suspension_end_date = case_date + timedelta(weeks=52)  # 2 semesters (approx. 1 year)
            elif num_case_profiles == 5:
                self.student.sanction = "expulsion"

        # Apply deadlines and save
        self.student.community_service_hours = community_service_hours
        self.student.community_service_deadline = community_service_deadline
        self.student.suspension_start_date = suspension_start_date
        self.student.suspension_end_date = suspension_end_date
        self.student.save()

    def get_highest_case_class(self):
        case_classes = set(cp.case_class for cp in self.student.caseprofile_set.all())
        if '3' in case_classes:
            return '3'
        elif '2' in case_classes:
            return '2'
        elif '1' in case_classes:
            return '1'
        else:
            return None

class GoodMoral(models.Model):
    case_profile = models.ForeignKey(CaseProfile, on_delete=models.CASCADE)
    reason = models.TextField()
    record = models.CharField(max_length=200)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.record
    
class TransactionReport(models.Model):
    name = models.CharField(max_length=100)
    course_year_section = models.CharField(max_length=100)
    reason = models.CharField(max_length=100)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name