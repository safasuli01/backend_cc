from django.urls import path
from .views import ProposalCreateView, ProposalListView

urlpatterns = [
    path('list/', ProposalListView.as_view(), name='proposal-list'),
    path('create/', ProposalCreateView.as_view(), name='proposal-create'),
]
