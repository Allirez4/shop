from django.shortcuts import get_object_or_404, render
from .models import supportsession , chatmessage
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
@login_required
def sessions(request):
    user=request.user
    if True:
        if user.is_staff:
            sessions=supportsession.objects.filter(is_active=True)
            return render(request,'chat/admin_support.html',{'sessions':sessions})
        else:
            return redirect('home:home')
            
def room(request,session_id):
    session = get_object_or_404(supportsession, user__id=session_id)
    
    # Now filter messages by the actual session object
    messages = chatmessage.objects.filter(session=session).order_by('timestamp')
    user_username = request.user.username
    return render(request, 'chat/room.html', {
        'session_id': session_id,
        'messages': messages,
        'user_username': user_username
    })
    