from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm #Import the form

# Create your views here.
# --- ADD Function ---
def task_search(request):
    # --- Logic for adding a Task ---
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
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
        results = Task.objects.filter(title__icontains = query)
    else:
        results = Task.objects.all()

    # --- Pass both 'results' and 'form' to the template ---
    return render(request, 'tasks/search_results.html', {
        'tasks':results,
        'form':form
        })

# --- EDIT Function ---
def edit_task(request, task_id):
    #1. Fetch the specific task or return a 404 error if it doesn't exist
    task = get_object_or_404(Task, pk=task_id)

    if request.method == "POST":
        #2. Pass 'instance=task' so Django knows we are updating, not creating
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/') #Redirect to your main list or home
    else:
        #3. If GET, show the form pre-filled with the task's current data
        form = TaskForm(instance = task)

    return render(request, 'tasks/edit_task.html', {'form':form, 'task':task})

# --- DELETE Function ---
def delete_task(request, task_id):
    #1. Fetch the task
    task = get_object_or_404(Task, pk=task_id)
    
    #2. Delete it
    task.delete()

    #3. Redirect back to the search/list page
    return redirect('task_search')
