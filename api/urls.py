from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TechnicianProfileView,
    TechnicianTaskListView,
    TechnicianTaskDetailView,
    TokenTestView,
    TaskStatusUpdateView,
    CustomLoginView,
    TechnicianProfileUpdateView,
    FilteredTaskListView,
    CompletedTaskListView,
    ServiceChargeViewSet,
    StartTaskView,
    PaymentModeListView,
    LogoutView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'tasks/service-charge', ServiceChargeViewSet, basename='service-charge')

urlpatterns = [
    # JWT Auth endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test-token/', TokenTestView.as_view(), name='test-token'),

    # Technician API endpoints
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    path('logout/', LogoutView.as_view(), name='token_logout'),
    path('profile/', TechnicianProfileView.as_view(), name='technician-profile'),
    path('tasks/', TechnicianTaskListView.as_view(), name='technician-task-list'),
    path('tasks/<int:pk>/', TechnicianTaskDetailView.as_view(), name='technician-task-detail'),
    path('tasks/<int:pk>/update-status/', TaskStatusUpdateView.as_view(), name='technician-task-status-update'),
    path('profile/update/', TechnicianProfileUpdateView.as_view(), name='technician-profile-update'),
    path("tasks/<int:pk>/start/", StartTaskView.as_view(), name="start-task"),
    path('payment-modes/', PaymentModeListView.as_view(), name='payment-mode-list'),
    #path('tasks/service-charge/', ServiceChargeViewSet.as_view(), name='service-charge'),
    path('', include(router.urls)),
]

urlpatterns += [
    path('tasks/completed/', CompletedTaskListView.as_view(), name='technician-completed-tasks'),
]


urlpatterns += [
    path('tasks/filter/', FilteredTaskListView.as_view(), name='technician-task-filter'),
]
from django.urls import path
from .views import IssuedItemListView, ReturnItemView

urlpatterns += [
    path('take/issued/', IssuedItemListView.as_view(), name='issued-items'),
    path('take/return/', ReturnItemView.as_view(), name='return-item'),
]


from .views import TaskBillingCreateView

urlpatterns += [
    path('submit-bill/<int:pk>/', TaskBillingCreateView.as_view(), name='submit-bill'),
]
