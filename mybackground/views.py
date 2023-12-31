from django.shortcuts import render

# Create your views here.
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.db.models import Avg, Max, Min, Count, Q
from django.shortcuts import render, redirect, HttpResponse
from mybackground import models
from mybackground.utile.pagenation import pagenation
from django.http import JsonResponse


# 定义所需要的表单样式
class loginform(forms.Form):
    user_name = forms.CharField(
        label='用户名',
        widget=forms.TextInput
    )
    user_password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 初始化父类方法
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', "placeholder": field.label}


class playerForms(forms.ModelForm):
    class Meta:
        # 首先说明这一表单的model是以Django中的Student类为基础
        model = models.Player
        fields = ["player_id", "name", "password", "play_time", "played_round", "max_score", "number_of_cooperation"]

    # 定义这一提交表单在前端显示时的样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 初始化父类方法
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', "placeholder": field.label}


class rankForms(forms.ModelForm):
    class Meta:
        model = models.RankRecord
        fields = ['record_id', 'player', 'score', 'upload_time', 'team']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 初始化父类方法
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', "placeholder": field.label}


# 该页面专门设置为管理员登录页面
def login(request):
    if request.method == "GET":
        form = loginform()  # 生成传到前端的需要填写的表单信息
        return render(request, "login.html", {'form': form})
    form = loginform(data=request.POST)  # 获得前端传入的数据
    user_name = request.POST.get('user_name')
    user_password = request.POST.get('user_password')

    # 将前端传入的数据与数据库中存在的个人信息进行比对，判断是否能登录
    if form.is_valid():
        admin_object = models.Admin.objects.filter(admin_name=user_name, admin_password=user_password).first()
        if not admin_object:
            form.add_error('user_password', '用户名或密码错误')
            return render(request, "login.html", {'form': form})
        request.session['info'] = {'id': user_name, 'password': user_password, 'name': admin_object.admin_name}
        return redirect('/admin/')


# 该页面专门设置为管理员注销页面
def logout(request):
    request.session.clear()
    return redirect('/login/')


def admin(request):  ### 管理员信息展示
    # 先创建一个字典
    data_list = {}
    # 然后通过得到前端传入的‘s'标签中的内容得到用户想要的搜索功能，如果用户不搜索则默认为空
    value = request.GET.get('s', '')
    # 如果用户有搜索内容则在字典中传入学生id的搜索值
    if value:
        data_list['admin_id__contains'] = value
    # 之后通过Django的models模块搜索id得到管理员列表，其中包含有全部的管理员信息
    queryset1 = models.Admin.objects.filter(**data_list).order_by('admin_id')
    # paganation是自行封装好的分页函数用于分页
    page_object = pagenation(request, queryset1)
    # 使用分页函数得到每一页需要显示的管理员内容admin_list有多少条以及下端的页面跳转按钮page_string
    admin_list = page_object.page_queryset
    page_string = page_object.html()

    # 之后将所有的这些内容打包成一个字典context传入前端页面进行渲染
    context = {"admin_list": admin_list, "data": value, "page": page_string}

    return render(request, 'admin.html', context)


def player_message(request):
    data_list = {}
    # name = 's'的标签代表前端传入的搜索内容，用户搜索想对应的玩家编号
    value = request.GET.get('s', '')
    if value:
        data_list['player_id__contains'] = value
    queryset_a = models.Player.objects.filter(**data_list).order_by('player_id')
    page_object = pagenation(request, queryset_a)
    player_list = page_object.page_queryset
    page_string = page_object.html()

    context = {"player_list": player_list, "data": value, "page": page_string}

    return render(request, 'player.html', context)


# 定义玩家的添加方法
def player_add(request):
    form = playerForms()

    if request.method == "GET":
        return render(request, 'player_add.html', {"form": form})
    # 使用POST方法提交数据,进行数据校验

    adding_form = playerForms(data=request.POST)
    if adding_form.is_valid():
        adding_form.save()  # 保存到数据库里面
        return redirect('/player/')
    else:
        return render(request, 'player_add.html', {"form": adding_form})


def player_edit(request, pid):
    if request.method == 'GET':
        row_object = models.Player.objects.filter(player_id=pid).first()
        form = playerForms(instance=row_object)
        return render(request, 'player_edit.html', {"form": form})

    row_object = models.Player.objects.filter(player_id=pid).first()
    form = playerForms(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/player/')

    return render(request, 'player_edit.html', {"form": form})


def player_delete(request, pid):
    models.Player.objects.filter(player_id=pid).delete()
    return redirect('/player/')


def record_rank(request):
    data_list = {}
    # name = 's'的标签代表前端传入的搜索内容，用户搜索想对应的排行榜记录号
    value = request.GET.get('s', '')
    if value:
        data_list['record_id__contains'] = value
    queryset_a = models.RankRecord.objects.filter(**data_list).order_by('record_id')
    page_object = pagenation(request, queryset_a)
    record_list = page_object.page_queryset
    page_string = page_object.html()

    context = {"record_list": record_list, "data": value, "page": page_string}

    return render(request, 'rank.html', context)


def record_edit(request, rid):
    if request.method == 'GET':
        row_object = models.RankRecord.objects.filter(record_id=rid).first()
        form = rankForms(instance=row_object)
        return render(request, 'rank_edit.html', {"form": form})

    row_object = models.RankRecord.objects.filter(record_id=rid).first()
    form = rankForms(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/record/')

    return render(request, 'rank_edit.html', {"form": form})


def record_delete(request, rid):
    models.RankRecord.objects.filter(record_id=rid).delete()
    return redirect('/record/')


def record_analysis(request):
    # 查询榜单成绩的最高分、最低分、平均分
    score_list = models.RankRecord.objects.all()

    # 聚合查询得到相关课程的最高、最低分和平均分
    avg = models.RankRecord.objects.all().aggregate(Avg('score'))
    max = models.RankRecord.objects.all().aggregate(Max('score'))
    min = models.RankRecord.objects.all().aggregate(Min('score'))

    # 将需要的数据打包成字典传入前端页面展示
    context = {'avg': avg, 'min': min, 'max': max, 'score_list': score_list}

    return render(request, 'record_analysis.html', context)


def record_chart(request):
    # 生成榜单的图表
    # 使用聚合函数多条件查询得到每个分数区间段的人数并附在字典之中
    count_1 = models.RankRecord.objects.filter(Q(score__lt=0)).count()
    search_list = []
    tem_1 = {}
    tem_1['name'] = '分数小于0'
    tem_1['value'] = count_1
    search_list.append(tem_1)
    count = models.RankRecord.objects.filter(Q(score__lt=100) & Q(score__gte=0)).count()
    tem_2 = {}
    tem_2['name'] = '分数在0-100区间'
    tem_2['value'] = count
    search_list.append(tem_2)
    count = models.RankRecord.objects.filter(Q(score__lt=1000) & Q(score__gte=100)).count()
    tem_3 = {}
    tem_3['name'] = '分数在100-1000区间'
    tem_3['value'] = count
    search_list.append(tem_3)
    count = models.RankRecord.objects.filter(Q(score__gte=1000)).count()
    tem_4 = {}
    tem_4['name'] = '分数大于1000'
    tem_4['value'] = count
    search_list.append(tem_4)

    # 之后将字典打包好传入前端渲染
    result = {
        "status": True,
        "data": search_list

    }
    # 回应前端的Ajax请求发送成绩分析内容
    return JsonResponse(result)
