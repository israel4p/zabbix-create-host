#!/usr/bin/env python3

from zabbix_api import Already_Exists, ZabbixAPI
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

server = config['ZABBIX']['server']
username = config['ZABBIX']['username']
password = config['ZABBIX']['password']

zapi = ZabbixAPI(server=server, path='')
zapi.login(username, password)

with open('hosts.txt', 'r') as hosts:
    hosts = hosts.readlines()

for host in hosts:
    host_list = host.strip().split(';')

    try:
        zapi.host.create({
            "host":
            host_list[0],
            "interfaces": [{
                "type": "1",
                "main": "1",
                "useip": "1",
                "ip": host_list[1],
                "dns": "",
                "port": "10050"
            }],
            "groups": [{
                "groupid": "15"
            }]
        })
        print('Host %s cadastrado' % host_list[0])

    except Already_Exists:
        print('Host %s já existe' % host_list[0])
