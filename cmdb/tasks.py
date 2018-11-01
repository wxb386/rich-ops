from celery import task, platforms
from time import sleep

platforms.C_FORCE_ROOT = True


@task
def mytask(param):
    print('执行%s' % param)
    sleep(10)
    print('执行完毕%s' % param)
    return True
