from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import UpdateView, ListView, DetailView, TemplateView
from django.contrib.auth.models import Group

from employer.models import Jobs,Employer, ExamQuestion, OpenedExams
from job_seeker.forms import SignUpForm, CustomUserChangeForm, EditEmployeeForm, AddressForm, ResumeForm
from job_seeker.models import JobApplication, JobSeeker
from job_seeker.decorators import unauthenticated_user, allowed_users

def home(request):
    
    context = {
        'total_jobs' : Jobs.objects.filter(is_opened=True).count(),
        'jobs': Jobs.objects.filter(is_opened=True).order_by('-posted_date'),
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
            
            group = Group.objects.get(name = 'employee')
            user.groups.add(group)
            
            return redirect('login')
    else:
        form = SignUpForm()
    context = {
        'form' : form
    }
    return render(request, 'job_seeker/signup.html', context)

@login_required
def profile(request):
    if not request.user.is_employee:
        return redirect('home')
    user_id = request.user.jobseeker.id
    emp = JobSeeker.objects.get(id = user_id)
    context = {
        'object' : emp
    }
    return render(request, 'job_seeker/profile.html', context)

class ProfileView(LoginRequiredMixin, DetailView):
    model = JobSeeker
    template_name = 'job_seeker/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['pk']
        context['object'] = self.model.objects.select_related('user').get(id=user_id)
        return context

def applications(request):
    total_applications = JobApplication.objects.filter(user = request.user.jobseeker).order_by('-applied_date')
    return total_applications

@login_required
@allowed_users(allowed_roles=['employee'])
def edit_profile(request):
    total_applications = applications(request)
    # form = ResumeForm()
    context = {
        'applications' : total_applications,
        'total_applications' : total_applications.count(),
        # 'form' : form,
            }
    return render(request,'job_seeker/account/my_account.html',context)

@login_required
@allowed_users(allowed_roles=['employee'])
def edit_employee(request):
    total_applications = applications(request)
    if request.method == 'POST':
        form1 = CustomUserChangeForm(request.POST, instance=request.user)
        form2 = EditEmployeeForm(request.POST, request.FILES, instance=request.user.jobseeker)
        form3 = AddressForm(request.POST, instance=request.user.jobseeker.address)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect('edit_emp_data')
        if form3.is_valid():
            form3.save()
            return redirect('edit_emp_data')
    else:
        form1 = CustomUserChangeForm(instance=request.user)
        form2 = EditEmployeeForm(instance=request.user.jobseeker)
        form3 = AddressForm(instance=request.user.jobseeker.address)
    context = {
        'form1' : form1,
        'form2' : form2,
        'form3' : form3,
        'applications' : total_applications,
        'total_applications' : total_applications.count(),
    }
    return render(request,'job_seeker/account/edit_account.html',context)

@login_required
@allowed_users(allowed_roles=['employee'])
def upload_resume(request):
    pass
    # return render(request, 'job_seeker/account/resume.html', context)

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
        if job.is_opened:
            print(job,'\n\n\n')
            try:
                self.model.objects.get(user=self.request.user.jobseeker, jobs=job)
            except self.model.DoesNotExist:
                self.model.objects.create(user=self.request.user.jobseeker, jobs=job)
            return HttpResponse(status = 201)
        return HttpResponse(status = 403)

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
    queryset = Jobs.objects.all().filter(is_opened = True)
    template_name = 'job_seeker/jobs.html'
    paginate_by = 10
    ordering = ['-posted_date']

class ViewExams(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model   = OpenedExams
    template_name = 'job_seeker/exam/exam.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_applications = JobApplication.objects.filter(user=self.request.user.jobseeker) 
        availableExams = OpenedExams.objects.filter(is_open=True)
        exams= []
        context['total'] = total_applications
        context['available'] = availableExams

        for applied_exam in total_applications:
            for exam in availableExams:
                if applied_exam.jobs == exam.job:
                    exams.append(exam)            
        context['examList'] = exams

        return context

    def test_func(self):
        try:
            if self.request.user.jobseeker:
                return True
        except:
            return False
        return False

class ExamAttendView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ExamQuestion
    template_name = 'job_seeker/exam/view_questions.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.kwargs['pk']
        context['title'] = None
        try:
            title = Jobs.objects.filter(id=job)
            context['title'] = title[0].title
        except Jobs.DoesNotExist:
            return redirect('viewExam')
        
        context['object'] = None

        try:
            context['object'] = self.model.objects.filter(job=job)
        except self.model.DoesNotExist:
            return redirect('viewExam')
        return context

    def test_func(self):
        try:
            if self.request.user.jobseeker:
                return True
        except:
            return False
        return False

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