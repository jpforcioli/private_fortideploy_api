#! /usr/bin/python

max_entries = 436

b1 = 10
b2 = 0
b3 = 0
b4 = 0

group_id = 1
i = 0

ha_pri = [200, 100]

for entry in range(0, max_entries):
    b4 += 1
    if b4 >= 256:
        b3 += 1
        b4 = 0
    if b3 >= 256:
        b2 +=1
        b3 = 0

    ip = '{}.{}.{}.{}'.format(str(b1), str(b2), str(b3), str(b4))

    string = '{} Interface: wan2 {}/24; Router-Static: 1 wan2 0.0.0.0/0 10.255.255.254; Virtual-Switch: purge; HA: group{} fortinet {} a-p internal7 {}; FMG: 192.168.194.84'.format(ip, ip, group_id, group_id, ha_pri[i])

    if i == 1:
        group_id += 1
        i = 0
    else:
        i += 1

    print string
