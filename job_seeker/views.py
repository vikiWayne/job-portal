from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import UpdateView

from employer.models import Jobs,Employer
from job_seeker.forms import SignUpForm, CustomUserChangeForm, EditEmployeeForm
from job_seeker.models import JobApplication
from job_seeker.decorators import unauthenticated_user, allowed_users

def home(request):
    context = {
        'total_jobs' : Jobs.objects.count(),
        'jobs': Jobs.objects.all(),
        'total_emp' : Employer.objects.count() -1
    }
    return render(request,'job_seeker/home.html',context)

@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.save()
            return redirect('login')
    else:
        form = SignUpForm()
    context = {
        'form' : form
    }
    return render(request, 'job_seeker/signup.html', context)

# ******************************************** LOGICAL MISS MATCH **********************************************
@login_required
def profile(request):
    if not request.user.is_employee:
        return redirect('home')
    return render(request, 'job_seeker/profile.html')

@login_required
@allowed_users(allowed_roles=['employee'])
def edit_profile(request):
    total_applications = JobApplication.objects.all().filter(user = request.user.jobseeker)
    context = {
        'applications' : total_applications,
        'total_applications' : total_applications.count(),
    }
    return render(request,'job_seeker/account/my_account.html', context)

# ******************************************** LOGICAL MISS MATCH **********************************************


def SearchResultsView(request):
    try:
        query = request.GET.get('job')
    except:
        query = None

    if query:
        jobs = Jobs.objects.filter(title__icontains=query)
        context = {'query' :query, 'jobs': jobs }
        template = 'job_seeker/search.html'
        return render(request, template, context)
    else:
        return redirect('home')


class JobApplyView(LoginRequiredMixin, View):
    model = JobApplication
    def post(self, request, *args, **kwargs):
        job_id = request.POST.get('job_id')
        job = get_object_or_404(Jobs,id=job_id)
        print(job,'\n\n\n')
        try:
            self.model.objects.get(user=self.request.user.jobseeker, jobs=job)
        except self.model.DoesNotExist:
             self.model.objects.create(user=self.request.user.jobseeker, jobs=job)
        return HttpResponse(status = 201)

class CancelJobApplication(LoginRequiredMixin, View):
    model = JobApplication
    def post(self, request, *args, **kwargs):
        job_id = request.POST.get('job_id')
        job = get_object_or_404(Jobs,id=job_id)

        try:
            applid_job = self.model.objects.get(user=self.request.user.jobseeker, jobs=job)
            if applid_job:
                applid_job.delete()
        except self.model.DoesNotExist:
            pass
        return HttpResponse(status = 204)

class JobListView(ListView):
    model = Jobs
    template_name = 'job_seeker/jobs.html'
    paginate_by = 10

# ERROR PAGES - production
def handler404(request, exception):
    return render(request,'error/404.html', status=404)








# class EmployeeUpdateView(UpdateView):
    # template_name = 'template can be tha same as create template'
    # form_class = #instacne of form , form must be a model form
    # queryset = optional custom query

    # def get_object(self):
    #     id_ = self.kwargs.get('')
    #     return get_object_or_404(ModelName, id=id_)