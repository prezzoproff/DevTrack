from django.shortcuts import render
from .ai_assistant import devtrack_ai_assistant
from django.http import HttpResponse
from .models import Issues



# Create your views here.
def issues_page(request):
    issues = Issues.objects.all()

    return render(request, 'issues/issues.html', {'issues' : issues})

def ai_assistant_view(request):
    assistant = devtrack_ai_assistant  

    if request.method == "POST":
        user_message = request.POST.get("message", "")
        response = assistant.chat(user_message, request.user)  
        return render(request, "issues/ai_chat.html", {"response": response, "message": user_message})

    return render(request, "issues/ai_chat.html")