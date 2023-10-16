

def get_current_domain(request):
    return request.scheme + '://' + request.get_host()
