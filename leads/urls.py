from django.urls import path
from .views import (
    AssignedAgentView, CategoryListView, CategoryDetailView,
    CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    LeadListView, LeadDetailView, LeadCreateView,
    LeadUpdateView, LeadDeleteView, LeadCategoryUpdateView
)

app_name = 'leads'

urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('<int:pk>/assign-agent/', AssignedAgentView.as_view(), name='assign-agent'),
    path('<int:pk>/category', LeadCategoryUpdateView.as_view(), name='lead-category-update'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('create-category/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/update', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete', CategoryDeleteView.as_view(), name='category-delete'),

]
