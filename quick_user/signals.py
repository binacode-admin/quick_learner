from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from .models import QuickUser, QuickUserProfile

@receiver(post_save, sender=QuickUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        QuickUserProfile.objects.create(user=instance)

@receiver(post_save, sender=QuickUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(user_logged_in)
def update_last_login_date(sender, request, user, **kwargs):
    user.profile.last_login_date = timezone.now()
    user.profile.save()


@receiver(post_save, sender=QuickUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:  # Only send email when a new user is created
        subject = "Welcome to QLearner!"
        message = f"Hello {instance.profile.first_name},\n\nWelcome to QLearner! We're excited to have you on board."

        # Send email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )