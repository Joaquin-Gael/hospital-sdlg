from django.utils.functional import SimpleLazyObject

def handler_user_data_redirection(request):
    if isinstance(request.user, SimpleLazyObject):
        return {
            'handler_user_data_redirection':False
        }
    response_value = getattr(request, 'handler_redirection_value', False)
    return {
        'handler_user_data_redirection':response_value
    }