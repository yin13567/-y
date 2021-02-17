from django.db import models

# Create your models here.
class User(models.Model):
    '''用户信息表'''

    gender=(
        ('male','男'),
        ('female', '女'),
    )

    name=models.CharField(max_length=128)
    password=models.CharField(max_length=256)
    idnum=models.CharField(max_length=32)
    phonenum=models.CharField(max_length=32,null=True)
    email=models.EmailField(unique=True)
    sex=models.CharField(max_length=32,choices=gender,default='男')
    c_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering=['c_time']
        verbose_name='用户信息'
        verbose_name_plural='用户信息'