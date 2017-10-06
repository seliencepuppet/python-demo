from django.db import models
from users.models import UserProfile

# Create your models here.
class Asset(models.Model):
	asset_type_choices = (
		('server', u'服务器'),
		('switch', u'交换机'),
		('router', u'路由器'),
		('firewall', u'防火墙'),
		('storage', u'存储设备'),
		('NLB', u'NetScaler'),
		('wireless', u'无线AP'),
		('software', u'软件资产'),
		('others', u'其它类'),
	)

	asset_type = models.CharField(choices=asset_type_choices, max_length=64, default='server')
	name = models.CharField(max_length=64, unique=True)
	sn = models.CharField(u'资产SN号', max_length=128, unique=True)
	manufactory = models.ForeignKey('Manufactory', verbose_name=u'制造商', null=True, blank=True)
	management_ip = models.GenericIPAddressField(u'管理IP', blank=True, null=True)
	
	contract = models.ForeignKey('Contract', verbose_name=u'合同', null=True, blank=True)
	trade_date = models.DateField(u'购买时间', null=True, blank=True)
	expire_date = models.DateField(u'过保修期', null=True, blank=True)
	price = models.FloatField(u'价格', null=True, blank=True)
	business_unit = models.ForeignKey('BusinessUnit', verbose_name=u'所属业务线', null=True, blank=True)
	tags = models.ManyToManyField('Tag', blank=True)
	admin = models.ForeignKey(UserProfile, verbose_name=u'资产管理员', null=True, blank=True)
	idc = models.ForeignKey('IDC', verbose_name=u'IDC机房', null=True, blank=True)

	memo = models.TextField(u'备注', null=True, blank=True)
	create_date = models.DateTimeField(blank=True, auto_now_add=True)
	update_date = models.DateTimeField(blank=True, auto_now=True)

	class Meta:
		verbose_name = u"资产总表"
		verbose_name_plural = verbose_name

	def __str__(self):
		return ('id:%s name:%s' % (self.id, self.name))


class Server(models.Model):
	asset = models.OneToOneField('Asset')
	created_by_choices = (
		('auto', 'Auto'),
		('manual', 'Manual'),
	)
	created_by = models.CharField(choices=created_by_choices, max_length=128, blank=True, null=True)
	hosted_on = models.ForeignKey('self', related_name='hosted_on_server', blank=True, null=True)
	model = models.CharField(u'型号', max_length=128, null=True, blank=True)
	raid_type = models.CharField(u'raid类型', max_length=5)
	os_type = models.CharField(u'操作系统类型', max_length=32)
	os_distribution = models.CharField(u'发型版本', max_length=32)
	os_release = models.CharField(u'操作系统版本', max_length=32)

	create_date = models.DateTimeField(blank=True, auto_now_add=True)
	update_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)

	class Meta:
		verbose_name = u'服务器'
		verbose_name_plural = verbose_name

	def __str__(self):
		return ('%s sn:%s' % (self.asset.name, self.asset.sn))


class CPU(models.Model):
	asset = models.OneToOneField('Asset')
	cpu_model = models.CharField(u'CPU型号', max_length=128, blank=True, null=True)
	cpu_count = models.SmallIntegerField(u'物理cpu个数')
	cpu_core_count = models.SmallIntegerField(u'cpu核数')
	memo = models.TextField(u'备注', null=True, blank=True)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(blank=True, null=True)

	class Meta:
		verbose_name = u"CPU部件"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.cpu_model


class Disk(models.Model):
	asset = models.ForeignKey('Asset')
	sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
	slot = models.CharField(u'插槽位', max_length=64)
	manufactory = models.CharField(u'制造商', max_length=64, blank=True, null=True)
	model = models.CharField(u'磁盘型号', max_length=128, blank=True, null=True)
	capacity = models.FloatField(u'磁盘容量GB')

	disk_iface_choice = (
		('SATA', 'SATA'),
		('SAS', 'SAS'),
		('SCSI', 'SCSI'),
		('SSD', 'SSD'),
	)

	iface_type = models.CharField(u'接口类型', max_length=64, choices=disk_iface_choice, default='SAS')
	memo = models.TextField(u'备注', blank=True, null=True)
	create_date = models.DateTimeField(blank=True, auto_now_add=True)
	update_date = models.DateTimeField(blank=True, null=True)

	auto_create_fields = ['sn', 'slot', 'manufactory', 'model', 'capacity', 'iface_type']

	class Meta:
		unique_together = ['asset', 'slot']
		verbose_name = u"硬盘"
		verbose_name_plural = verbose_name

	def __str__(self):
		return ("%s:slot; %s capacity:%s" % (self.asset_id, self.slot, self.capacity))


