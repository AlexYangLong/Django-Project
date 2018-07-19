from django.db import models

# Create your models here.


# class BaseModel(object):
#     create_time = models.DateTimeField(auto_now_add=True)
#     update_time = models.DateTimeField(auto_now_add=True, auto_now=True)


class Authority(models.Model):
    name = models.CharField(max_length=16, null=False)
    url = models.CharField(max_length=64, null=True)
    parent = models.ForeignKey('self', null=True)
    admin_id = models.IntegerField(null=False)

    class Meta:
        db_table = 'auth'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url if self.url else '',
            'parent': self.parent.to_dict() if self.parent_id else '',
            'admin': Admin.objects.filter(id=self.admin_id).first().to_dict(),
        }

    def to_basic_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
        }

    def to_parent_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'sub_auths': [auth.to_basic_dict() for auth in Authority.objects.filter(parent_id=self.id)],
            'admin': Admin.objects.filter(id=self.admin_id).first().to_dict(),
        }


class Role(models.Model):
    name = models.CharField(max_length=16, null=False)
    aid = models.IntegerField(null=False)
    description = models.CharField(max_length=64, null=True)
    auths = models.ManyToManyField(Authority)

    class Meta:
        db_table = 'role'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }

    def to_auth_info_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'auths': ','.join([str(auth.id) for auth in self.auths.all()])
        }

    def to_full_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'admins': ','.join([admin.name for admin in self.admin_set.all()]),
            'description': self.description,
        }


class Admin(models.Model):
    username = models.CharField(max_length=20, null=False)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=256, null=False)
    gender = models.BooleanField(default=True)
    phone = models.CharField(max_length=12, null=False)
    email = models.CharField(max_length=64, null=False)
    role = models.ForeignKey(Role)

    class Meta:
        db_table = 'admin'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'gender': self.gender,
            'phone': self.phone,
            'email': self.email,
            'role': self.role.to_dict(),
        }


# class RoleAuth(models.Model):
#     role = models.ForeignKey(Role)
#     auth = models.ForeignKey(Authority)
#
#     class Meta:
#         db_table = 'role_auth'
#
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'role': self.role.to_dict(),
#             'auth': self.auth.to_dict()
#         }


class LoginRecord(models.Model):
    login_ip = models.CharField(max_length=24, null=False)
    login_time = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(Admin)

    class Meta:
        db_table = 'login_record'

    def to_dict(self):
        return {
            'id': self.id,
            'login_ip': self.login_ip,
            'admin': self.admin.to_dict(),
        }
