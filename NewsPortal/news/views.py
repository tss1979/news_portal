from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import Post, PostCategory
from .filters import PostFilter
from .forms import PostForm


# Create your views here.
class PostsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


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


def create_post(request):
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


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = '/news'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = '/news'
