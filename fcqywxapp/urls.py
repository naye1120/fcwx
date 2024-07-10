# myapp/urls.py
from django.urls import path

from fcqywxapp.views import qywxrenzheng

urlpatterns = [
    path('api/qywxrenzheng/', qywxrenzheng.as_view(), name='qywxrenzheng'),

]