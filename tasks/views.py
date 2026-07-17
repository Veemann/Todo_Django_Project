from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from django.shortcuts import get_object_or_404
from .forms import TaskForm, RegisterForm
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib.auth import authenticate, login, logout
from .forms import TaskForm, RegisterForm
from django.contrib import messages

# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Already signed in!')
        return redirect('home')

    form = RegisterForm()
    errors =None
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()    
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) 
                messages.success(request,'Account created successfuly!')   
                return redirect('home')
            else:
                messages.error(request, 'Error creating account. Please try again.')
                return redirect('login')
        else:
            errors = form.errors.as_data()
            messages.error(request, errors)
            return redirect('register')
        
    context = {
        'form':form,
        'errors':errors
    }
    
    return render(request, 'register.html', context)

@login_required(login_url='login')
def home(request):
    date = datetime.datetime.now()
    h = int(date.strftime('%H'))
    
    msg = 'Good '
    
    if h < 12:
        msg += 'Morning'
    elif h < 16:
        msg += 'Afternoon'
    elif h < 18:
        msg += 'Evening'
    else: 
        msg += 'Night'
    
    greetings = f'{msg}! Veemann'
    
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    #reads everything
    
    
    context = {
        'greetings': greetings,
        'tasks':tasks
        
        }
        
    return render(request, 'home.html', context)
    
def login_view(request):
    if request.user.is_authenticated:
        messages.success(request, 'Already signed in!')
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('login')
        
        
    return render(request, 'login.html')

def logout_view(request):
    user =request.user
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def add_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        due_time = request.POST.get('due_time')
        
        task = Task.objects.create(
            title=title,
            due_time=due_time
        )
        task.save()
        return redirect('home')
    return render (request, 'add_task.html')
        
@login_required(login_url='login')
def filter_tasks(request, foo):
    if foo == 'true':
        tasks = Task.objects.filter(done=True, user=request.user).order_by('-created_at'),
    elif foo == 'false':
        tasks = Task.objects.filter(done=False, user=request.user).order_by('-created_at'),
    else:
        pass
    
    context = {
        'tasks':tasks
    }
    return render(request, 'home.html', context)

@login_required(login_url='login')
def update_task(request, pk):
    #task = Task.objects.get(id=pk)
    task = get_object_or_404(Task, id=pk, user=request.user)
    form = TaskForm(instance=task)
    
    
    if request.method == "POST":
        form.save()
        messages.success(request, 'Task updated successfully!')
        return redirect('home')
    else:
        # title = request.POST.get('title')
        # done = request.POST.get('done')
        errors = form.errors.as_data()
        messages.error(request, errors)
        due_time = request.POST.get('due_time')
        
        #=========================#
        #assign values to task#
        #=========================#
        
        task.title = title
        if done:
            task.done = True
        else: 
            task.done = False
            
        task.due_time = due_time
        
        #save task
        task.save()
        
    context = {
        'task':task
    }
    return render(request, 'update_task.html', context)

@login_required(login_url='login')
def delete_task(reques, pk):
    task = get_object_or_404(Task, id=pk)
    task.delete()
    return redirect(home)