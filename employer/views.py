from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib.auth import login, authenticate
from django.views.generic import ListView,CreateView
from django.http import HttpResponseRedirect

from employer.forms import PostJobForm, EmployerRegistrationForm
from employer.models import Employer, Jobs
from job_seeker.models import User
from job_seeker.decorators import unauthenticated_user, allowed_users
# company = Company.objects.get(id=1)

@login_required
@allowed_users(allowed_roles=['employer'])
def post_job(request):
    # pass
    # if request.method == 'POST':
    #     form = PostJobForm(request.POST)
    #     if form.is_valid():
    #         job = form.save(commit=False)
    #         job.posted_by = company
    #         job.save()
    #         return redirect('post_job')
    # else:
    #     form = PostJobForm()
    # context = {
    #     'form' : form
    # }
    return render(request,'employer/post_job.html')

@unauthenticated_user
def RegisterEmployerView(request):
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST)
        if form.is_valid():
            employer = form.save(commit=False)
            password = form.cleaned_data.get('password1')
            employer.set_password(password)
            employer.save()
            return redirect('login')
    else:
        form = EmployerRegistrationForm()
     
    context = {
        'form' : form
    }
    return render(request, 'employer/register.html', context)

class JobDetailView(DetailView):
    model = Jobs
    template_name = 'employer/job_detail.html'

class EmployerListView(ListView):
    model = Employer
    template_name = 'employer/employers.html'
    paginate_by = 10
    