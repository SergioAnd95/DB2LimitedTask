from django.views.generic import DetailView, FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse

from .models import Post, Comment
from .forms import CreateCommentForm, CreatePostForm
# Create your views here.


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    comment_paginte_by = 10

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)

        paginator = Paginator(self.object.comments.all(), self.comment_paginte_by)

        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        ctx['comments'] = comments
        ctx['comment_form'] = CreateCommentForm
        return ctx


class AjaxCreateCommentFormView(FormView):
    model = Comment
    form_class = CreateCommentForm

    def get(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=kwargs.get('pk'))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=kwargs.get('pk'))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.post
        comment.author = self.request.user
        comment.save()

        return JsonResponse({'status': 'ok', 'redirect_url': self.post.get_absolute_url()})

    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'errors': form.errors})


class CreatePostFormView(FormView):
    form_class = CreatePostForm
    template_name = 'blog/post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()

        return redirect(post.get_absolute_url())


def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not post.user_like_exist(request.user):
        post.likes.create(user=request.user)
        liked=True
    else:
        post.likes.filter(user=request.user).delete()
        liked=False

    return JsonResponse({'likes_count':post.likes.count(), 'status': 'ok', 'liked':liked})