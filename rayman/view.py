from django.http import HttpResponse
from django.shortcuts import render


def base(request):
    context = {}
    # return HttpResponse("Hello world !")
    return render(request, 'base.html', context)


def hello(request):
    context = {'hello': 'hi ray', 'gender': True, 'age': 36, 'health': True,
               'companyList': ['yongyou', 'microduino', 'uniwisee']}
    # return HttpResponse("Hello world !")
    return render(request, 'hello.html', context)
