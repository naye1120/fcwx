from django.db import models


class WeChatToken(models.Model):
    appid = models.CharField(max_length=255, unique=True)
    access_token = models.CharField(max_length=255)
    expires_at = models.DateTimeField(null=True, blank=True)  # 可以用来存储token的过期时间

    # 其他你可能需要的字段...

    def __str__(self):
        return self.appid


from django.db import models
from django.utils.translation import gettext_lazy as _


# 假设你已经有或将会创建以下两个模型
class Classroom(models.Model):
    name = models.CharField(_("班级名称"), max_length=100)
    school = models.CharField(_("学校"), max_length=200)
    homeroom_teacher = models.CharField(_("班主任"), max_length=100)
    homeroom_teacher_phone = models.CharField(_("班主任联系方式"), max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("班级")
        verbose_name_plural = _("班级列表")


class HostClass(models.Model):
    name = models.CharField(_("托管班级名称"), max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("托管班级")
        verbose_name_plural = _("托管班级列表")


class StudentProfile(models.Model):
    # 学生基本信息
    name = models.CharField(_("姓名"), max_length=100)
    class_name = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, verbose_name=_("班级"))
    birthday = models.DateField(_("生日"))
    gender = models.CharField(
        _("性别"),
        max_length=10,
        choices=(('male', _("男")), ('female', _("女"))),
        default='male'
    )
    nationality = models.CharField(_("民族"), max_length=50)
    home_address = models.TextField(_("家庭住址"))
    guardian = models.CharField(_("监护人"), max_length=100)
    guardian_phone = models.CharField(_("监护人联系电话"), max_length=20)

    # 托管相关信息
    host_class = models.ForeignKey(HostClass, on_delete=models.SET_NULL, null=True, verbose_name=_("所在托管班级"))
    responsible_teacher = models.CharField(_("负责老师"), max_length=100)
    responsible_teacher_phone = models.CharField(_("负责老师联系方式"), max_length=20)

    # 剩余课时
    remaining_hours = models.IntegerField(default=0, verbose_name="剩余课时")
    # 餐费余额
    meal_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="餐费余额")
    # 唯一标识和关联
    archive_number = models.CharField(_("档案编号"), max_length=50, unique=True)
    parent_openid = models.CharField(_("家长openid"), max_length=100)

    # Django的自动时间戳字段（可选）
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("学生档案")
        verbose_name_plural = _("学生档案列表")
        ordering = ['-created_at']  # 按照创建时间降序排列


class StudentRecord(models.Model):
    # 学生姓名
    student_name = models.CharField(max_length=100, verbose_name="学生姓名")
    # 档案编号，设为唯一
    file_number = models.CharField(max_length=50,  verbose_name="档案编号")
    # 本次变化课时
    changed_hours = models.IntegerField(default=0, verbose_name="本次变化课时")
    # 剩余课时
    remaining_hours = models.IntegerField(default=0, verbose_name="剩余课时")
    # 本次扣减餐费
    deducted_meal_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="本次扣减餐费")
    # 餐费余额
    meal_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="餐费余额")
    # 发生时间
    occurrence_time = models.DateTimeField(auto_now_add=True, verbose_name="发生时间")
    # 上午标识符（假设为布尔类型）
    morning = models.BooleanField(default=False, verbose_name="上午")
    # 下午标识符（假设为布尔类型）
    afternoon = models.BooleanField(default=False, verbose_name="下午")
    # 午饭标识符（假设为布尔类型）
    lunch = models.BooleanField(default=False, verbose_name="午饭")
    # 备注
    note = models.TextField(blank=True, verbose_name="备注")

    # 这里可以添加更多逻辑或方法

    class Meta:
        verbose_name = "学生课时记录"
        verbose_name_plural = "学生课时记录"

    def __str__(self):
        return f"{self.student_name} - {self.file_number}"


from django.db import models


class RechargeRecord(models.Model):
    # 学生姓名
    student_name = models.CharField(max_length=100, verbose_name="学生姓名")
    # 档案编号
    file_number = models.CharField(max_length=50, verbose_name="档案编号")
    # 充值日期
    recharge_date = models.DateField(verbose_name="充值日期")
    # 充值课时
    recharge_hours = models.IntegerField(default=0, verbose_name="充值课时")
    # 充值餐费
    recharge_meal_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="充值餐费")
    # 缴费方式，使用choices限制选项
    PAYMENT_CHOICES = (
        ('wechat', '微信'),
        ('transfer', '转账'),
        ('cash', '现金'),
        ('other', '其他'),
    )
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='other', verbose_name="缴费方式")
    # 备注
    note = models.TextField(blank=True, verbose_name="备注")

    class Meta:
        verbose_name = "充值记录"
        verbose_name_plural = "充值记录"

    def __str__(self):
        return f"{self.student_name} - {self.file_number} - {self.recharge_date}"

        # 可以添加其他方法或属性

    @property
    def payment_method_display(self):
        """返回缴费方式的易读名称"""
        return dict(self.PAYMENT_CHOICES).get(self.payment_method, '未知')