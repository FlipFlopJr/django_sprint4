from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from django.conf.urls.static import static

urlpatterns = [
    path('', include('blog.urls', namespace='blog')),
    # path('posts/', include('blog.urls', namespace='blog')),
    # path('category/', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('blog:index'),
        ),
        name='registration',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.failure_500'
