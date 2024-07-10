# Generated by Django 5.0.6 on 2024-06-30 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcwxapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='姓名')),
                ('class_name', models.CharField(max_length=100, verbose_name='班级')),
                ('school', models.CharField(max_length=200, verbose_name='学校')),
                ('birthday', models.DateField(verbose_name='生日')),
                ('gender', models.CharField(choices=[('male', '男'), ('female', '女')], default='male', max_length=10, verbose_name='性别')),
                ('nationality', models.CharField(max_length=50, verbose_name='民族')),
                ('home_address', models.TextField(verbose_name='家庭住址')),
                ('guardian', models.CharField(max_length=100, verbose_name='监护人')),
                ('guardian_phone', models.CharField(max_length=20, verbose_name='监护人联系电话')),
                ('host_class', models.CharField(max_length=100, verbose_name='所在托管班级')),
                ('homeroom_teacher', models.CharField(max_length=100, verbose_name='班主任')),
                ('homeroom_teacher_phone', models.CharField(max_length=20, verbose_name='班主任联系方式')),
                ('responsible_teacher', models.CharField(max_length=100, verbose_name='负责老师')),
                ('responsible_teacher_phone', models.CharField(max_length=20, verbose_name='负责老师联系方式')),
                ('payment_date', models.DateField(verbose_name='缴费日期')),
                ('total_classes', models.IntegerField(verbose_name='总课时')),
                ('paid_classes', models.IntegerField(verbose_name='缴费课时')),
                ('remaining_classes', models.IntegerField(verbose_name='剩余课时')),
                ('meal_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='餐费余额')),
                ('remaining_points', models.IntegerField(default=0, verbose_name='剩余积分')),
                ('archive_number', models.CharField(max_length=50, unique=True, verbose_name='档案编号')),
                ('parent_openid', models.CharField(max_length=100, verbose_name='家长openid')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '学生档案',
                'verbose_name_plural': '学生档案列表',
                'ordering': ['-created_at'],
            },
        ),
    ]
