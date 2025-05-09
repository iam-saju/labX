#threading
from django.conf import settings
import time
from django.contrib import messages
import threading
from django.shortcuts import render,redirect,HttpResponse
from .forms import UploadFileForm,ChatForm
from django.conf import settings
from .tl_utility import send_file_to_telegram,check_chat_id
import json
import time
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

threads = []
count=0


def login(request):
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            phno = form.cleaned_data['phno']
            username = request.POST.get('username')
            
            
            
            # Debug output
            print(f"Form valid: Username={username}, Phone={phno}")
            result=check_chat_id(phno)
            if result['status']:
                token=result['chat_id']

                # Store in session
                request.session['username'] = username
                request.session['phno'] = phno
                request.session['token']=result['chat_id']


                print("chat id in login",token)
                return redirect('upload')
            else:
                return render(request, 'success.html', {'form': form})
        else:
            print(f"Form errors: {form.errors}")
            # Render the same page with errors
            return render(request, 'success.html', {'form': form})
    else:
        form = ChatForm()
    return render(request, 'success.html', {'form': form})

def login_page(request):
    print(settings.key)
    return render(request, 'tl.html')
    

def thread1(file,file_name,token):
    thread= threading.Thread(target=upload_file, args=(file, f"{file_name}",token))
    thread.start()
    print(file_name+"is in thread1 ")
    return thread

def thread2(file,file_name,token):
    thread= threading.Thread(target=upload_file, args=(file, f"{file_name}",token))
    thread.start()
    print(file_name+"is in thread2 ")
    return thread

def thread3(file,file_name,token):
    thread= threading.Thread(target=upload_file, args=(file, f"{file_name}",token))
    thread.start()
    print(file_name+"is in thread3 ")
    return thread

# Create a thread pool for parallel uploads
def upload_file(file,message,token):
    response=send_file_to_telegram(file, file.name, message,token)
     # Debugging

def upload(request):
    message = None
    error = None
    
 
    if request.method == 'POST':
        username = request.POST.get('username') or request.session.get('username')
        phno = request.POST.get('phno') or request.session.get('phno')
        token=request.session.get('token')

        # Make sure we store these in the session
        request.session['username'] = username
        request.session['phno'] = phno
        request.session['token']=token

        print("CHAT ID IN UPLOAD PAGE",token)

        print(username, phno)

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_files = request.FILES.getlist('file_field') 
            length = len(uploaded_files)
            
            threads = []

            start = time.perf_counter()
            for f in range(0, length, 3):
                t1 = thread1(uploaded_files[f], uploaded_files[f].name,token)
                threads.append(t1)

                if f+1 < length:
                    t2 = thread2(uploaded_files[f+1], uploaded_files[f+1].name,token)
                    threads.append(t2)

                    if f+2 < length:
                        t3 = thread3(uploaded_files[f+2], uploaded_files[f+2].name,token)  # Fixed index from f+1 to f+2
                        threads.append(t3)

            for t in threads:
                t.join()
            end = time.perf_counter()

            duration = end - start
            total_size = sum(f.size for f in uploaded_files)
            total_size = (total_size/1024)/1000
            speed = (total_size / duration)
            
            message = "Files uploaded successfully!"
            print(f'{message} of size : {total_size:.2f} mb completed in {duration:.2f} seconds @ {speed:.2f} mbps')
        else:
            error = "Invalid form submission."
    else:
        form = UploadFileForm()

    return render(request, 'hi.html', {
        'form': form,
        'message': message,
        'error': error
    })
# Replace this with your bot's API token

def logout(request):
    """
    Log out the user by clearing their session data
    """
    # Clear specific session variables
    if 'username' in request.session:
        del request.session['username']
    
    if 'phno' in request.session:
        del request.session['phno']
        
    # Optional: You can also flush the entire session if desired
    request.session.flush()
    
    messages.success(request, "You have been logged out successfully!")
    
    # Redirect to the login page
    return redirect('login')
