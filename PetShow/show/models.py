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
            'avatar': self.avatar if self.avatar else '',
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
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
            'avatar': self.avatar if self.avatar else '',
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
        }


class Article(models.Model):
    """文章"""
    title = models.CharField(max_length=100, null=False)
    cover = models.CharField(max_length=200, null=False)
    content = models.TextField(null=False)

    t = models.ForeignKey(Type, null=False)
    admin = models.ForeignKey(Admin, null=True)

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
            'type': self.t.to_dict(),
            'admin': self.admin.to_simple_dict(),
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
        }


class Baike(models.Model):
    """百科"""
    # basic info
    name = models.CharField(max_length=40, null=False)
    name_en = models.CharField(max_length=64, null=False)
    other_name = models.CharField(max_length=64, null=False)
    cover = models.CharField(max_length=200, null=True)
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
            'cover': self.cover if self.cover else '',
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
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
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
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
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
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
        }


class Topic(models.Model):
    """专题"""
    title = models.CharField(max_length=64, null=False)
    cover = models.CharField(max_length=200, null=True)
    content = models.TextField(null=False)

    user = models.ForeignKey(User, null=False)

    views = models.IntegerField(default=0)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'topic'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'cover': self.cover if self.cover else '',
            'content': self.content,
            'user': self.user.to_simple_dict(),
            'views': self.views,
            'upvote': self.upvotetopic_set.all().count(),
            'upvote_users': [user.to_simple_dict() for user in self.upvotetopic_set.all()],
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
        }

    def to_full_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'cover': self.cover if self.cover else '',
            'content': self.content,
            'pics': [tp.to_dict() for tp in self.topicpic_set.all()],
            'user': self.user.to_simple_dict(),
            'views': self.views,
            'upvote': self.upvotetopic_set.all().count(),
            'upvote_users': [user.to_simple_dict() for user in self.upvotetopic_set.all()],
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
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
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
        }


class UpvoteTopic(models.Model):
    user = models.ForeignKey(User)
    topic = models.ForeignKey(Topic)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'upvote_topic'


class Pet(models.Model):
    username = models.CharField(max_length=20, null=False)
    avatar = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=16, null=True)
    picture = models.CharField(max_length=200, null=False)
    like_num = models.IntegerField()

    user = models.ForeignKey(User, null=True)

    # t = models.ForeignKey(Type, null=False)
    t = models.CharField(max_length=12, null=False)

    v_second = models.CharField(max_length=4, null=True)
    video = models.CharField(max_length=200, null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pet'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'avatar': self.avatar if self.avatar else '',
            'city': self.city,
            'picture': self.picture,
            'type': self.t,
            'like_num': self.like_num,
            'comment_count': self.petcomment_set.all().count(),
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
        }


class PetDoodle(models.Model):
    avatar = models.CharField(max_length=200, null=True)

    user = models.ForeignKey(User, null=True)
    pet = models.ForeignKey(Pet, null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pet_doodle'

    def to_dict(self):
        return {
            'id': self.id,
            'avatar': self.avatar,
            'doodle_list': [doodle.to_dict() for doodle in self.doodles_set.all()],
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
        }


class Doodles(models.Model):
    angle = models.CharField(max_length=12, null=False)
    center_x = models.CharField(max_length=12, null=False)
    center_y = models.CharField(max_length=12, null=False)
    zoom = models.CharField(max_length=12, null=False)
    picture = models.CharField(max_length=200, null=False)
    is_turn = models.BooleanField(default=False)
    rect_upper_left_x = models.CharField(max_length=12, null=False)
    rect_upper_left_y = models.CharField(max_length=12, null=False)
    rect_width = models.CharField(max_length=12, null=False)
    rect_height = models.CharField(max_length=12, null=False)
    word = models.CharField(max_length=20, null=True)

    pd = models.ForeignKey(PetDoodle, null=False)

    class Meta:
        db_table = 'doodles'

    def to_dict(self):
        return {
            'angle': self.angle,
            'center_x': self.center_x,
            'center_y': self.center_y,
            'zoom': self.zoom,
            'picture': self.picture,
            'is_turn': self.is_turn,
            'rect_upper_left_x': self.rect_upper_left_x,
            'rect_upper_left_y': self.rect_upper_left_y,
            'rect_width': self.rect_width,
            'rect_height': self.rect_height,
            'word': self.word if self.word else ''
        }


class PetComment(models.Model):
    username = models.CharField(max_length=20, null=False)
    avatar = models.CharField(max_length=200, null=False)
    content = models.CharField(max_length=256, null=False)
    city = models.CharField(max_length=16, null=False)

    pet = models.ForeignKey(Pet, null=False)
    user = models.ForeignKey(User, null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pet_comment'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'avatar': self.avatar,
            'content': self.content,
            'city': self.city,
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
        }
