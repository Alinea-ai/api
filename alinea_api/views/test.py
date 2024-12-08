from django.shortcuts import render


def websocket_test(request):
    return render(request, 'doctor_dashboard.html')


def access_requests_view(request):
    return render(request, 'user_dashboard.html')

def template_builder_view(request):
    return render(request, 'template.html')