from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta

def antiSpamMiddleware(fun):
    @wraps(fun)
    def wrapper(request, *args, **kwargs):
        SPAM_LIMIT_TIME = 60
        user_id = request.user.userID if request.user.is_authenticated else request.META.get('REMOTE_ADDR')
        lastRequestTime = request.session.get(f'last_request_time_{user_id}')

        if lastRequestTime:
            lastRequestTime = timezone.datetime.fromisoformat(lastRequestTime)
            currentTime = timezone.now()
            if currentTime - lastRequestTime < timedelta(seconds=SPAM_LIMIT_TIME):
                messages.warining(request=request, message='Se han enviado demasiadas solicitudes en poco tiempo. Por favor, espere unos segundos.')
                return redirect('Contactos')

        request.session[f'last_request_time_{user_id}'] = timezone.now().isoformat()
        return fun(request, *args, **kwargs)

    return wrapper