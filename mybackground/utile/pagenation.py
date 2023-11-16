from django.utils.safestring import mark_safe

class pagenation(object):

    def __init__(self, request, queryset, page_size=10, page_param="page",plus =3):
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(request.GET.get(page_param, "1"))
        else:
            page = 1

        self.page = page
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        # 计算数据条数
        total_count = queryset.count()
        # 总页码

        total_page, div = divmod(total_count, page_size)
        if div:
            total_page += 1
        self.total_page = total_page
        self.plus=plus

    def html(self):
        # 显示总共的前三页与后三页
        if self.total_page <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page

        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus
            else:
                if (self.page + self.plus )> self.total_page:
                    start_page = self.total_page - 2 * self.plus
                    end_page = self.total_page
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        start = (self.page - 1) * self.page_size
        end = self.page * self.page_size

        page_str_list = []
        page_str_list.append('<li ><a href="?page=1">首页</a></li>')
        # 上一页
        if self.page > 1:
            prev = ' <li ><a href="?page={}">{}</a></li>'.format(self.page - 1, '上一页')
            page_str_list.append(prev)
        else:
            prev = ' <li ><a href="?page={}">{}</a></li>'.format(self.page, '上一页')
            page_str_list.append(prev)

        for i in range(start_page, end_page + 1):
            if i == self.page:
                ele = ' <li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
            else:
                ele = ' <li><a href="?page={}">{}</a></li>'.format(i, i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page:
            nell = ' <li ><a href="?page={}">{}</a></li>'.format(self.page + 1, '下一页')
            page_str_list.append(nell)
        else:
            nell = ' <li ><a href="?page={}">{}</a></li>'.format(self.page, '下一页')
            page_str_list.append(nell)

        page_str_list.append('<li ><a href="?page={}">尾页</a></li>'.format(self.total_page))
        search_string = '''

           '''
        page_str_list.append(search_string)
        page_string = mark_safe(''.join(page_str_list))
        return page_string