from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView,  DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task
from .forms import PositionForm

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True # Eğer kullanıcı giriş yapmışsa register sayfasına gitmesini engelliyoruz.
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save() # formdan gelen bilgileri kaydediyoruz.
        if user is not None:
            login(self.request, user) # login fonksiyonu ile kullanıcıyı otomatik olarak giriş yapıyoruz.
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated: # Eğer kullanıcı giriş yapmışsa register sayfasına gitmesini engelliyoruz.
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks') # reverse_lazy fonksiyonu ile tasks urline yönlendiriyoruz.

    def form_valid(self, form):
        form.instance.user = self.request.user # form.instance.user ile formdan gelen user bilgisini alıyoruz.
        return super(TaskCreate, self).form_valid(form) # formu geçerli kılmak için form_valid fonksiyonunu override ediyoruz.

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))
