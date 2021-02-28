from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .base import UserManager

class Department(models.Model):
    department_name = models.CharField(max_length=100)

    



class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100,default="dufault")
    last_name = models.CharField(max_length=100,default="dufault")
    username = models.CharField(max_length=100)
    user_number = models.IntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
    user_salary = models.IntegerField(null=True, blank=True)
    user_role = models.CharField(max_length=100, null=True, blank=True)
    department = models.ForeignKey(Department, models.CASCADE, default='2')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    head = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)
    

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

class Expenses(models.Model):
    employee = models.ForeignKey(User,models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    hotel_rent = models.IntegerField(null=True, blank=True)
    transport = models.IntegerField(null=True, blank=True)
    meal = models.IntegerField(null=True, blank=True)
    others = models.IntegerField(null=True, blank=True)
    form_status = models.BooleanField(default=None, null=True, blank=True)
    total_amount = models.IntegerField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)




class Budget(models.Model):
    department = models.ForeignKey(Department,models.CASCADE)
    budget_monthly = models.IntegerField()
    budget_yearly = models.IntegerField()


    def remaining_monthly_budget(self):
        expenses = Expenses.objects.filter(department=self.department, form_status=True)
        total = 0
        for expense in expenses:
            total += expense.total_amount
        return self.budget_monthly - total


    def remaining_yearly_budget(self):
        expenses = Expenses.objects.filter(department=self.department, form_status=True)
        total = 0
        for expense in expenses:
            total += expense.total_amount
        return self.budget_yearly - total


    
    def expense_approval(self, id):
        exp = Expenses.objects.get(id=id)
        if self.remaining_monthly_budget() < exp.total_amount:
            return False
        else:
            return True