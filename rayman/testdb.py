# -*- coding: utf-8 -*-

from django.http import HttpResponse

from dbUsersModel.models import userInfo
import time
from django.shortcuts import render

# 添加
def addToDB(request):
	dateTime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	user = userInfo(name='mmmmm', birthday=dateTime)
	print(user.name)
	user.save()
	return HttpResponse("<p>数据添加成功！</p>")


# 添加
def addToDBForm(request):

	if request.method == "POST":
		# context = {}
		name = request.POST.get("name")
		birthday = request.POST.get("birthday")

		user = userInfo()
		user.name = name
		# user.birthday = birthday


		user.user_pass = request.POST.get("user_pass")
		user.user_roleID = request.POST.get("user_roleID")
		user.user_grade = request.POST.get("user_grade")
		user.user_class = request.POST.get("user_class")
		user.user_gender = request.POST.get("user_gender")


		# ok = user.save()
		user.save()
		# if(ok):
		# 	context['isOK'] = True
		# else:
		# 	context['isOK'] = False
		return render(request,'search_form.html')
	else:
		return render(request,'addUserPost.html')


def queryFromDB(request):
	response = ""
	list = userInfo.objects.all()
	# 输出所有数据


	# filter相当于SQL中的WHERE，可设置条件过滤结果
	# response2 = userInfo.objects.filter(id=1) 
	# 获取单个对象
	# response3 = userInfo.objects.get(id=1) 
	# 限制返回的数据 相当于 SQL 中的 OFFSET 0 LIMIT 2;
	# userInfo.objects.order_by('name')[0:2]
	#数据排序
	# userInfo.objects.order_by("id")
	# 上面的方法可以连锁使用
	# userInfo.objects.filter(name="w3cschool.cn").order_by("id")


	# response +="<ul>"
	# for person in list:
	# 	# response += "<li>" + person.name + " " + str(person.birthday) + "</li>"
	# 	response += "<li>"
	# 	response += person.name + " "
	# 	# response += str(person.birthday) + " "
	# 	response += str(person.user_roleID) + " "

	# 	response += person.user_class + " "
	# 	response += person.user_grade + " "
	# 	response += str(person.user_gender) + " "

	# 	response += "</li>"

	# response +="</ul>"

	context = {}
	context['resultList'] = list

	
	# return HttpResponse("<p>"+ response +"</p>")

	return render(request,'search_result.html', context)

def updateToDB(request):

	# 修改其中一个id=1的name字段，再save，相当于SQL中的UPDATE
	user = userInfo.objects.get(id=1)
	user.name = 'hhhhh'
	user.save()
	
	# 另外一种方式
	#userInfo.objects.filter(id=1).update(name='hhhhhhh')
	
	# 修改所有的列
	# userInfo.objects.all().update(name='hhhhhh')
	
	return HttpResponse("<p>修改成功</p>")

def deleteToDB(request):
	# 删除id=1的数据
	user = userInfo.objects.get(id=3)
	user.delete()

	# 另外一种方式
	# userInfo.objects.filter(id=1).delete()

	# 删除所有数据
	# userInfo.objects.all().delete()

	return HttpResponse("<p>删除成功</p>")