from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import task_form
from .models import task
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone

# Create your views here.
def home(request):
    return render(request, "tasks/home.html")

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                username = request.POST['username']
                password = request.POST['password1']
                user = User.objects.create_user(username=username, password=password)
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, "tasks/signup.html", {
                    "form":UserCreationForm(),
                    "error":"User allready exists"
                })
        else:
            return render(request, "tasks/signup.html", {
                    "form":UserCreationForm(),
                    "error":"Password does not match"
                })
    else:
        return render(request, "tasks/signup.html", {
            'form':UserCreationForm()
        })

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            return render(request, 'tasks/signin.html', {
            'form':AuthenticationForm(),
            'error':'Los datos ingresados no coinciden'
        })

    else:
        return render(request, 'tasks/signin.html', {
            'form':AuthenticationForm()
        })

@login_required
def tasks(request):
    tasks = task.objects.filter(user=request.user, date_completed__isnull = True)
    return render(request, 'tasks/tasks.html', 
    {'tasks':tasks})

@login_required
def create_task(request):
    if request.method == 'POST':
        try:
            form = task_form(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks/create_task.html', {
            'form':task_form(),
            'error':'Please provide valid data.'
        })
    else:
        return render(request, 'tasks/create_task.html', {
            'form':task_form()
        })

@login_required
def task_detail(request, id):
    if request.method == 'POST':
        try:
            task_detail = get_object_or_404(task, pk=id, user=request.user)
            form = task_form(request.POST, instance=task_detail)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks/task_detail.html', 
        {'task':task_detail,
        'form':form,
        'error':'Error actualizando el formulario'
        })
    else:
        task_detail = get_object_or_404(task, pk=id, user=request.user)
        form = task_form(instance=task_detail)
        return render(request, 'tasks/task_detail.html', 
        {'task':task_detail,
        'form':form
        })

@login_required
def task_complete(request, id):
    if request.method == 'POST':
        task_detail = get_object_or_404(task, pk=id, user=request.user)
        task_detail.date_completed = timezone.now()
        task_detail.save()
        return redirect('tasks')

@login_required
def task_delete(request, id):
    if request.method == 'POST':
        task_detail = get_object_or_404(task, pk=id, user=request.user)
        task_detail.delete()
        return redirect('tasks')

@login_required
def tasks_completed(request):
    tasks_completed = task.objects.filter(user=request.user, date_completed__isnull=False)
    return render(request, 'tasks/task_completed.html', 
    {'tasks':tasks_completed})
    

