from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect


class c1(MiddlewareMixin):

    def process_request(self,request):
        #排除不需要检测的页面
        if request.path_info == '/login/': #如果用户当前访问的页面为登录页面,直接让用户进入不需要检测
            return
        if request.path_info == '/logout/':
            return

        #读取当前访问的session信息,如果能读到说明用户已登录
        get_dict= request.session.get('info')
        if get_dict:
            return
        else:
            return redirect('/login/')

    def process_response(self,request,response):

        return response