from email import message
from re import A
from django.shortcuts import render, redirect
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.contrib import messages

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)

def create(request):
    form = ArticleForm()
    if request.method == "POST":
        aform = ArticleForm(request.POST, request.FILES)
        if aform.is_valid():
            aform = aform.save(commit=False)
            aform.user = request.user
            aform.save()
            messages.success(request, '글 작성이 완료되었습니다.')
            return redirect('articles:index')
        else:
            form = ArticleForm()
    context = {
        "form" : form,
    }

    return render(request, 'articles/create.html', context)

def detail(request, pk):
    article = Article.objects.get(pk=pk)
    comment = CommentForm()
    context ={
        'article' : article,
        'comment': comment,
        'comments': article.comment_set.all(),
    }
    return render(request, 'articles/detail.html', context)

def update(request, pk):
    article = Article.objects.get(pk=pk)
    form = ArticleForm(instance=article)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance= article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article.pk)
    context = {
        'form' : form, 
    }
    return render(request, 'articles/update.html', context)

def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('articles:index')

def comment(request, pk):
    article = Article.objects.get(pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.user = request.user
        messages.success(request, '댓글을 달았다.')
        comment.save()
    return redirect('articles:detail', article.pk)

def comments_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
        messages.success(request, '댓글을 삭제했다.')
    return redirect('articles:detail', article_pk)

def search(request):
    return render(request, 'articles/search.html')


def comments_update (request,article_pk, comment_pk):
    pick_comment = Comment.objects.get(pk=comment_pk)
    pick_article = Article.objects.get(pk=article_pk)
    if request.method == 'POST':
        C_Form = CommentForm(request.POST, instance=pick_comment )
        if C_Form.is_valid():
            a = C_Form (commit=False)
            a.article = pick_article    
            a.save()
            return redirect ("articles:index")
    return render(request,"articles/detail.html" ,)