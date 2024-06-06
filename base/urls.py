from django.urls import path
from . import views

urlpatterns = [
    #path('', views.caseProfile, name="case-profile"),
    path('', views.NewCase, name="NewCase"),
    path('CaseList/', views.caseList, name="case-list"),
    #path('case-list/', views.caseList, name="case-list"),

    #GOOD MORAL URL
    path('RequestGoodMoral/', views.req_goodmoral, name="req_goodmoral"),
   path('GoodMoral/<int:student_id>/', views.goodmoral, name="goodmoral"),
    path('GoodMoralTemplate/',views.GoodMoralTemplate, name="GoodMoralTemplate"),

    path('Transaction/', views.transaction, name="transaction"),
    path('CommunityServiceTracker/', views.community_service, name="community_service"),

    path('update-case/<str:pk>/', views.updateCase, name='update-case'),
    
    path('goodmoralTable',views.goodmoral,name="goodmoral"),



    path('goodmoral/', views.goodmoral, name='goodmoral'),
    path('goodmoral/<int:student_id>/', views.goodmoral_detail, name='goodmoral_detail'),

    

    #modal part
    path('SavedSuccesfully/', views.savedcaseprofile, name="savedcaseprofile"),
    path('DeleteCaseRecord/<str:pk>/', views.deletecaserecord, name="deletecaserecord"),
]