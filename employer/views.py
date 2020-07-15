from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, authenticate
from django.views.generic import ListView,CreateView, DetailView, UpdateView, DeleteView
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import Group


from employer.forms import PostJobForm, EmployerRegistrationForm, ProfileUpadteForm, ExamCreateForm
from employer.models import Employer, Jobs, ExamQuestion
from job_seeker.models import User, JobApplication
from job_seeker.decorators import unauthenticated_user, allowed_users
from job_seeker.forms import CustomUserChangeForm

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
def post_job(request):
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
            return redirect('employer-account')
    else:
        form = PostJobForm()
    context = {
        'form' : form
    }
    return render(request, 'employer/account/post-job.html',context)

class JobUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Jobs
    template_name = 'employer/account/post-job.html'
    fields = ['title', 'description','qualifications','experience', 'salary', 'location', 'type', 'is_opened']
    # success_url = '/'

    
    def form_valid(self, form):
        form.instance.posted_by = self.request.user.employer
        return super().form_valid(form)
    
    def test_func(self):
        job = self.get_object()
        if self.request.user.employer == job.posted_by:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('applicants', kwargs={'pk': self.object.pk})
    
class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Jobs
    success_url = '/'
    template_name = 'employer/account/jobs_confirm_delete.html'

    def test_func(self):
        job = self.get_object()
        if self.request.user.employer == job.posted_by:
            return True
        return False

@login_required
@allowed_users(allowed_roles=['employer'])
def view_applicants(request):
    employer = get_object_or_404(Employer,id= request.user.employer.id)
    jobs= Jobs.objects.select_related('posted_by').filter(posted_by = employer).order_by('-posted_date')
    
    context = {
        'jobs' : jobs,
    }
    return render(request, 'employer/account/view_jobs.html', context)

class GetApplicants(LoginRequiredMixin, ListView):
    model = JobApplication
    template_name = 'employer/account/view_applicants.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_id = self.kwargs['pk']
        try:
            job = Jobs.objects.values('title', 'id', 'is_opened').filter(posted_by = self.request.user.employer.id).get(id=job_id)
            context['job'] = job
        except Jobs.DoesNotExist:
            pass
        try:
            applicants = self.model.objects.filter(jobs=job_id).filter(jobs__posted_by=self.request.user.employer).order_by('-applied_date')
            context['applicants'] = applicants
        except JobApplication.DoesNotExist:
            pass
        return context



@login_required
@allowed_users(allowed_roles=['employer'])
def update_employer_account(request):
    if request.method == 'POST':
        form1 = ProfileUpadteForm(request.POST, instance = request.user.employer)
        form2 = CustomUserChangeForm(request.POST, instance=request.user)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect('employer-account-update')
    else:
        form1 = ProfileUpadteForm(instance = request.user.employer)
        form2 = CustomUserChangeForm(instance=request.user)
    
    context = {
        'form1' : form1,
        'form2' : form2
    }
    return render(request,'employer/account/update.html',context)


class JobDetailView(DetailView):
    model = Jobs
    template_name = 'employer/job_detail.html'

    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        job_id = self.kwargs['pk']
        try:
            job = self.model.objects.get(id=job_id)
        except Jobs.DoesNotExist:
            pass

        if self.request.user.is_authenticated and self.request.user.is_employee:
            try:
                applied_job = JobApplication.objects.filter(user=self.request.user.jobseeker).get(jobs = job)
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
        context['object_list'] = self.model.objects.all().filter(posted_by = employer).order_by('-posted_date')
        return context


@login_required
@allowed_users(allowed_roles=['employer'])
def ExamCreateView(request, job_id):
    try:
        job = Jobs.objects.get(id=job_id)
        if job.is_opened:
            print('\n\n\n', job.is_opened)
            return redirect('applicants', pk=job.id) 
        count = ExamQuestion.objects.filter(job=job).count()
    except Jobs.DoesNotExist:
        return redirect('employer-applicants')
    if request.method == 'POST':
        form = ExamCreateForm(request.POST)
        if form.is_valid():
            job_form = form.save(commit=False)
            job_form.job = job
            job_form.save()
            return redirect('exam',job_id=job.id)
    if request.method == 'GET':
        form = ExamCreateForm()
    context = {
        'form'  : form,
        'job' : job,
        'count' : count+1
    }
    return render(request, 'employer/exam/exam.html', context)