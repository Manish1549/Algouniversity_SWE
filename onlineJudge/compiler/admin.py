from django.contrib import admin

# Register your models here.
from .models import Problem, Testcases, Codesubmission

admin.site.register(Problem)
admin.site.register(Testcases)
admin.site.register(Codesubmission)