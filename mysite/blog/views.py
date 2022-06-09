from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .froms import EmailPostForm

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# 处理视图的表单 p37
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')

    if request.method == 'POST':     # 是POST请求，就是提交表单
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # 表单字段验证
            cd = form.cleaned_data
            # 发送邮件
    else:                            # 不是POST 而是 GET， 就生产一个新的表单
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form})

# 设置邮件发送 https://juejin.cn/post/6844904030729142285
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import HttpResponse

def check_email(request):
    # 邮件主题
    subject = '请注意这是Django邮件测试'
    message = '测试django发送邮箱'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['657832009@qq.com'] # 注意这是列表
    send_mail(subject=subject,
               from_email=from_email,
               recipient_list=recipient_list,
               message=message)
    return HttpResponse('测试邮件已发出请注意查收')