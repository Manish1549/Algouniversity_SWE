from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.conf import settings
import os 
import subprocess
from pathlib import Path
from compiler.models import Codesubmission,Problem,Testcases
import uuid
from django.contrib.auth.decorators import login_required
import google.generativeai as genai
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))

# Create your views here.
@login_required
@csrf_exempt
def ai_review(request,problem_id):
    
    problem = get_object_or_404(Problem,id = problem_id)
    last_submission = Codesubmission.objects.filter(user=request.user, problem=problem).order_by('-timestamp').first()
    if not last_submission:
        return HttpResponse("No previous Submission Found")
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
        Please review this coding problem solution and provide constructive feedback in 3-5 bullet points  and write in short and beutiful structured :
        
        Problem Description:
        {problem.description}
        
        User's Solution (in {last_submission.language}):
        {last_submission.code}

        also error may be there {last_submission.error}
        
        Please provide:
        1. Code quality assessment
        2. Potential improvements
        3. Alternative approaches
        4. Performance considerations
        """  
  
  
    response = model.generate_content(
                prompt)
        
    
    feedback_items = [
        line.strip() for line in response.text.split('\n') 
        if line.strip().startswith('-')
    ]
    
    context = {"last_submission":last_submission,"problem":problem,"response_text":response.text}
    return render(request,'ai_review.html',context)
 



@login_required
def submit(request,problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    last_submission = Codesubmission.objects.filter(user=request.user,problem=problem).order_by('timestamp').first()
    if request.method == "POST":
        
        user_name = request.user
        language = request.POST.get('language')
        code = request.POST.get('code')
        testcases = problem.testcases_set.all()
        problem_name = problem

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
                error = f"Expected {testcase.expected_output.strip()} but got {output_data}"
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
            problem = problem_name,
            user = user_name,
            language =  language,
            code = code,
            input_data = input_data,
            output_data = "\n".join(results),
            verdict = verdict,
            error = error
        )
        submission.save()
        return render(request,'compiler.html',{"submission" : submission,"problem" :problem,"last_submission":submission})
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


              
