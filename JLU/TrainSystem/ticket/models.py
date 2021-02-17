from django.db import models


# Create your models here.
from userinfo.models import User


class Station(models.Model):
    """所有的车站"""
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '车站的信息'
        verbose_name_plural = '车站的信息'


class TrainLine(models.Model):
    """车次信息"""
    trainnum = models.CharField(max_length=16)  # 车次号
    startplace = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="linestartplace")
    starttime = models.DateTimeField()
    endplace = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="lineendplace")
    endtime = models.DateTimeField()

    def __str__(self):
        return self.trainnum

    class Meta:
        verbose_name = '路线的信息'
        verbose_name_plural = '路线的信息'


class TicketKind(models.Model):
    """票的类型"""

    name = models.CharField(max_length=16)  # 类型的名称
    num = models.IntegerField(default=-1)  # 余票,-1表示不存在
    price = models.FloatField(default=0)  # 价格
    startplace = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="kindstartplace")
    startplaceseq = models.IntegerField(default=0)
    endplace = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="kindendplace")
    endplaceseq = models.IntegerField(default=0)
    trainline = models.ForeignKey(TrainLine, on_delete=models.CASCADE, related_name="kindtrainline")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '车票的信息'
        verbose_name_plural = '车票的信息'


class SingleLine(models.Model):
    """每一个车次中的每一段"""
    startplace = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="singlestartplace")
    starttime = models.DateTimeField()
    endplace = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="singleendplace")
    endtime = models.DateTimeField()
    trainline = models.ForeignKey(TrainLine, on_delete=models.CASCADE)
    seq = models.IntegerField()  # 在车次中的序列号

class TicketOrder(models.Model):
    """订票的信息"""
    userid=models.ForeignKey(User,on_delete=models.DateField)
    ticketid=models.ForeignKey(TicketKind,on_delete=models.DateField)
    ctime=models.DateTimeField(auto_now_add=True)