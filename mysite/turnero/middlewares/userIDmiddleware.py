from functools import wraps
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect

def UserIDMiddleware(fun):
    @wraps(fun)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('NotFound')
        if not request.session['user_id'] == kwargs.get('token_userID'):
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        return fun(request, *args, **kwargs)
    return wrapper