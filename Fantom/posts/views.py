from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

from .models import Post, Category, Tag
from .forms import *


class IndexView(ListView):
    template_name = 'posts/index.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['slider_posts'] = Post.objects.all().filter(slider_post=True)
        return context


class PostDetail(DetailView, FormMixin):
    template_name = 'posts/detail.html'
    model = Post
    context_object_name = 'single'
    form_class = CreateCommentForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # self.hit = Post.objects.filter(id=self.kwargs['pk']).update(hit=F('hit')+1)
        self.hit = Post.objects.filter(id=self.kwargs['pk']).update(hit=self.object.hit + 1)
        return super(PostDetail, self).get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['previous'] = Post.objects.filter(id__lt=self.kwargs['pk']).order_by('-pk').first()
        context['next'] = Post.objects.filter(id__gt=self.kwargs['pk']).order_by('pk').first()
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        self.object = self.get_object()
        if form.is_valid():
            form.instance.posts = self.object
            form.save()
            return super(PostDetail, self).form_valid(form)
        else:
            return super(PostDetail, self).form_invalid(form)

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_valid(form)

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})


class CategoryDetail(ListView):
    model = Post
    template_name = 'categories/category_detail.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Post.objects.filter(category=self.category).order_by('-id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['pk'])
        return context


class TagDetail(ListView):
    model = Tag
    template_name = 'tags/tag_detail.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(tag=tag).order_by('id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TagDetail, self).get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])

        return context


@method_decorator(login_required(login_url='users/login'), name='dispatch')
class PostCreationView(CreateView):
    model = Post
    form_class = PostCreationForm
    template_name = 'posts/create-post.html'

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})

    def form_valid(self, form):
        ## in the creation sefl.kwargs is empty so you must use self.object.fieldname
        form.instance.user = self.request.user
        form.save()

        tags = self.request.POST.get('tag').split(",")
        for tag in tags:
            current_tag = Tag.objects.filter(slug=slugify(tag))
            if current_tag.count() < 1:
                create_tag = Tag.objects.create(title=tag)
                form.instance.tag.add(create_tag)
            else:
                existed_tag = Tag.objects.get(slug=slugify(tag))
                form.instance.tag.add(existed_tag)
        return super(PostCreationView, self).form_valid(form)


@method_decorator(login_required(login_url='users/login'), name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'posts/update-post.html'

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.tag.clear()

        tags = self.request.POST.get('tag').split(",")
        for tag in tags:
            current_tag = Tag.objects.filter(slug=slugify(tag))
            if current_tag.count() < 1:
                create_tag = Tag.objects.create(tag)
                form.instance.tag.add(create_tag)
            else:
                existed_tag = Tag.objects.get(slug=slugify(tag))
                form.instance.tag.add(existed_tag)
        form.save()
        return super(PostUpdateView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != self.request.user:
            return HttpResponseRedirect('/')
        return super(PostUpdateView, self).get(request, *args, **kwargs)


class DeletePostView(DeleteView):
    model = Post
    success_url = '/'
    template_name = 'posts/delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect(self.success_url)
        return super(DeletePostView, self).get(request, *args, **kwargs)


class SearchView(ListView):
    model = Post
    template_name = 'posts/search.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(Q(title__icontains=query) |
                                       Q(content__icontains=query) |
                                       Q(tag__title__icontains=query)
                                       ).order_by('id').distinct()
        return Post.objects.all().order_by('id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query

        return context
