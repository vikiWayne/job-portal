from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib.auth import login, authenticate
from django.views.generic import ListView,CreateView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import Group


from employer.forms import PostJobForm, EmployerRegistrationForm
from employer.models import Employer, Jobs
from job_seeker.models import User, JobApplication
from job_seeker.decorators import unauthenticated_user, allowed_users


@unauthenticated_user
def RegisterEmployerView(request):
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST)
        if form.is_valid():
            employer = form.save(commit=False)
            password = form.cleaned_data.get('password1')
            employer.set_password(password)
            employer.save()
            
            group = Group.objects.get(name = 'employer')
            employer.groups.add(group)
            
            return redirect('login')
    else:
        form = EmployerRegistrationForm()
     
    context = {
        'form' : form
    }
    return render(request, 'employer/register.html', context)

@login_required
@allowed_users(allowed_roles=['employer'])
def edit_employer(request):
    if request.method == 'POST':
        form = PostJobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            try:
                employer = User.objects.get(email=request.user)
            except User.DoesNotExist:
                pass
            job.posted_by = employer.employer
            job.save()
            return redirect('employer-account   ')
    else:
        form = PostJobForm()
    context = {
        'form' : form
    }
    return render(request, 'employer/account/post-job.html',context)


class JobDetailView(DetailView):
    model = Jobs
    template_name = 'employer/job_detail.html'

    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        job_id = self.kwargs['pk']
        job = self.model.objects.get(id=job_id)
        try:
            applied_job = JobApplication.objects.get(jobs = job)
            context['applied_job'] = applied_job.jobs
        except JobApplication.DoesNotExist:
            pass
        context['object'] = job
        return context

class EmployerDetailView(DetailView):
    model = Employer
    template_name = 'employer/employer_detail.html'

    def get_context_data(self, **kwargs):
        employer_id = self.kwargs['pk']
        employer = Employer.objects.get(id= employer_id )
        context = super(EmployerDetailView, self).get_context_data(**kwargs)
        context['job_count'] = Jobs.objects.all().filter(posted_by = employer).count()
        return context
        
class EmployerListView(ListView):
    model = Employer
    template_name = 'employer/employers.html'
    paginate_by = 10

class JobsByEmployerView(ListView):
    model = Jobs
    paginate_by = 10
    template_name = 'job_seeker/jobs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employer = get_object_or_404(Employer,id= self.kwargs['pk'])
        context['object_list'] = self.model.objects.all().filter(posted_by = employer)
        return context

