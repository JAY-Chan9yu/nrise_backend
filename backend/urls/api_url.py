from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    # oatuh2 token todo: oauth2로 구현하려고 했지만, 문서 내용을 보면 oauth2를 사용안하는 것 같아 주석처리
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # api url
    url(r'^', include('api.urls', namespace='api')),
]
