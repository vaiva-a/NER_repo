from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from .models import TagManager,Admin,Annotators
import os
from django.core.files.storage import default_storage
from django.conf import settings
from django.http import JsonResponse, FileResponse, HttpResponseBadRequest

import pandas as pd

@login_required(login_url='')
def home(request):
    tag_manager = TagManager.get_instance()
    return render(request, 'tags/home.html', {'tags': tag_manager.tags})

@login_required(login_url='')
def adminhome(request):
    tag_manager = TagManager.get_instance()
    return render(request, 'tags/adminhome.html', {'tags': tag_manager.tags})

@csrf_exempt
def add_tag(request):
    if request.method == 'POST':
        tag_manager = TagManager.get_instance()
        data = json.loads(request.body)
        new_tag = data.get('tag')
        if new_tag and new_tag not in tag_manager.tags:
            tag_manager.tags.append(new_tag)
            tag_manager.save()
            return JsonResponse({'status': 'success', 'tags': tag_manager.tags})
    return JsonResponse({'status': 'error'})
# Create your views here.

@csrf_exempt
def clear_tags(request):
    if request.method == 'POST':
        try:
            # Get or create the TagManager instance
            tag_manager = TagManager.get_instance()
            
            # Clear the tags
            tag_manager.tags = []
            tag_manager.save()

            return JsonResponse({'status': 'success', 'message': 'All tags removed successfully.'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def add_annotator(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # Validate required fields
            if not username or not password:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Username and password are required'
                })

            # Check if username already exists
            if Annotators.objects.filter(username=username).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Username already exists'
                })

            # Generate next ID
            last_annotator = Annotators.objects.order_by('-ID').first()
            next_id = 1 if not last_annotator else last_annotator.ID + 1

            user = User.objects.create_user(username=username,email=username,password=password)
            Annotators.objects.create(ID=next_id,username=username, password=password)
            # Create new annotator
            # annotator = Annotators(
            #     ID=next_id,
            #     username=username,
            #     password=password  # Note: Consider using password hashing
            # )
            # annotator.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Annotator created successfully',
                'data': {
                    'id': next_id,
                    'username': username
                }
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })

@csrf_exempt
def submit_file(request):
    if request.method == 'POST':
        # Parse the filename from the POST request
        body = json.loads(request.body)
        filename = body.get('filename')

        data = json.loads(request.body)

        filename = data.get("filename", "default.xlsx")
        annotations = data.get("data", [])

        results_dir = os.path.join(settings.BASE_DIR, 'tagproject', 'results')
        os.makedirs(results_dir, exist_ok=True)  # Ensure directory exists

        file_path = os.path.join(results_dir, "annotations.xlsx")

        # Convert annotations to DataFrame
        records = []
        for sentence in annotations:
            print(sentence)
            sentence_number = sentence.get("sentence_number", "")
            for word_data,tags in sentence.get("annotations", {}).items():
                print(word_data)
                records.append({
                    "Sentence Number": sentence_number,
                    "Word": word_data[0:],
                    "Tag": tags[0:]
                })

        df = pd.DataFrame(records)

        # Append or create the file
        if os.path.exists(file_path):
            existing_df = pd.read_excel(file_path)
            df = pd.concat([existing_df, df], ignore_index=True)

        df.to_excel(file_path, index=False)

        if not filename:
            return JsonResponse({"status": "error", "message": "Filename is required."})

        # Path to the picked files JSON
        picked_files_path = os.path.join(settings.BASE_DIR, 'tagproject', 'picked_files.json')

        # Ensure the JSON file exists
        if not os.path.exists(picked_files_path):
            with open(picked_files_path, 'w') as f:
                json.dump([], f)

        # Load the picked files list
        with open(picked_files_path, 'r') as f:
            picked_files = json.load(f)

        # Add the filename if not already present
        if filename not in picked_files:
            picked_files.append(filename)
            with open(picked_files_path, 'w') as f:
                json.dump(picked_files, f)

        return JsonResponse({"status": "success", "message": f"File '{filename}' has been submitted."})

    return JsonResponse({"status": "error", "message": "Invalid request method."})

def get_paragraph(request):
    # Define the path to the text files directory
    text_files_dir = os.path.join(settings.BASE_DIR, 'tagproject', 'text_files')
    
    # Define the path for the JSON file to track picked files
    picked_files_path = os.path.join(settings.BASE_DIR, 'tagproject', 'picked_files.json')

    # If the JSON file doesn't exist, create it with an empty list
    if not os.path.exists(picked_files_path):
        with open(picked_files_path, 'w') as f:
            json.dump([], f)

    # Load the list of picked files
    with open(picked_files_path, 'r') as f:
        picked_files = json.load(f)

    # List all text files in the directory
    all_text_files = [f for f in os.listdir(text_files_dir) if f.endswith('.txt')]

    # Find the remaining files that have not been picked yet
    remaining_files = [f for f in all_text_files if f not in picked_files]

    # Handle case when there are no remaining files
    if not remaining_files:
        return JsonResponse({"status": "error", "message": "All text files have been picked."})

    # Pick the next file (no sorting, just the first unpicked file in the list)
    next_file = remaining_files[0]
    file_path = os.path.join(text_files_dir, next_file)

    # Read the content of the picked file
    with open(file_path, 'r') as file:
        content = file.read()

    # Add the picked file to the list and update the JSON file
    # picked_files.append(next_file)
    # with open(picked_files_path, 'w') as f:
    #     json.dump(picked_files, f)

    return JsonResponse({"status": "success", "paragraph": content, "filename": next_file})

