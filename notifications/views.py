from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def liste_notifications(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'notifications/liste_notifications.html', {'notifications': notifications})

@login_required
def marquer_comme_lu(request, notification_id):
    notification = Notification.objects.get( id=notification_id, user=request.user)
    notification.lu = True
    notification.save()
    return redirect('notifications:liste')