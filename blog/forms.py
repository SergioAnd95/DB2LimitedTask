from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from .models import Post, Comment

class PostSearchForm(forms.Form):
    country = forms.CharField(widget=forms.TextInput(attrs={"placeholder": _('Country')}), required=False)
    city = forms.CharField(widget=forms.TextInput(attrs={"placeholder": _('City')}), required=False)
    keyword = forms.CharField(widget=forms.TextInput(attrs={"placeholder": _('Search text')}), required=False)

    def search(self, base_qs=None):
        posts = base_qs if base_qs else Post.objects.all()
        print(posts)
        if self.is_valid():
            if self.cleaned_data.get("country"):
                posts = posts.filter(author__country__iexact=self.cleaned_data['country'])

            if self.cleaned_data.get("city"):
                posts = posts.filter(author__city__iexact=self.cleaned_data['city'])

            if self.cleaned_data.get("keyword"):
                kw = self.cleaned_data['keyword']
                posts = posts.filter(Q(title__icontains=kw) | Q(preview_text__icontains=kw) | Q(body__icontains=kw))

        return posts.prefetch_related('likes', 'comments')


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author', )


class CreateCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body', )