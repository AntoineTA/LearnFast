from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

registration_patterns = ([
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutRedirectView.as_view(), name='logout'),
], 'registration')

profile_patterns = ([
    path('', views.ProfileRedirectView.as_view(), name='own'),
    path('list', views.UserListView.as_view(), name='list'),
    path('<int:pk>', views.ProfileView.as_view(), name='detail'),
    path('edit', views.ProfileEditView.as_view(), name='edit'),
    path('notification/read/<int:notif_id>', views.NotificationReadView.as_view(), name='notification_read'),
    path('notification/unread/<int:notif_id>', views.NotificationUnreadView.as_view(), name='notification_unread'),
    path('notification/delete/<int:notif_id>', views.NotificationDeleteView.as_view(), name='notification_delete'),
], 'profile')

course_patterns = ([
    path('', views.CourseListView.as_view(), name='list'),
    path('create', views.CourseCreateView.as_view(), name='create'),
    path('<int:pk>', views.CourseView.as_view(), name='detail'),
    path('<int:pk>/enroll', views.CourseEnrollView.as_view(), name='enroll'),
    path('<int:pk>/feedback/add', views.CourseFeedbackAddView.as_view(), name='feedback_add'),
    path('<int:pk>/material/add', views.CourseMaterialAddView.as_view(), name='material_add'),
    path('<int:pk>/student/block/<int:student_id>', views.CourseStudentBlockView.as_view(), name='student_block'),
    path('<int:pk>/student/unblock/<int:student_id>', views.CourseStudentUnblockView.as_view(), name='student_unblock'),
], 'course')

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('', include(registration_patterns)),
    path('profile/', include(profile_patterns)),
    path('course/', include(course_patterns)),
]