class RAM(models.Model):
	asset = models.ForeignKey('Asset')
	sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
	model = models.CharField(u'内存型号', max_length=128)
	slot = models.CharField(u'插槽', max_length=64)
	capacity = models.IntegerField(u'内存大小(MB)')
	memo = models.CharField(u'备注', max_length=128, blank=True, null=True)
	create_date = models.DateTimeField(blank=True, auto_now_add=True)
	update_date = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return ("%s:%s:%s" % (self.asset_id, self.slot, self.capacity))

	class Meta:
		verbose_name = u"RAM"
		verbose_name_plural = verbose_name
		unique_together = ("asset", "slot")

	auto_create_fields = ['sn', 'slot', 'model', 'capacity']


class NIC(models.Model):
	asset = models.ForeignKey('Asset')
	name = models.CharField(u'网卡名', max_length=64, blank=True, null=True)
	sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
	model = models.CharField(u'网卡型号', max_length=128, blank=True, null=True)
	macaddress = models.CharField(u'MAC', max_length=64, unique=True)
	ipaddress = models.GenericIPAddressField(u'IP', blank=True, null=True)
	netmask = models.CharField(max_length=64, blank=True, null=True)
	bonding = models.CharField(max_length=64, blank=True, null=True)
	memo = models.CharField(u'备注', max_length=128, blank=True, null=True)
	create_date = models.DateTimeField(blank=True, auto_now_add=True)
	update_date = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return ("%s:%s" % (self.asset_id, self.macaddress))

	class Meta:
		verbose_name = u"网卡"
		verbose_name_plural = verbose_name

	auto_create_fields = ['name', 'sn', 'model', 'macaddress']


class RaidAdaptor(models.Model):
	asset = models.ForeignKey('Asset')
	sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
	slot = models.CharField(u'插口', max_length=64)
	model = models.CharField(u'型号', max_length=64, blank=True, null=True)
	memo = models.TextField(u'备注', blank=True, null=True)
	create_date = models.DateTimeField(blank=True, auto_now_add=True)
	update_date = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		unique_together = ("asset", "slot")


class NetworkDevice(models.Model):
	asset = models.OneToOneField('Asset')
	vlan_ip = models.GenericIPAddressField(u'VlanIP', blank=True, null=True)
	intranet_ip = models.GenericIPAddressField(u'内网IP', blank=True, null=True)
	sn = models.CharField(u'SN号', max_length=128, unique=True)
	model = models.CharField(u'型号', max_length=128, null=True, blank=True)
	firmware = models.ForeignKey('Software', blank=True, null=True)
	port_num = models.SmallIntegerField(u'端口个数', null=True, blank=True)
	device_detail = models.TextField(u'设置详细配置', null=True, blank=True)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(blank=True, null=True)

	class Meta:
		verbose_name = u"网络设备"
		verbose_name_plural = verbose_name


class Software(models.Model):
	os_types_choice = (
		('linux', 'Linux'),
		('windows', 'Windows'),
		('network_firmware', 'Network Firmware'),
		('software', 'Software'),
	)
	os_distribution_choice = (
		('windows', 'Windows'),
		('centos', 'CentOS'),
		('ubuntu', 'Ubuntu'),
	)
	type = models.CharField(u'系统类型', choices=os_types_choice, max_length=32)
	distribution = models.CharField(u'发型版本', choices=os_distribution_choice, max_length=32)
	version = models.CharField(u'软件/系统版本', max_length=64)
	language_choices = (
		('cn', u'中文'),
		('en', u'英文'),
	)
	language = models.CharField(u'系统语言', choices=language_choices, default='cn', max_length=32)

	def __str__(self):
		return self.version

	class Meta:
		verbose_name = u"软件/系统"
		verbose_name_plural = verbose_name


class Manufactory(models.Model):
	manufactory = models.CharField(u'厂商名称', max_length=64, unique=True)
	support_num = models.CharField(u'支持电话', max_length=30, blank=True)
	memo = models.CharField(u'备注', max_length=128, blank=True)

	def __str__(self):
		return self.manufactory

	class Meta:
		verbose_name = u"厂家"
		verbose_name_plural = verbose_name


