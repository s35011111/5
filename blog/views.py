from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):

        queryset = Post.objects.filter(published=True)



        # Filter by search query if provided
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )

        # Ordering - default by newest first
        ordering = self.request.GET.get('ordering', '-created_at')
        if ordering == 'views':
            queryset = queryset.order_by('-view_count')
        elif ordering == 'title':
            queryset = queryset.order_by('title')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_ordering'] = self.request.GET.get('ordering', '-created_at')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'#
    context_object_name = 'post'

    def get_queryset(self):
        # Only allow viewing published posts or posts by the author
        if self.request.user.is_authenticated:
            return Post.objects.filter(
                Q(published=True) | Q(author=self.request.user)
            )
        return Post.objects.filter(published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get(self, request, *args, **kwargs):
        # Increment view count when someone views the post
        response = super().get(request, *args, **kwargs)
        self.object.increment_view_count()
        return response


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content',  'published']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'published']

    def get_queryset(self):
        # Only allow authors to edit their own posts
        return Post.objects.filter(author=self.request.user)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/blog/'

    def get_queryset(self):
        # Only allow authors to delete their own posts
        return Post.objects.filter(author=self.request.user)


