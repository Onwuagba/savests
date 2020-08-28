from django.contrib import admin
from .models import User
from django.utils import timezone
from django.urls import path, reverse
from django.utils.html import format_html
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import EmailForm
from django.core.mail import send_mail
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_active", "date_joined", "last_login", "update_status")
    change_list_template = 'admin/savestsapp/user/user_change_button.html'
    # date_hierarchy = 'date_joined'

    def get_urls(self):
        urls = super(UserAdmin, self).get_urls()
        new_urls = [
            path('<int:id>/change/', self.admin_site.admin_view(self.change_status), name='change'),
            path('send_email/', self.admin_site.admin_view(self.send_email), name='sendEmail'),
        ]
        return new_urls + urls


    def update_status(self, obj):
        url = (
            reverse('admin:change', args=[obj.id])
        )
        return format_html('<a class="button" href="{}">Update</a>', url)

    update_status.short_description = 'Change user state'
    update_status.allow_tags = True

    def change_status(self, request, id):
        context = {}
        try:
            user = self.model.objects.get(id=id)
            if user.is_active == True:
                user.is_active = False
                user.save()
            else:
                user.is_active = True
                user.save()
            messages = "User state has been successfully changed"
        except ObjectDoesNotExist:
            messages = "User does not exist"
        context = {'messages': messages}
        return redirect('/admin/savestsapp/user/')
        # return render(request, 'admin/savestsapp/user/user_change_button.html', context)  
        
    #send email by staff
    def send_email(self, request):
        title = "Send message to all users"
        user = request.user
        to_emails = []
        if request.method == 'POST':
            form = EmailForm(request.POST)
            all_user = User.objects.all()
            if form.is_valid():
                subject = form.cleaned_data['subject']
                content = form.cleaned_data['content']

                #Retrieve user emails and append to to_emails list
                for use in all_user:
                    user_email = use.email #get each user's email
                    if user_email: 
                        to_emails.append(user_email)

                #check if user is staff and if not, set email field to empty
                if user.is_staff == True:
                    from_email = user.email
                    #ensure no field is empty
                    if subject and content and from_email and to_emails:
                        try:
                            send_mail(subject, content, from_email, to_emails)
                            messages = "Your mail was sent successfully."
                            form = EmailForm()
                        except BadHeaderError:
                            messages = "Invalid header found."  
                    else:
                        messages = "Error processing form."
                else:
                    messages = "Login with a staff account."

            context = {'form': form,'title':title,'messaging': messages}

        else:
            form = EmailForm()
            context = {'form': form,'title':title}

        return render(request, 'admin/savestsapp/user/send_email.html', context)    

#Editing admin dashboard
class MyAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        context = super().each_context(request)
        users_today = User.objects.filter(date_joined__startswith=timezone.now().date())
        print (users_today)
        user_count = users_today.count()
        context.update ({
            'user_count' : user_count,
            'users_today': users_today
        })
        print (context)
        return context


# admin.site.register(User, UserAdmin)
admin.site.index_template = "admin/savestsapp/index.html"