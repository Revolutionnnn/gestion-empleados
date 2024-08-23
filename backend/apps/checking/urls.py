from . import views
from django.urls import path


urlpatterns = [
    path('<int:document>/', views.CheckingListCreateView.as_view(), name='check-person-api'),
    path('inside/', views.CheckinsTodayListView.as_view(), name='check-insede-api'),
    path('report-range/', views.ReportRangeAPIView.as_view(), name='report-range-api'),
    path('report-area/', views.ReportAreaRangeAPIView.as_view(), name='report-area-api'),
]
