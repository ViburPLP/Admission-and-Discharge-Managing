from django.utils import timezone

def greeting(request):
    now = timezone.now()
    
    if 0 <= now.hour < 12:
        greeting_text = 'Good Morning'
    elif 12 <= now.hour < 15:
        greeting_text = 'Good Afternoon'
    elif 15 <= now.hour < 22:
        greeting_text = 'Good Evening'
    else:
        greeting_text = 'Good Night'

    return {'greeting': greeting_text}