class BusinessUnit(models.Model):
	parent_unit = models.ForeignKey('self', related_name='parent_level', blank=True, null=True)
	name = models.CharField(u'业务线', max_length=64, unique=True)
	memo = models.CharField(u'备注', max_length=64, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = u"业务线"
		verbose_name_plural = verbose_name


class Contract(models.Model):
	sn = models.CharField(u'合同号', max_length=128, unique=True)
	name = models.CharField(u'合同名称', max_length=64)
	memo = models.TextField(u'备注', blank=True, null=True)
	price = models.IntegerField(u'合同金额')
	detail = models.TextField(u'合同详细', blank=True, null=True)
	start_date = models.DateField(blank=True)
	end_date = models.DateField(blank=True)
	license_num = models.IntegerField(u'license数量', blank=True)
	create_date = models.DateField(auto_now_add=True)
	update_date = models.DateField(auto_now=True)

	class Meta:
		verbose_name = u"合同"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name


class IDC(models.Model):
	name = models.CharField(u'机房名称', max_length=64, unique=True)
	memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = u"机房"
		verbose_name_plural = verbose_name


class Tag(models.Model):
	name = models.CharField('Tag name', max_length=32, unique=True)
	creater = models.ForeignKey(UserProfile)
	create_date = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.name


class EventLog(models.Model):
	name = models.CharField(u'事件名称', max_length=100)
	event_type_choices = (
		(1, u'硬件变更'),
		(2, u'新增配件'),
		(3, u'设备下线'),
		(4, u'设备上线'),
		(5, u'定期维护'),
		(6, u'业务上线/更新/变更'),
	)
	event_type = models.SmallIntegerField(u'事件类型', choices=event_type_choices)
	asset = models.ForeignKey('Asset')
	component = models.CharField(u'事件子项', max_length=255, blank=True, null=True)
	detail = models.DateTimeField(u'事件详情')
	date = models.DateTimeField(u'事件时间', auto_now_add=True)
	user = models.ForeignKey(UserProfile, verbose_name=u"事件通知人")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = u"事件记录"
		verbose_name_plural = verbose_name

	def colored_event_type(self):
		if sef.event_type == 1:
			cell_html = '<span style="background: orange;">%s</span>'
		elif self.event_type == 2:
			cell_html = '<span style="background: yellowgreen">%s</span>'
		else:
			cell_html = '<span>%s</span>'
		return cell_html % self.get_event_type_display()
	colored_event_type.allow_tags = True
	colored_event_type.short_description = u"事件类型"


class NewAssetApprovalZone(models.Model):
	sn = models.CharField(u'资产SN号', max_length=128, unique=True)
	asset_type_choices = (
		('server', u'服务器'),
		('switch', u'交换机'),
		('router', u'路由器'),
		('firewall', u'防火墙'),
		('storage', u'存储设备'),
		('NLB', u'NetScaler'),
		('wireless', u'无限AP'),
		('software', u'软件资产'),
		('others', u'其它类'),
	)
	asset_type = models.CharField(max_length=32, choices=asset_type_choices, null=True, blank=True)
	manufactory = models.CharField(max_length=64, blank=True, null=True)
	model = models.CharField(max_length=128, blank=True, null=True)
	ram_size = models.IntegerField(blank=True, null=True)
	cpu_model = models.CharField(max_length=128, blank=True, null=True)
	cpu_count = models.IntegerField(blank=True, null=True)
	cpu_core_count = models.IntegerField(blank=True, null=True)
	os_distribution = models.CharField(max_length=64, blank=True, null=True)
	os_type = models.CharField(max_length=64, blank=True, null=True)
	os_release = models.CharField(max_length=64, blank=True, null=True)
	data = models.TextField(u'资产数据')
	date = models.DateTimeField(u'汇报日期', auto_now_add=True)
	approved = models.BooleanField(u'已批准', default=False)
	approved_by = models.ForeignKey(UserProfile, verbose_name=u"汇报相关人员")
	approved_date = models.DateTimeField(u'批准日期', blank=True, null=True)

	def __str__(self):
		return self.sn

	class Meta:
		verbose_name = u"新上线待批准资产"
		verbose_name_plural = verbose_name

