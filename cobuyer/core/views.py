from shortcuts import request_to_response

#-------------------------------------------------------------------------------
def home(request):
    data = dict()
    return request_to_response(request, 'index.html', data)
    
#-------------------------------------------------------------------------------
def handler500(request):
    from django.template import loader, RequestContext
    from django import http
    return http.HttpResponseServerError("500.html".render(RequestContext(request, {})))

