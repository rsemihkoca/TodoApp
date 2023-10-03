from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Task
class TaskList(ListView):
    model = Task
    context_object_name = 'tasks' # Modelden gelen verileri tasks adında bir değişken ile templateye gönderiyoruz.
class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'
class TaskCreate(CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks') # reverse_lazy fonksiyonu ile tasks urline yönlendiriyoruz.