from django import template
from .models import User
from django.utils import timezone

register = template.Library()

@register.simple_tag
def login_count():
    user_count = User.objects.filter(date_joined__startswith=timezone.now().date()).count()
    users_today = User.objects.filter(date_joined__startswith=timezone.now().date())
    
    context = {
        'user_count' : user_count,
        'users_today': users_today
    }

    return context


def each_context(self, request):
        context = super().each_context(request)
        # context.update({
        #     "whatever", "this is",
        #     "just a": "dict",
        # })
        user_count = User.objects.filter(date_joined__startswith=timezone.now().date()).count()
        users_today = User.objects.filter(date_joined__startswith=timezone.now().date())
        context.update{
            'user_count' : user_count,
            'users_today': users_today
        }
        return context