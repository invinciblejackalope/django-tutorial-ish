from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Post
from .forms import PostForm

# the generic ListView automatically renders poster/post_list.html with the
# output of get_queryset as a variable called post_list
class IndexView(generic.ListView):
    def get_queryset(self):
        '''
        return the latest 20 posts
        '''
        return Post.objects.all().order_by('-timestamp')[:20]

# this is the basic structure for rendering and processing forms: most other
# pages are a variation on this (to avoid repetitiveness, comments explaining
# form code will be omitted for other pages)
def new(request):
    # if this is a POST request, process form data
    if request.method == 'POST':
        # stick the data into a form object
        form = PostForm(request.POST)
        # check whether it's valid
        if form.is_valid():
            # the data is now in form.cleaned_data
            # create new Post object with given data (and save, of course)
            p = Post(text=form.cleaned_data['text'], author=form.cleaned_data \
            ['author'], timestamp=timezone.now(), mod_time=timezone.now())
            p.save()
            # redirect to index when done
            return HttpResponseRedirect(reverse('poster:index'))
    # if a GET (or any other method) create a blank form
    else:
        form = PostForm()
    # render the page (the third parameter is a dict of variable definitions;
    # for example form replaces the {{ form }} variable in form_page.html)
    # reverse takes the name of a page and outputs its URL; avoids hard-coding
    # URLs
    return render(request, 'poster/form_page.html', \
        {'form': form, 'page': reverse('poster:new'), 'action': 'Post', \
        'index': reverse('poster:index'), 'title': 'New post'})


# the generic DetailView automatically renders poster/post_detail.html with
# the Post object in get_queryset whose id matches pk as a variable called post
class PostView(generic.DetailView):
    model = Post

    # get_context_data allows me to make variable definitions, like the third
    # parameter for render above
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm()
        return context

    def get_queryset(self):
        '''
        search in the list of posts
        '''
        return Post.objects.all()

    # go here if it's a post request
    def post(self, request, pk):
        # get the desired Post object
        p = Post.objects.get(id=pk)

        form = PostForm(request.POST)
        if form.is_valid():
            # change the attributes of the Post object
            p.text = form.cleaned_data['text']
            p.author = form.cleaned_data['author']
            p.mod_time = timezone.now()
            p.save()
            # redirect to index
            return HttpResponseRedirect(reverse('poster:index'))


# I wish I could've done this with a DELETE request but apparently HTML forms
# only support GET and POST
def delete(request, pk):
    if request.method == 'POST':
        p = Post.objects.get(id=pk)
        # pretty straightforward
        p.delete()
    # redirect to index
    return HttpResponseRedirect(reverse('poster:index'))
