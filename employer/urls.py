from django.urls import path, include
from employer.views import  (
                    RegisterEmployerView, 
                    post_job, 
                    view_applicants, 
                    GetApplicants,
                    JobUpdateView,
                    JobDeleteView,
                    update_employer_account,
                    ExamCreateView,
                    FinishExam
                    )

urlpatterns = [
    path('register/', RegisterEmployerView, name='employer-register'),
    path('account/',  post_job, name='employer-account'),
    path('account/update/',  update_employer_account, name='employer-account-update'),
    path('account/my-applicants/', view_applicants, name='employer-applicants'),
    path('account/my-applicants/<int:pk>/', GetApplicants.as_view(), name='applicants' ),
    path('account/my-applicants/<int:job_id>/create-exam/', ExamCreateView, name='exam' ),
    path('account/my-applicants/<int:job_id>/create-exam/finish/', FinishExam.as_view(), name='exam_finish' ),
    path('job/<int:pk>/update/', JobUpdateView.as_view(), name='job_update'),
    path('job/<int:pk>/delete/', JobDeleteView.as_view(), name='job_delete'),
]