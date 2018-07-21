from django.db import models

# Create your models here.


class Authority(models.Model):
    """权限"""
    name = models.CharField(max_length=20, null=False)
    adid = models.IntegerField(null=False)

    parent = models.ForeignKey('self', null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'authority'


class Role(models.Model):
    """角色"""
    name = models.CharField(max_length=20, null=False)
    description = models.CharField(max_length=64, null=True)
    adid = models.IntegerField(null=False)

    auths = models.ManyToManyField(Authority)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'role'


class Admin(models.Model):
    """管理员"""
    username = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=256, null=False)
    avatar = models.CharField(max_length=200, null=True)
    gender = models.BooleanField(default=True)
    phone = models.CharField(max_length=12, null=False)
    email = models.CharField(max_length=64, null=True)

    role = models.ForeignKey(Role)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin'

    def to_simple_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'avatar': self.avatar,
            'create_time': self.create_time
        }


class User(models.Model):
    """用户"""
    username = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=256, null=False)
    avatar = models.CharField(max_length=200, null=True)
    gender = models.BooleanField(default=True)
    phone = models.CharField(max_length=12, null=False)
    email = models.CharField(max_length=64, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'

    def to_simple_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'avatar': self.avatar,
            'create_time': self.create_time
        }


class LoginRecord(models.Model):
    """登录记录"""
    login_ip = models.CharField(max_length=24, null=False)
    login_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True)
    admin = models.ForeignKey(Admin, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'login_record'


# class PetPic(models.Model):
#     pic = models.CharField(max_length=200, null=False)
#     location = models.CharField(max_length=64, null=False)
#     user = models.ForeignKey(User)
#     create_time = models.DateTimeField(auto_now_add=True)
#     update_time = models.DateTimeField(auto_now=True)
#
#
# class Comment(models.Model):

class Type(models.Model):
    """文章类型"""
    name = models.CharField(max_length=20, null=False)

    parent = models.ForeignKey('self', null=True)
    admin = models.ForeignKey(Admin, null=False)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'type'


class Article(models.Model):
    """文章"""
    title = models.CharField(max_length=100, null=False)
    cover = models.CharField(max_length=200, null=False)
    content = models.TextField(null=False)

    t = models.ForeignKey(Type, null=False)
    user = models.ForeignKey(User, null=False)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'article'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'cover': self.cover if self.cover else '',
            'content': self.content,
            'type': self.t.name,
            'user': self.user.to_simple_dict(),
            'create_time': self.create_time
        }


class Baike(models.Model):
    """百科"""
    # basic info
    name = models.CharField(max_length=40, null=False)
    name_en = models.CharField(max_length=64, null=False)
    other_name = models.CharField(max_length=64, null=False)
    cover = models.CharField(max_length=200, null=False)
    shapes = models.CharField(max_length=16, null=False)
    ages = models.CharField(max_length=16, null=False)
    fci_group = models.CharField(max_length=40, null=False)
    akc_group = models.CharField(max_length=40, null=False)

    # relation info
    history = models.TextField(null=False)
    character = models.TextField(null=False)
    suit_person = models.TextField(null=False)
    suit_environment = models.TextField(null=False)
    hair_color = models.TextField(null=False)
    disease = models.TextField(null=False)
    tags = models.CharField(max_length=100, null=False)

    admin = models.ForeignKey(Admin, null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'baike'

    def to_dict(self):
        return {
            'id': self.id,
            'name':self.name,
            'name_en': self.name_en,
            'other_name': self.other_name,
            'cover': self.cover,
            'shapes': self.shapes,
            'ages': self.ages,
            'fci_group': self.fci_group,
            'akc_group': self.akc_group,

            'history': self.history,
            'character': self.character,
            'suit_person': self.suit_person,
            'suit_environment': self.suit_environment,
            'hair_color': self.hair_color,
            'disease': self.disease,
            'tags': self.tags,

            'admin': self.admin.to_simple_dict(),
            'create_time': self.create_time
        }


class Question(models.Model):
    """问题"""
    question = models.CharField(max_length=200, null=False)
    subtitle = models.TextField(null=True)

    user = models.ForeignKey(User, null=False)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'question'

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'subtitle': self.subtitle,
            'user': self.user.to_simple_dict(),
            'answers': [ans.to_dict() for ans in self.answer_set.all()],
            'create_time': self.create_time
        }


class Answer(models.Model):
    """答案"""
    content = models.TextField(null=False)

    question = models.ForeignKey(Question, null=False)
    user = models.ForeignKey(User, null=False)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'answer'

    def to_dict(self):
        return {
            'content': self.content,
            'qid': self.question.id,
            'user': self.user.to_simple_dict(),
            'create_time': self.create_time
        }


class Topic(models.Model):
    """专题"""
    title = models.CharField(max_length=64, null=False)
    content = models.TextField(null=False)

    user = models.ForeignKey(User, null=False)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'topic'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'pics': [tp.to_dict() for tp in self.topicpic_set.all()],
            'user': self.user.to_simple_dict(),
            'create_time': self.create_time
        }


class TopicPic(models.Model):
    """专题的图片"""
    pic = models.CharField(max_length=200, null=False)

    topic = models.ForeignKey(Topic, null=False)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'topic_pic'

    def to_dict(self):
        return {
            'id': self.id,
            'pic': self.pic,
            'tid': self.topic.id,
            'create_time': self.create_time
        }
