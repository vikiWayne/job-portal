from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib.auth import login, authenticate
from django.views.generic import ListView
from employer.forms import PostJobForm, CompanyRegisterForm
from employer.models import Employer, Jobs

# Create your views here.

# company = Company.objects.get(id=1)

def post_job(request):
    pass
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
    # return render(request,'employer/post_job.html', context)

def company_register(request):
    return render(request,'employer/register.html')

class JobDetailView(DetailView):
    model = Jobs
    template_name = 'employer/job_detail.html'

class EmployerListView(ListView):
    model = Employer
    template_name = 'employer/employers.html'
    paginate_by = 10
    