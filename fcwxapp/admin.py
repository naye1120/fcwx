from django.contrib import admin
from .models import StudentProfile, HostClass, Classroom  # 导入你的模型


# 注册你的模型到Django的admin
class StudentAdmin(admin.ModelAdmin):
    # 这里你可以定义ModelAdmin的选项，但因为我们想要所有字段都是可编辑的，
    # 并且Django默认就是这样，所以我们不需要添加任何额外的字段列表。
    # 如果你想要自定义列表显示的字段，你可以这样做：
    # list_display = ('name', 'class_name', 'school', ...)
    pass


admin.site.register(StudentProfile, StudentAdmin)  # 注册模型到admin，并指定ModelAdmin类

class ClassroomAdmin(admin.ModelAdmin):
    # 这里你可以定义ModelAdmin的选项，但因为我们想要所有字段都是可编辑的，
    # 并且Django默认就是这样，所以我们不需要添加任何额外的字段列表。
    # 如果你想要自定义列表显示的字段，你可以这样做：
    # list_display = ('name', 'class_name', 'school', ...)
    pass


admin.site.register(Classroom, ClassroomAdmin)  # 注册模型到admin，并指定ModelAdmin类

class HostClassadmin(admin.ModelAdmin):
    # 这里你可以定义ModelAdmin的选项，但因为我们想要所有字段都是可编辑的，
    # 并且Django默认就是这样，所以我们不需要添加任何额外的字段列表。
    # 如果你想要自定义列表显示的字段，你可以这样做：
    # list_display = ('name', 'class_name', 'school', ...)
    pass


admin.site.register(HostClass, HostClassadmin)  # 注册模型到admin，并指定ModelAdmin类