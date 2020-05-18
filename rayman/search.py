# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render

# 表单
def search_form(request):
	context = {}
	return render(request, 'search_form.html', context)
	# return render('search_form.html')

# 接收请求数据
def search(request):
	request.encoding='utf-8'
	if 'q' in request.GET:
		message = '你搜索的内容为: ' + str(request.GET['q'].encode('utf-8'))
	else:
		message = '你提交了空表单'
	return HttpResponse(message)