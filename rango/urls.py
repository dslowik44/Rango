from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from rango import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='main'),
		url(r'^about/$', views.about, name='about'),
		url(r'^add_category/$', views.add_category, name='add_category'),
	    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
		url(r'^add_page/(?P<category_name_slug>[\w\-]+)/$', views.add_page, name='add_page'),
    	#url(r'^register/$', views.register, name='register'),
        #url(r'^reg_success/$', TemplateView.as_view(template_name='rango/reg_success.html')), 
		#url(r'^login/$', views.user_login, name='login'),
		#url(r'^logout/$', views.user_logout, name='logout'),
		)
