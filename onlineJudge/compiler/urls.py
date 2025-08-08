from django.urls import path, include
from compiler.views import submit,problem_list,ai_review

urlpatterns = [
    path('problems/',problem_list,name='problems'),
    path('problems/<int:problem_id>/',submit,name = 'submit'),
    path('problems/<int:problem_id>/ai-review/',ai_review,name='ai_review'),
]