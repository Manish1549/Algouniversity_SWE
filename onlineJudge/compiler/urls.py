from django.urls import path, include
from compiler.views import submit,problem_list

urlpatterns = [
    path('problems/',problem_list,name='problems'),
    path('problems/<int:problem_id>/',submit,name = 'submit'),
    
]