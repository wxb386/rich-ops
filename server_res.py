#!/usr/bin/python
# -*- coding: utf-8 -*-
# 服务器的资源数据获取,主要在python2的环境使用

import psutil
import time
import json


class Config():
    WAN_ADDR = '192.168.80'


static = {}


def cpu():
    '''
{
  "cpu": {
    "cpu_count": 2,                  #cpu的物理核心数
    "cpu_freq_min": 1600.0,          #cpu的当前频率
    "cpu_freq_max": 3100.0,          #cpu的频率范围
    "cpu_ctx_switches": 173275986,   #上下文
    "cpu_interrupts": 74589867,      #中断
    "cpu_soft_interrupts": 51475233, #软中断
    "cpu_percent": 13.8,             #cpu使用率
    "cpu_user": 9461.61,             #cpu用户时间
    "cpu_system": 1895.57,           #cpu系统时间
    "cpu_idle": 350045.97,           #cpu空闲时间
    "cpu_iowait": 945.14             #cpuIO时间
  }
}
    :return:
    '''
    stat = {}
    # cpu的物理核心数
    stat['cpu_count'] = psutil.cpu_count(logical=False)
    # cpu的当前频率和频率范围,默认时所有统计在一起
    cpu_freq = psutil.cpu_freq(percpu=False)
    stat['cpu_freq_min'] = cpu_freq[1]
    stat['cpu_freq_max'] = cpu_freq[2]
    # cpu统计数据,上下文,中断
    cpu_stats = psutil.cpu_stats()
    stat['cpu_ctx_switches'] = cpu_stats[0]
    stat['cpu_interrupts'] = cpu_stats[1]
    stat['cpu_soft_interrupts'] = cpu_stats[2]
    # cpu使用率,统计间隔2秒的使用率
    stat['cpu_percent'] = psutil.cpu_percent(interval=2)
    # cpu时间统计,用户时间,系统时间,空闲时间
    cpu_time = psutil.cpu_times(percpu=False)
    stat['cpu_user'] = cpu_time[0]
    stat['cpu_system'] = cpu_time[2]
    stat['cpu_idle'] = cpu_time[3]
    stat['cpu_iowait'] = cpu_time[4]
    global static
    static['cpu'] = stat


def memory():
    '''
{
  "memory": {
    "memory_total": 8212160512,     #内存总量
    "memory_available": 5525135360, #空闲内存
    "memory_percent": 32.7,         #内存使用比例
    "swap_total": 0,                #交换分区总量
    "swap_percent": 0               #交换分区使用比例
  }
}
    :return:
    '''
    memory = {}
    # 虚拟内存
    virtual_memory = psutil.virtual_memory()
    memory['memory_total'] = virtual_memory[0]
    memory['memory_available'] = virtual_memory[1]
    memory['memory_percent'] = virtual_memory[2]
    # 交换内存
    swap_memory = psutil.swap_memory()
    memory['swap_total'] = swap_memory[0]
    memory['swap_percent'] = swap_memory[3]
    global static
    static['memory'] = memory


def network():
    network_stat = {}
    # 网卡基本信息
    net_if_stats = psutil.net_if_stats()
    # 网络io信息
    net_io_counters = psutil.net_io_counters(pernic=True)
    for i in net_if_stats:
        speed = net_if_stats[i][2]
        # 有速率的网卡是物理网卡,链路聚合的网卡状况未知
        # 有的网卡速率是65535的
        # 非物理网卡则跳过
        if speed == 0 or speed % 10 != 0: continue
        network_stat[i] = {}
        network_stat[i]['speed'] = speed
        network_stat[i]['bytes_sent'] = net_io_counters[i].bytes_sent
        network_stat[i]['bytes_recv'] = net_io_counters[i].bytes_recv
        network_stat[i]['packets_sent'] = net_io_counters[i].packets_sent
        network_stat[i]['packets_recv'] = net_io_counters[i].packets_recv

    global static
    static['network'] = network_stat


def disk():
    # 磁盘分区信息
    disk_partitions = psutil.disk_partitions(all=True)
    disk_stat = {}
    for i in disk_partitions:
        device = i[0]
        path = i[1]
        # 当设备不是物理设备时,跳过
        if not device.startswith('/'): continue
        # 如果已有记录了,就判断谁的挂载点路径更短,保存短的挂载点
        if (device in disk_stat):
            if (len(disk_stat[device]['path']) < len(path)):
                continue
        disk_stat[device] = {}
        disk_stat[device]['path'] = path
        disk_usage = psutil.disk_usage(path)
        disk_stat[device]['total'] = disk_usage.total
        disk_stat[device]['free'] = disk_usage.free
        disk_stat[device]['percent'] = disk_usage.percent
    global static
    static['disk'] = disk_stat


def host():
    host_stat = {}
    net_addrs = psutil.net_if_addrs()
    addrs = []
    for i in net_addrs:
        for proto in net_addrs[i]:
            if proto[0] == 2: addrs.append(proto[1])
    host_stat['wan'] = []
    host_stat['lan'] = []
    for addr in addrs:
        if addr.startswith(Config.WAN_ADDR):
            host_stat['wan'].append(addr)
        else:
            host_stat['lan'].append(addr)
    host_stat['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    global static
    static['host'] = host_stat


def server():
    pass


if __name__ == '__main__':
    cpu()
    memory()
    network()
    disk()
    host()
    server()

    print(json.dumps(static, indent=2))
