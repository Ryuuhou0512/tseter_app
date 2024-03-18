
from flask import Blueprint

# 创建 user_bp 蓝图

# 从 view 模块中导入视图函数
user_bp = Blueprint('user_bp', __name__,template_folder='template')

# 注册蓝图
from . import view
