from django.db import models
from django.contrib.auth.models import User

class HostConfig(models.Model):
    IDLE=0
    RUNNING=1
    COMPLETED=2
    FAILED=3
    status_options=(
        (IDLE, 'Idle'),
        (RUNNING, 'Running'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed'),
    )
    CENTOS=1
    UBUNTU=2
    os_options=(
        (CENTOS, 'CentOS'),
        (UBUNTU, 'Ubuntu'),
    )
    ip_address = models.GenericIPAddressField(protocol='IPv4')
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    status = models.SmallIntegerField(choices=status_options,default=IDLE)
    os_type = models.IntegerField(choices=os_options,null=True,blank=True)
    os_version = models.CharField(max_length=50,null=True,blank=True)
    err_msg = models.TextField(null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'host_config'
