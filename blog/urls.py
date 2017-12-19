from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^post/(?P<pk>[-\d]+)/$', login_required(views.PostDetailView.as_view()), name="post_detail"),
    url(r'^post/(?P<pk>[-\d]+)/add_comment/$', login_required(views.AjaxCreateCommentFormView.as_view()), name="add_comment"),
    url(r'^post_create/$', login_required(views.CreatePostFormView.as_view()), name="post_create"),
    url(r'^toggle_like/(?P<pk>[-\d]+)/$', login_required(views.toggle_like), name="toggle_like")
]
