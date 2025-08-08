from django.db import models
from django.contrib.auth.models import User


#problem model 
class Problem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    constraints = models.TextField()
    example_input = models.TextField()
    example_output = models.TextField()

    def __str__(self):
        return self.title


#testcases model
class Testcases(models.Model):
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE,null=True,blank=True)
    input_data = models.TextField()
    expected_output = models.TextField()

    def __str__(self):
        return f"Testcases for the {self.problem.title}"
    

# Create your models here.
class Codesubmission(models.Model):
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    language = models.CharField(max_length=100)
    code = models.TextField()
    input_data = models.TextField(null =True,blank=True)
    output_data = models.TextField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    VERDICT_CHOICES = [
        ('AC', 'Accepted'),
        ('WA', 'Wrong Answer'),
        ('RE', 'Runtime Error'),
        ('TLE', 'Time Limit Exceeded'),
        ('CE', 'Compilation Error'),
    ]
    verdict= models.CharField(max_length=3,choices=VERDICT_CHOICES,default='WA')

    error = models.TextField(blank=True) 
    


    



