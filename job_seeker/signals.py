from django.db.models.signals import post_save
from job_seeker.models import JobSeeker, Resumes, Address
from django.dispatch import receiver

# when a user is created a resume filed is created for the user 

@receiver(post_save, sender=JobSeeker)
def create_resume(sender, instance, created, **kwargs):
    if created:
        Resumes.objects.create(jobseeker=instance)


@receiver(post_save, sender= JobSeeker)
def save_resume(sender, instance, **kwargs):
    instance.resumes.save()

# when a user is created a address filed is created for the user 

@receiver(post_save, sender=JobSeeker)
def create_address(sender, instance, created, **kwargs):
    if created:
        Address.objects.create(jobseeker=instance)

@receiver(post_save, sender= JobSeeker)
def save_address(sender, instance, **kwargs):
    instance.address.save()