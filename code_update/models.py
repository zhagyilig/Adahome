from django.db import models

# Create your models here.

ASSET_ENV = (
    (1, U'生产环境'),
    (2, U'测试环境')
)


class Minion(models.Model):
    """salt minion"""
    ip = models.GenericIPAddressField()
    saltname = models.CharField(max_length=32, verbose_name=u'salt minion name')

    def __str__(self):
        return self.saltname

    class Meta:
        db_table = 'code_update_minions'
        ordering = ['id']


class ServiceGroup(models.Model):
    """项目组
        ps： detalase； ALS
    """
    name = models.CharField(max_length=32, verbose_name="项目组", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'code_update_servergroup'
        ordering = ['id']


class ServicesName(models.Model):
    """项目名称"""
    ip = models.GenericIPAddressField()
    name = models.CharField(max_length=128, verbose_name=u'项目名字')
    env = models.IntegerField(choices=ASSET_ENV, blank=True, null=True, verbose_name=u"运行环境")
    group = models.ForeignKey(ServiceGroup)
    saltminion = models.ForeignKey(Minion)
    owner = models.CharField(max_length=32)
    comment = models.CharField(max_length=256)
    ports = models.CharField(max_length=128, null=True, verbose_name=u'ports')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'code_update_servicesname'
        ordering = ['id']
