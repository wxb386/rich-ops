
1.下载模块
```bash
pip3 install django-celery flower gunicorn
```

2.修改配置文件settings.py
```python
import djcelery  # celery模块

# 添加app
INSTALLED_APPS = [
    'djcelery',
]

# celery配置
djcelery.setup_loader()
BROKER_URL = 'amqp://admin:admin@192.168.80.254:5672'
CELERY_IMPORTS = ('cmdb.tasks')
# CELERY_RESULT_BACKEND = 'amqp://admin:admin@192.168.80.254:5672'
```

3.在app的根目录下创建tasks.py
```python
from celery import task, platforms
from time import sleep

# 允许celery以root用户启动
platforms.C_FORCE_ROOT = True

# 声明任务函数
@task
def mytask(param):
    print('执行%s' % param)
    sleep(10)
    print('执行完毕%s' % param)
    # 返回True为success
    return True

```

4.开始添加任务
```python
from cmdb.tasks import mytask
a=mytask.delay('lalalala04')
a.ready() # 返回False表示未完成

```

5.更新数据库
```bash
python manage.py makemigrations
python manage.py migrate
```

6.启动服务
```bash
gunicorn -D -w 2 --reload -b 0.0.0.0:8080 richops.wsgi
python manage.py celery worker -D --loglevel=info
python manage.py celery flower -D
```
