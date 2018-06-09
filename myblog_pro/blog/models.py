from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.AutoField(primary_key=True)  # 用户id
    username = models.CharField(max_length=20, unique=True, null=False)  # 用户名
    password = models.CharField(max_length=256, null=False)  # 密码
    email = models.CharField(max_length=64, unique=True, null=False)  # 邮箱
    sex = models.BooleanField(default=True)  # 性别，False 为女
    icon = models.ImageField(upload_to='icons', null=True)  # 头像
    brief = models.TextField(null=True)  # 自我简介
    is_delete = models.BooleanField(default=False)  # 是否删除
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间

    class Meta:
        db_table = 't_user'


class UserTicket(models.Model):
    id = models.AutoField(primary_key=True)  # id
    user = models.ForeignKey(User)  # 关联用户
    token = models.CharField(max_length=36, null=False)  # 用户登录口令
    out_time = models.DateTimeField()  # 过期时间

    class Meta:
        db_table = 't_user_ticket'


class Type(models.Model):
    """文章类型"""
    type_id = models.AutoField(primary_key=True)  # 文章类型id
    type_name = models.CharField(max_length=16, null=False)  # 文章类型name
    is_use = models.BooleanField(default=True)  # 是否启用
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_time = models.DateTimeField(auto_now=True)  # 修改时间
    parent = models.ForeignKey('self', null=True, blank=True)  # 父分类，自关联

    class Meta:
        db_table = 't_type'  # 表名


class Banner(models.Model):
    id = models.AutoField(primary_key=True)  # id
    img = models.ImageField(upload_to='banner')  # 图片路径
    img_info = models.CharField(max_length=40)  # 图片描述
    target_url = models.CharField(max_length=64)  # 图片目标url
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    is_delete = models.BooleanField(default=False)  # 是否删除

    class Meta:
        db_table = 't_banner'


class Tag(models.Model):
    """文章标签"""
    tag_id = models.AutoField(primary_key=True)  # 标签id
    tag_name = models.CharField(max_length=16, null=False)  # 标签名
    is_use = models.BooleanField(default=True)  # 是否启用
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_time = models.DateTimeField(auto_now=True)  # 修改时间

    class Meta:
        db_table = 't_tag'  # 表名


class Article(models.Model):
    """文章"""
    id = models.AutoField(primary_key=True)  # 文章id
    title = models.CharField(max_length=40, null=False)  # 文章标题
    brief = models.CharField(max_length=200, null=False)  # 文章简介
    content = models.TextField(null=False)  # 文章内容
    cover = models.ImageField(upload_to='cover', null=True)  # 文章封面
    view_times = models.IntegerField(default=0)  # 查看次数
    praise_times = models.IntegerField(default=0)  # 点赞次数
    is_delete = models.BooleanField(default=False)  # 是否删除
    is_recommend = models.BooleanField(default=False)  # 是否上推荐榜
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_time = models.DateTimeField(auto_now=True)  # 修改时间
    type = models.ForeignKey(Type)  # 文章类型
    author = models.ForeignKey(User)  # 作者

    class Meta:
        db_table = 't_article'  # 表名


class ArticleTags(models.Model):
    """文章-标签-关联中间类"""
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article)
    tag = models.ForeignKey(Tag)

    class Meta:
        db_table = 't_article_tag'


class Comment(models.Model):
    """文章评论"""
    id = models.AutoField(primary_key=True)  # id
    visitor_name = models.CharField(max_length=20, null=False)  # 评论用户名
    visitor_email = models.CharField(max_length=64, unique=True, null=False)  # 评论用户邮箱
    content = models.CharField(max_length=400, null=False)  # 评论内容
    is_delete = models.BooleanField(default=False)  # 是否删除
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    article = models.ForeignKey(Article)  # 关联文章

    class Meta:
        db_table = 't_comment'


class Link(models.Model):
    id = models.AutoField(primary_key=True)
    link_name = models.CharField(max_length=20, null=False)
    link_url = models.CharField(max_length=100, null=False)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 't_link'
