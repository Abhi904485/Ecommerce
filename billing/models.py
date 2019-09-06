from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL


class BillingProfile(models.Model):
    billing_profile_id = models.AutoField(db_column='billing_profile_id', verbose_name='Billing Profile Id',
                                          help_text='this is Billing Profile Primary key ',
                                          error_messages={'required': 'Enter Billing Profile Primary key'},
                                          primary_key=True, default=1)

    billing_profile_user = models.OneToOneField(to=User, null=True, blank=True, help_text="User One to one field",
                                                verbose_name="Billing User",
                                                error_messages={'required': "User is necessary"},
                                                on_delete=models.CASCADE, db_column='billing_profile_user')

    billing_profile_email = models.EmailField(error_messages={'required': "Email is necessary"},
                                              verbose_name='Billing Email',
                                              null=False, blank=True, help_text="Billing profile mail",
                                              db_column='billing_profile_email')

    billing_profile_active = models.BooleanField(verbose_name='Billing Profile Status',
                                                 error_messages={'required': "profile Status"},
                                                 db_column='billing_profile_active',
                                                 help_text="Billing profile status",
                                                 default=True,
                                                 )

    billing_profile_update_time = models.DateTimeField(auto_now=True, verbose_name="Billing profile Update",
                                                       help_text="Billing profile Update",
                                                       error_messages={
                                                               'required': 'Billing profile Update time required'},
                                                       db_column='billing_profile_update_time')

    billing_profile_create_time = models.DateTimeField(auto_now_add=True, verbose_name="Billing Profile Creation",
                                                       help_text="Billing Profile Creation",
                                                       error_messages={
                                                               'required': 'Billing profile Create Time required'},
                                                       db_column='billing_profile_create_time')

    def __str__(self):
        return self.billing_profile_email

    def __unicode__(self):
        return self.billing_profile_email

    class Meta:
        db_table = 'BillingProfile'
        verbose_name_plural = 'BillingProfiles'


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.billing_profile_email:
        BillingProfile.objects.get_or_create(user=instance, billing_profile_email=instance.billing_profile_email)


post_save.connect(user_created_receiver, sender=User)
