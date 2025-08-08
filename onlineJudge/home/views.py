from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from compiler.models import Problem,Codesubmission

def homepage(request):
    
    submissions = Codesubmission.objects.select_related('user','problem').order_by('-timestamp')[:3]
    context = {"userCount":User.objects.count(),
               "problemCount":Problem.objects.count(),
               "submissionCount":Codesubmission.objects.count(),
               "submissions":submissions}

    return render(request,'home.html',context)
