def handler_user_data_redirection(request):
    response_value = getattr(request, 'handler_redirection_value', False)
    return {
        'handler_user_data_redirection':response_value
    }