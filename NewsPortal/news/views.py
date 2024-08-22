import pytz
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, View
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, PostCategory, BaseRegisterForm, Category, Author
from .filters import PostFilter
from .forms import PostForm, SubscribeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.core.cache import cache
from django.utils import timezone


# Create your views here.
class PostsList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context


class PostsListSearch(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts_filter.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'product-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)
        return obj


def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            for el in dict(request.POST)['category']:
                cat = Category.objects.get(pk=el)
                cat.user.add(request.user)
            return HttpResponseRedirect('/news')
    form = SubscribeForm()
    return render(request, 'subscribe.html', {'form': form})


def create_post(request):
    if request.user.groups.filter(name='authors').exists():
        if request.method == 'POST':
            form = PostForm(request.POST)
            url = str(request.path.split('/')[2])
            if form.is_valid():
                instance = form.save(commit=False)
                if url == 'articles':
                    instance.post_kind = 'A'
                elif url == 'news':
                    instance.post_kind = 'N'
                instance.save()
                for el in dict(request.POST)['category']:
                    cat = PostCategory.objects.create(category_id=el, post_id=Post.objects.last().pk)
                    cat.save()
                return HttpResponseRedirect('/news')
        form = PostForm()
        return render(request, 'post_edit.html', {'form': form})
    else:
        return HttpResponseRedirect('/news')


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = '/news'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = '/news'


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
        author = Author.objects.create(user=user)
        author.save()
    return redirect('/news')


def set_timezone(request):
    if request.method == "POST":
        request.session["django_timezone"] = request.POST["timezone"]
        return redirect("/news")
    else:
        return render(request, "/news")


