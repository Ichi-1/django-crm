from django.urls import path
from .views import (
    AgentListView, AgentCreateView, AgentDeleteView,
    AgentUpdateView, AgentDetailView
)

app_name = 'agents'

urlpatterns = [
    path('', AgentListView.as_view(), name='agent-list'),
    path('create/', AgentCreateView.as_view(), name='agent-create'),
    path('<int:pk>/detail/', AgentDetailView.as_view(), name='agent-detail'),
    path('<int:pk>/delete/', AgentDeleteView.as_view(), name='agent-delete'),
    path('<int:pk>/update/', AgentUpdateView.as_view(), name='agent-update'),
]
