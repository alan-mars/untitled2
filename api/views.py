import json
from django.shortcuts import render, HttpResponse

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.versioning import QueryParameterVersioning, URLPathVersioning
from rest_framework.parsers import JSONParser, FormParser

from api import models


class VersionView(APIView):
    """
    版本
    """

    # versioning_class = QueryParameterVersioning  # get传参获取版本号, setting默认url获取

    def get(self, request, *args, **kwargs):
        # version = request._request.GET.get('version')
        # version = request.query_params.get('version')

        # 获取版本
        print(request.version)
        # 获取处理版本的对象
        print(request.versioning_scheme)
        # 反向生成url
        print(request.versioning_scheme.reverse(viewname='uu', request=request))

        return HttpResponse('用户列表')


class ParserView(APIView):
    """
    解析器
    """

    # JSONParser表示只能解析Content-Type: application/json的请求头
    # FormParser表示只能解析Content-Type：application/x-www-form-urlencoded的请求头
    # parser_classes = [JSONParser, FormParser, ]

    def post(self, request, *args, **kwargs):

        # 获取请求后的结果
        print(request.data)
        return HttpResponse('parser')


from rest_framework import serializers

class RolesSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    title = serializers.CharField()


class RolesView(APIView):
    """
    序列化
    """

    def get(self, request, *args, **kwargs):

        # 方式一：[{"id": 1, "title": "医生"}, {"id": 2, "title": "老师"}]
        # roles = models.Role.objects.all().values('id', 'title')
        # roles = list(roles)
        # ret = json.dumps(roles, ensure_ascii=False)

        # 方式二：
        roles = models.Role.objects.all()
        ser = RolesSerializer(instance=roles, many=True)
        ret = json.dumps(ser.data, ensure_ascii=False)

        # 对于单个对象
        # role = models.Role.objects.all().first()
        # ser = RolesSerializer(instance=role, many=False)
        # ret = json.dumps(ser.data, ensure_ascii=False)

        return HttpResponse(ret)


class UserInfoSerializer(serializers.Serializer):

    user_type1 = serializers.CharField(source='user_type')
    user_type2 = serializers.CharField(source='get_user_type_display')
    username = serializers.CharField()
    password = serializers.CharField()
    gp = serializers.CharField(source='group.id')

    rl = serializers.SerializerMethodField()
    def get_rl(self, row):

        role_obj_list = row.roles.all()
        ret = []
        for item in role_obj_list:
            ret.append({"id":item.id, "title":item.title})
        return ret


class UserInfoView(APIView):

    def get(self, request, *args, **kwargs):

        # [{"user_type1": "1", "user_type2": "普通用户", "username": "infan", "password": "123", "gp": "1", "rl": [{"id": 2, "title": "老师"}]}, {"user_type1": "2", "user_type2": "vip", "username": "wuyifan", "password": "123", "gp": "1", "rl": [{"id": 1, "title": "医生"}, {"id": 2, "title": "老师"}]}]
        user = models.UserInfo.objects.all()
        ser = UserInfoSerializer(instance=user, many=True)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


class UserInfoSerializer1(serializers.ModelSerializer):

    # oooo = serializers.CharField(source='get_user_type_display')
    # xxxx = serializers.CharField(source='group.title')

    class Meta:
        model = models.UserInfo
        # fields = "__all__"
        # fields = ['id', 'username', 'password', 'oooo', 'xxxx']
        fields = ['id', 'username', 'password', 'user_type', 'group', 'roles']
        depth = 1


class UserInfoView1(APIView):

    def get(self, request, *args, **kwargs):

        # [{"id": 1, "username": "infan", "password": "123", "oooo": "普通用户", "xxxx": "A组"}, {"id": 2, "username": "wuyifan", "password": "123", "oooo": "vip", "xxxx": "A组"}]
        # [{"id": 1, "username": "infan", "password": "123", "user_type": 1, "group": {"id": 1, "title": "A组"}, "roles": [{"id": 2, "title": "老师"}]}, {"id": 2, "username": "wuyifan", "password": "123", "user_type": 2, "group": {"id": 1, "title": "A组"}, "roles": [{"id": 1, "title": "医生"}, {"id": 2, "title": "老师"}]}]
        user = models.UserInfo.objects.all()
        ser = UserInfoSerializer1(instance=user, many=True)
        ret = json.dumps(ser.data, ensure_ascii=False)

        return HttpResponse(ret)


#################################验证####################################

class XXXValid(object):
    """
    自定义认证类
    """

    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        if not value.startswith(self.base):
            message = '内容必须以%s为开头'%self.base
            raise serializers.ValidationError(message)

    def set_context(self, serializer_field):
        pass


class UserGroupSerializer(serializers.Serializer):

    title = serializers.CharField(error_messages={'required': '内容不能为空'},
                                  validators=[XXXValid('老男人'), ])

    def validate_title(self, value):
        """
        自定义认证方法
        :param value:
        :return:
        """
        from rest_framework import exceptions
        raise exceptions.ValidationError('自定义不让你通过')
        # return value


class UserGroupView(APIView):

    def post(self, request, *args, **kwargs):

        ser = UserGroupSerializer(data=request.data)
        if ser.is_valid():
            print(ser.validated_data)
        else:
            print(ser.errors)
        return HttpResponse('提交数据')


from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from api.utils.serializers.pager import PagerSerializer

class MyPageNumberPagination(PageNumberPagination):
    """
    自定义分页，可有可无
    """

    page_size = 5
    page_size_query_param = 'size'
    max_page_size = 10
    page_query_param = 'page'


class MyPageNumberPagination1(LimitOffsetPagination):
    """
    自定义从哪条数据分页
    """

    default_limit = 5
    limit_query_param = 'limit'
    max_limit = 10
    offset_query_param = 'offset'


class MyPageNumberPagination2(CursorPagination):
    """
    加密分页
    """
    cursor_query_param = 'cursor'
    ordering = 'id'
    page_size = 5


class Pager1View(APIView):

    def get(self, request, *args, **kwargs):

        role = models.Role.objects.all()
        pg = MyPageNumberPagination()
        pager_roles = pg.paginate_queryset(queryset=role, request=request, view=self)
        ser = PagerSerializer(instance=pager_roles, many=True)

        #拓展 同时获取前后页url等更多数据(加密分页时如此返回)
        # return pg.get_paginated_response(ser.data)

        return Response(ser.data)


from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

class View1View(GenericViewSet):

    queryset = models.Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):

        roles = self.get_queryset()  # roles = models.Role.objects.all()
        pager_roles = self.paginate_queryset(roles)
        ser = self.get_serializer(instance=pager_roles, many=True)

        return Response(ser.data)


class View2View(ModelViewSet):

    queryset = models.Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = PageNumberPagination


from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

class TestView(APIView):

    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, ]

    def get(self, request, *args, **kwargs):

        role = models.Role.objects.all()
        pg = MyPageNumberPagination()
        pager_roles = pg.paginate_queryset(queryset=role, request=request, view=self)
        ser = PagerSerializer(instance=pager_roles, many=True)

        return Response(ser.data)