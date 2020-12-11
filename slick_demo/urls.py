"""slick_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from slick_example import views

urlpatterns = [
                  path('admin/', admin.site.urls),

                  path('', views.Index.as_view()),
                  path('raw/', views.GroupByViewWith2ChartsRaw.as_view()),
                  path('setup/', views.SetupView.as_view(), name='report-model'),
                  path('no-group-by/', views.SimpleListReport.as_view(), name='simple-filer'),
                  path('no-group-by-plus-charts/', views.NoGroupByPlusChart.as_view()),

                  path('group-by/', views.GroupByIntro.as_view()),
                  path('group-by-chart/', views.GroupByView.as_view()),
                  path('group-by-with-several-charts/', views.GroupByViewWith2Charts.as_view()),
                  path('group-by-date/', views.LogIns.as_view()),

                  path('time-series/', views.TimeSeries.as_view()),
                  path('time-series-charts/', views.TimeSeriesCustomization.as_view()),
                  path('crosstab/', views.CrossTabReportView.as_view()),
                  path('crosstab-charts/', views.CrosstabCustomization.as_view()),

                  path('thank-you', views.ThankYou.as_view()),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
