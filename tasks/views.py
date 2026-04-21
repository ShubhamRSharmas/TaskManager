from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm #Import the form
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout

# Create your views here.
# --- ADD Function ---
def task_search(request):
    # --- Logic for adding a Task ---
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False) #Don't save to DB yet!
            task.user = request.user       #Attach the current user
            task.save()                    #Now save to DB  
            return redirect('task_search') #Refresh the page to show new task
        else:
            #If the form is invalid, print errors to terminal to debug
            print(form.errors)

    else:
        #Initialize an empty form here so it's available for both GET and POST
        form = TaskForm()   
        
    # --- Logic for searching ---
    #In FastAPI: q = Optional[str]
    #In Django:
    query = request.GET.get('q')

    if query:
        #In FastAPI: .where(col(Task.task).contains(query))
        #In Django
        results = Task.objects.filter(title__icontains = query, user=request.user)
    else:
        results = Task.objects.filter(user=request.user)

    # --- Pass both 'results' and 'form' to the template ---
    return render(request, 'tasks/search_results.html', {
        'tasks':results,
        'form':form
        })

# --- EDIT Function ---
@login_required
def edit_task(request, task_id):
    #1. Fetch the specific task or return a 404 error if it doesn't exist || Implemented data ownership enforcement by filtering database queries with "user=request.user" in get_object_or_404(). This ensures that objects are only retrieved if they belong to authenticated user, preventing "Insecure Direct Object Reference" (IDOR) vulnerabilities. The "user" association is handled via a Foreign Key defined in "Task" model which maps tasks to the User model managed by Django's built-in authentication system. || The browser doesn't send the user ID; the session cookie tells the server who the user is, and Django automatically populates "request.user" || I'm using the "user" attribute of the "request" object to scope the query. This guarantees that the database operation is isolated to the authenticated session context.
    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == "POST":
        #2. Pass 'instance=task' so Django knows we are updating, not creating
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            #Since task.user is already set from original object
            # and verified by get_object_or_404, you can just save()!
            task.save()                      #Now save to DB
            return redirect('/') #Redirect to your main list or home
    else:
        #3. If GET, show the form pre-filled with the task's current data
        form = TaskForm(instance = task)

    return render(request, 'tasks/edit_task.html', {'form':form, 'task':task})

# --- DELETE Function ---
@login_required #Prevents non-logged-in users from accessing this | If the user isn't logged in, they are redirected to login page before the function even runs
def delete_task(request, task_id):
    #1. Fetch the task and verify ownership in one go
    #We filter by both ID and current user
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    
    #2. If it's found delete it
    task.delete()

    #3. Redirect back to the task list
    return redirect('task_search')

# --- REGISTER Function ---
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Send a "success" message that will appear on the next page
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# --- LOGIN Function ---
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            #Get user object from the validated form
            user = form.get_user()
            #Start the session
            login(request,user)
            messages.success(request, 'Login Successful! Redirecting to search page...')
            return redirect('task_search')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form':form})
    
