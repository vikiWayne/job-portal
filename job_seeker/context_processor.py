from job_seeker.models import JobApplication
from django.http import HttpResponse

def job_count(request):
    try:
        total_applications = JobApplication.objects.all().filter(user = request.user.jobseeker)
    except JobApplication.DoesNotExist:
        return HttpResponse(status = 404)
    context = {
        'applications' : total_applications,
        'total_applications' : total_applications.count(),
            }
    return context
