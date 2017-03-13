from django.shortcuts import render


def livelog(request):
    return render(request, 'blog.html')
