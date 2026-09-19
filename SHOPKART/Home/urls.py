from django.urls import path
from django.conf.urls import handler404, handler500
from . import views


urlpatterns=[
    path('',views.home, name='home'),
    path('contact/',views.contact, name='contact'),
    path('about/',views.about, name='about'),
    path('faq/',views.faq, name='faq'),
]

handler404 = 'Home.views.page_not_found'
handler500 = 'Home.views.server_error'
