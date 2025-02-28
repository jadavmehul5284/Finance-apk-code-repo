from django.http import JsonResponse

def admin_dashboard(request):
    return JsonResponse({"message": "Admin Panel Running"})