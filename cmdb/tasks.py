from .models import Job
from celery import task, platforms
from time import sleep

platforms.C_FORCE_ROOT = True


@task
def remote_execute(job_id):
    print('def remote_execute(job):')
    try:
        job = Job.objects.get(pk=job_id)
        print(job)
        job.status = '进行中'
        job.save()
        sleep(5)
        out = {
            'address': job.host_ip.route,
            'script': job.task_name.task.content,
            'param': job.task_name.param,
            'other': None
        }
        print(out)
        job.status = '已完成'
        job.status = '已创建'
        job.save()
    except Exception as e:
        print(e)
    return
