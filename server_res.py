#!/usr/bin/python
# -*- coding: utf-8 -*-
# 服务器的资源数据获取,主要在python2的环境使用

import psutil
from time import sleep

dynamic = {}
static = {}


def cpu():
    # cpu的物理核心数
    static['cpu_count'] = psutil.cpu_count(logical=False)
    # cpu的当前频率和频率范围,默认时所有统计在一起
    cpu_freq = psutil.cpu_freq(percpu=False)
    static['cpu_freq_min'] = cpu_freq[1]
    static['cpu_freq_max'] = cpu_freq[2]
    # cpu统计数据,上下文,中断
    cpu_stats = psutil.cpu_stats()
    dynamic['cpu_ctx_switches'] = cpu_stats[0]
    dynamic['cpu_interrupts'] = cpu_stats[1]
    dynamic['cpu_soft_interrupts'] = cpu_stats[2]
    # cpu使用率,统计间隔2秒的使用率
    dynamic['cpu_percent'] = psutil.cpu_percent(interval=2)
    # cpu时间统计,用户时间,系统时间,空闲时间
    cpu_time = psutil.cpu_times(percpu=False)
    dynamic['cpu_user'] = cpu_time[0]
    dynamic['cpu_system'] = cpu_time[2]
    dynamic['cpu_idle'] = cpu_time[3]
    dynamic['cpu_iowait'] = cpu_time[4]


def memory():
    # 虚拟内存
    virtual_memory = psutil.virtual_memory()
    static['memory_total'] = virtual_memory[0]
    dynamic['memory_available'] = virtual_memory[1]
    dynamic['memory_percent'] = virtual_memory[2]
    # 交换内存
    swap_memory = psutil.swap_memory()
    static['swap_total'] = swap_memory[0]
    dynamic['swap_percent'] = swap_memory[3]


def network():
    # 网卡基本信息
    net_if_stats = psutil.net_if_stats()
    net_if = {}
    for i in net_if_stats:
        speed = net_if_stats[i][2]
        # 有速率的网卡是物理网卡,链路聚合的网卡状况未知
        # 有的网卡速率是65535的
        if speed == 0 or speed % 100 != 0: continue
        net_if[i] = {'speed': speed}
    static['net_if'] = net_if
    # 网络io信息
    net_if = {}
    net_io_counters = psutil.net_io_counters(pernic=True)
    for i in net_if:
        net_if[i]['bytes_sent'] = net_io_counters[i].bytes_sent
        net_if[i]['bytes_recv'] = net_io_counters[i].bytes_recv
        net_if[i]['packets_sent'] = net_io_counters[i].packets_sent
        net_if[i]['packets_recv'] = net_io_counters[i].packets_recv

    dynamic['net_if'] = net_if


def disk():
    # 磁盘分区信息
    disk_partitions = psutil.disk_partitions(all=True)
    count = {}
    for i in disk_partitions:
        device = i[0]
        if device.startswith('/'):
            # 如果已有记录了,就判断谁的挂载点路径更短,保存短的挂载点
            if (device in count) and (len(count[device]) < len(i[1])):
                continue
            count[device] = i[1]
    static['disk_partitions'] = count
    # 每个磁盘的io信息
    disk_io_counters = psutil.disk_io_counters(perdisk=True)
    count = {}
    for i in disk_io_counters:
        io = {}
        io['read_count'] = disk_io_counters[i][0]
        io['write_count'] = disk_io_counters[i][1]
        io['read_bytes'] = disk_io_counters[i][2]
        io['write_bytes'] = disk_io_counters[i][3]
        count[i] = io
    dynamic['disk_io_counters'] = count


def server():
    pass


if __name__ == '__main__':
    cpu()
    memory()
    network()
    disk()
    server()
    print('>>> static - 静态信息\n')
    for i in static:
        print('  %s : %s' % (i, static[i]))
    else:
        print('\n<<< static - 静态信息\n')
    print('>>> dynamic - 动态信息\n')
    for i in dynamic:
        print('  %s : %s' % (i, dynamic[i]))
    else:
        print('\n<<< dynamic - 动态信息\n')
