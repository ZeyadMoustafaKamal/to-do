from django.shortcuts import render,redirect
from tasks.models import Task
from accounts.models import UserProfile
from django.contrib import messages

# Create your views here.

def index(request):


    # If the user is authenticated => not anonymous show the tasks from the database
    # I made the tasks in a separate app to make my project ready for all future changes
    
    tasks = None
    verified = None

    if not request.user.is_anonymous:
        user = UserProfile.objects.get(user = request.user)
        verified = user.verified
        tasks = user.tasks.all()

    if request.method == 'GET' and 'add-task' in request.GET:
        # show an error if the user is anonymous

        if request.user.is_anonymous:
            messages.error(request,'You have to login first')
        # if the user isn't anonymous add the task in the database and add it to the many to many field
        
        else:
            name = request.GET['task-to-add']
            user = UserProfile.objects.get(user = request.user)
            task = Task(name = name)
            task.save()
            user.tasks.add(task)

    # here is the button to update the tasks state ( id_done or not )

    if 'submit-tasks' in request.POST:
        states = request.POST.getlist('checkk')
        for task in tasks:
            if str(task.id) in states:
                task.is_done = True
            else:
                task.is_done = False
            task.save()
        return redirect('index')


    # delete a task
    if 'btndelete' in request.POST:
        task_todelete = Task.objects.get( id = request.POST['btndelete'])
        user.tasks.remove(task_todelete)
        return redirect('index')
        
    context = {
        'tasks':tasks,
        'verified':verified,
        
    }
    return render(request,'pages/index.html',context)
    
def whoami(request):
    # here is the Who am I page
    return render(request,'whoami.html')



