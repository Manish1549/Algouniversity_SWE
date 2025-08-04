from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.conf import settings
import os 
import subprocess
from pathlib import Path
from compiler.models import Codesubmission,Problem,Testcases
import uuid
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def submit(request,problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    last_submission = Codesubmission.objects.filter(user=request.user,problem=problem).order_by('timestamp').first()
    if request.method == "POST":
        
        language = request.POST.get('language')
        code = request.POST.get('code')
        testcases = problem.testcases_set.all()
        

        results =[]
        all_passed = True     
        test_num =1
        error =''
        compile_error = False
        for testcase in testcases :
            input_data = testcase.input_data
            output_data,error,compile_error = run_code(language,code,input_data)
            
            if error.strip() :
                  if compile_error:
                      verdict ='CE'
                      results.append("Compilation Error !")
                      error = error
                      break
                  print("Compilation Successful\n")
                  verdict='RE'
                  error = error
                  results.append(f"Runtime Error on Testcase {test_num}")
                  all_passed = False
                  break
            if output_data.strip() != testcase.expected_output.strip():
                results.append(f"Testcase {test_num} failed")
                error = f"Expected {testcase.expected_output.strip()} but got {output_data.strip()}"
                verdict = 'WA'
                all_passed = False
                break
            else :
                 results.append(f"Testcase {test_num} Passed")
                 
                 
            test_num+=1

        if all_passed :
            verdict = 'AC'
        
        
         
        #save to db
        submission = Codesubmission.objects.create(
            language =  language,
            code = code,
            input_data = input_data,
            output_data = "\n".join(results),
            verdict = verdict,
            error = error
        )
        submission.save()
        return render(request,'compiler.html',{"submission" : submission,"problem" :problem})
    #get 
    return render(request,'compiler.html',{"problem":problem,"last_submission":last_submission})

def run_code(language,code,input_data):
    project_path = Path(settings.BASE_DIR)
    directories = ["codes","inputs","outputs"]
    for directory in directories:
        dir_path = project_path/directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True,exist_ok=True)

    codes_dir = project_path/"codes"
    input_dir = project_path/"inputs"
    output_dir = project_path/"outputs"

    unique = str(uuid.uuid4())

    code_file_name = f"{unique}.{language}"
    input_file_name = f"{unique}.txt"        
    output_file_name = f"{unique}.txt"  

    code_file_path = codes_dir/code_file_name
    input_file_path = input_dir/input_file_name
    output_file_path = output_dir/output_file_name

    with open(code_file_path,"w") as code_file:
        code_file.write(code)

    with open(input_file_path,"w") as input_file:
        input_file.write(input_data)

    with open(output_file_path,"w") as output_file:
        pass
    
    if language == "cpp":
       exec_path = codes_dir/unique
       compile_result = subprocess.run(["g++",str(code_file_path),"-o",str(exec_path)],stderr=subprocess.PIPE,text=True)
       
       if compile_result.returncode !=0:
           compile_error = True
           return "", compile_result.stderr,True
       
       with open(input_file_path,"r") as input_file:
            with open(output_file_path,'w') as output_file:
                   result = subprocess.run([exec_path],
                                  stdin=input_file,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)
                   output_file.write(result.stdout)
                   return result.stdout,result.stderr,False
                   
    elif language=="py":
        with open(input_file_path,'r') as input_file:
            with open(output_file_path,'w') as output_file:
                result =subprocess.run(['python',str(code_file_path)],
                               stdin=input_file,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True)
                
                output_file.write(result.stdout)
                return result.stdout,result.stderr,False
    return "", "Unknown language or execution failed",False
        


def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'problem_list.html', {'problems': problems})


              
