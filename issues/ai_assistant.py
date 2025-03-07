import json
from django_ai_assistant import AIAssistant, method_tool
from .models import Issues

class DevtrackAiAssistant(AIAssistant):
    id = 'devtrack_assistant'
    name = 'Devtrack Ai Assistant'
    instructions = (
        "You are a AI assisatnt for projct management in Devtrack"
        "Help users manage projects, tasks and issues effectively"
    )
    model = 'gpt-4o'

    @method_tool
    def get_current_user_email(self) -> str:
        '''get current user'''
        return self._users.email
    
    @method_tool
    def get_user_assigned_issues(self, user_email:str) -> str:
        """get issues assigned to a certain user"""
        issues = Issues.objects.filter(assigned_to__email=user_email).values('id', 'title', "description", "priority", "status", "created_at")

        return json.dumps({'issues' : list(issues)})
    
    @method_tool
    def assign_issue(self, issue_id: int, user_email: str) -> str:
        """Assign an issue to a user"""
        try:
            issue = Issues.objects.get(id=issue_id)
            issue.assigned_to.email = user_email
            issue.save()
            return f"Issue {issue_id} has been assigned to {user_email}."
        except Issues.DoesNotExist:
            return f"Issue {issue_id} not found."

    @method_tool
    def create_issue(self, title: str, description: str) -> str:
        """Create a new issue"""
        issue = Issues.objects.create(title=title, description=description)
        return f"Issue '{title}' has been created with ID {issue.id}."
    
    def chat(self, user_message: str, user):
        """Handles AI chat messages."""
        response = f"Processing message: {user_message}"  # Placeholder logic
        return response

# Register the assistant
devtrack_ai_assistant = DevtrackAiAssistant()
    