def skip_file(request):
    # Ensure session variable exists
    if 'skipped_files' not in request.session:
        request.session['skipped_files'] = []

    # Path to text files and picked files JSON
    text_files_dir = os.path.join(settings.BASE_DIR, 'tagproject', 'text_files')
    picked_files_path = os.path.join(settings.BASE_DIR, 'tagproject', 'picked_files.json')

    # Ensure the picked files JSON exists
    if not os.path.exists(picked_files_path):
        with open(picked_files_path, 'w') as f:
            json.dump([], f)

    # Load the picked files list
    with open(picked_files_path, 'r') as f:
        picked_files = json.load(f)

    # Parse the current filename from the frontend
    current_file = request.GET.get('currentFileName', None)
    
    if current_file and current_file not in request.session['skipped_files']:
        request.session['skipped_files'].append(current_file)
        request.session.modified = True

    # List all text files in the directory
    all_text_files = [f for f in os.listdir(text_files_dir) if f.endswith('.txt')]

    # Find files not yet picked or skipped
    remaining_files = [f for f in all_text_files if f not in picked_files and f not in request.session['skipped_files']]

    # Handle case when no files are left
    if not remaining_files:
        request.session['skipped_files'] = []  # Clear session variable
        request.session.modified = True
        return JsonResponse({"status": "error", "message": "Last file reached."})


    # Pick the next file
    next_file = remaining_files[0]
    file_path = os.path.join(text_files_dir, next_file)

    # Read the content of the next file
    with open(file_path, 'r') as file:
        content = file.read()

    return JsonResponse({"status": "success", "paragraph": content, "filename": next_file})



def reset_picked_files(request):
    picked_files_path = os.path.join(settings.BASE_DIR, 'tagproject', 'picked_files.json')

    try:
        print(f"Attempting to reset the file at {picked_files_path}")  # Debugging line
        with open(picked_files_path, 'w') as f:
            json.dump([], f)

        return JsonResponse({"status": "success", "message": "Picked files list has been reset."})
    
    except Exception as e:
        print(f"Error resetting picked files: {str(e)}")  # Debugging line
        return JsonResponse({"status": "error", "message": str(e)})

def login_page(request):
    if request.method == "POST":
        # admin_user = Admin.objects.create(username="admin", password="admin")
        username = request.POST.get('username')
        password = request.POST.get('password')
       
        user = authenticate(request, username=username, password=password)
        # Check for admin login
        try:
            
            print("here1")
            admin_user = Admin.objects.get(username=username, password=password)
            print(admin_user,user)
            if admin_user and user is not None:
                print("Admin authenticated")
                login(request,user)
                return redirect('/adminhome')  # Redirect to admin home
                
            else:
                return render(request, 'registration/login.html')

        except Admin.DoesNotExist:
            pass  # Proceed to user login check if not admin

        # Check for annotator login
        try:
            print("here")
            print(username,password)
            annotator_user = Annotators.objects.get(username=username, password=password)
            print(annotator_user,user)
            if annotator_user and user is not None:
                print("Annotator authenticated")
                login(request,user)
                return redirect('/home')  # Redirect to user home
            else:
                print("doesnt exist")
                return render(request, 'registration/login.html')
        except Annotators.DoesNotExist:
            pass

        # If neither admin nor user credentials match
        err_msg = {"msg": "Username or password is wrong, please try again"}
        return render(request, 'registration/login.html', err_msg)

    return render(request, 'registration/login.html')
        
UPLOAD_DIR = os.path.join(settings.BASE_DIR, 'tagproject', 'text_files')

os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure directory exists

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

        with default_storage.open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        return JsonResponse({'status': 'success', 'message': 'File uploaded successfully!'})

    return JsonResponse({'status': 'error', 'message': 'No file provided!'}, status=400)

RESULTS_DIR = os.path.join(settings.BASE_DIR, 'tagproject','results')

def list_result_files(request):
    if request.method == 'GET':
        try:
            print("hello")
            files = [f for f in os.listdir(RESULTS_DIR) if f.endswith('.xlsx')]
            print(files)
            print("after")
            return JsonResponse({'files': files})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

def download_result_file(request):
    filename = request.GET.get('filename')
    if not filename:
        return HttpResponseBadRequest('Missing filename')

    file_path = os.path.join(RESULTS_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    else:
        return JsonResponse({'status': 'error', 'message': 'File not found'})

@csrf_exempt
def delete_result_file(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        filename = data.get('filename')
        if not filename:
            return JsonResponse({'status': 'error', 'message': 'Filename is required'})

        file_path = os.path.join(RESULTS_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return JsonResponse({'status': 'success', 'message': 'File deleted successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'File not found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
