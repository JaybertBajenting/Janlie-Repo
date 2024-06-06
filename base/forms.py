from django.forms import ModelForm
from . models import CaseProfile, GoodMoral

class CaseProfileForm(ModelForm):
    class Meta:
        model = CaseProfile
        fields = ['case_date','student', 'violation', 'description', 'received_by', 'reported_by']
