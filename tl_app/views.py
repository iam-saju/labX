# In tl_app/views.py

#threading
# Removed duplicate import: from django.conf import settings
import time
from django.contrib import messages
import threading
from django.shortcuts import render,redirect,HttpResponse
from .forms import UploadFileForm,ChatForm
from django.conf import settings # Keep this one
from .tl_utility import send_file_to_telegram,check_chat_id
import json
import time
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Removed incorrect self-import: # from .views import upload,login,logout

threads = []
count=0


print("--- views.py is being imported ---") # Keep this print at the top

def login(request):
    print("--- Inside login view ---") # Debug print
    if request.method == 'POST':
        print("--- Handling POST request in login ---") # Debug print
        form = ChatForm(request.POST)
        if form.is_valid():
            print("--- Login form is valid ---") # Debug print
            phno = form.cleaned_data['phno']
            username = request.POST.get('username')
            print(f"--- Attempting check_chat_id for Username={username}, Phone={phno} ---") # Debug print

            try: # Add a try/except block to catch potential errors
                result = check_chat_id(phno)
                print(f"--- check_chat_id result: {result} ---") # Debug print

                if result and result.get('status'): # Check result and status key
                    token = result.get('chat_id')
                    if token: # Ensure token is not None or empty if needed
                         print(f"--- check_chat_id success, token: {token} ---") # Debug print
                         # Store in session
                         request.session['username'] = username
                         request.session['phno'] = phno
                         request.session['token'] = token # Store the actual token

                         print("--- Redirecting to upload ---") # Debug print
                         # messages.success(request, f"Welcome, {username}!") # Optional: Add a message
                         return redirect('upload')
                    else:
                         print("--- check_chat_id success but returned no chat_id ---") # Debug print
                         error_message = "Login failed: Could not retrieve chat ID."
                         # messages.error(request, error_message) # Optional: Add a message
                         return render(request, 'success.html', {'form': form, 'error': error_message})

                else: # Failure path from check_chat_id
                    print("--- check_chat_id status is False ---") # Debug print
                    error_message = result.get('message', "Login failed: Invalid phone number or user.") # Get message from result if available
                    # messages.error(request, error_message) # Optional: Add a message
                    return render(request, 'success.html', {'form': form, 'error': error_message})

            except Exception as e: # Catch any exception during check_chat_id or subsequent code
                print(f"--- ERROR during login POST handling: {e} ---") # Debug print the error
                # You might want to log the full traceback here in a real application
                error_message = f"An unexpected error occurred during login: {e}"
                # messages.error(request, error_message) # Optional: Add a message
                # Render the page again with an error message
                return render(request, 'success.html', {'form': form, 'error': error_message})


        else: # Form is not valid
            print(f"--- Login form errors: {form.errors} ---") # Debug print form errors
            # Render the same page with errors
            # messages.error(request, "Please correct the errors below.") # Optional: Add a message
            return render(request, 'success.html', {'form': form})

    else: # Handling GET request
        print("--- Handling GET request in login ---") # Debug print
        form = ChatForm()
        # messages.info(request, "Please log in.") # Optional: Add a message
        return render(request, 'success.html', {'form': form})

# Note: login_page seems unused based on your urls.py
def login_page(request):
    # This view is not mapped in your provided urls.py
    print(settings.key) # Note: settings.key is not a standard Django setting
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
    print("--- Inside upload view ---")
    message = None
    error = None


    if request.method == 'POST':
        print("--- Handling POST request in upload ---")
        # Note: Getting username/phno from POST is usually only on login.
        # For upload POST, you likely only need it from the session.
        username = request.session.get('username')
        phno = request.session.get('phno')
        token=request.session.get('token')

        # Ensure session variables exist before proceeding with upload logic
        if not username or not phno or not token:
             print("--- Upload POST failed: Session data missing ---")
             # Redirect back to login or show an error
             messages.error(request, "Please log in to upload files.")
             return redirect('login')


        print("CHAT ID IN UPLOAD PAGE",token)
        print(f"User from session: {username}, {phno}")

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
            print(f"--- Upload POST failed: form errors: {form.errors} ---") # Add print for form errors in POST
    else: # Handling GET request for /upload/
        print("--- Handling GET request in upload ---") # This print should work
        print("--- About to create UploadFileForm ---") # Add this print
        form = UploadFileForm()
        print("--- UploadFileForm created successfully ---") # Add this print

    print("--- About to render hi.html ---") # Add this print (runs for both GET and POST)
    return render(request, 'hi.html', {
        'form': form,
        'message': message,
        'error': error
    })
# Replace this with your bot's API token # This comment is misplaced

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