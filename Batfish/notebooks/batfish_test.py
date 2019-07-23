#!/usr/bin/python
#-*- utf-8 -*-

import os
import subprocess
import json
import sys
import re
#textfsmのパスをnotebookに渡す
sys.path.append('/Users/lisago/python/ansible/venv/lib/python3.7/site-packages')
import textfsm
from pybatfish.client.commands import *
from pybatfish.question.question import load_questions, list_questions
from pybatfish.question import bfq
from pybatfish.question import *
from pybatfish.datamodel import *

#subprocess.call()('startup.py')
load_questions()

# Initialize a network and a snapshot
bf_set_network("network-example-filters")

SNAPSHOT_NAME = "mycurrent"
SNAPSHOT_PATH = "networks/example-filters/mycurrent"
bf_init_snapshot(SNAPSHOT_PATH, name=SNAPSHOT_NAME, overwrite=True)


#acl_file = 'networks/example-filters/mycandidate/config/ASA_acl.cfg'
#ntc_template = 'ntc-templates/cisco_asa_show_access-list.template'
#acl_file = 'networks/example-filters/mycandidate/config/nxos_acl_sample.cfg'
#ntc_template = 'ntc-templates/cisco_nxos_show_access-lists.template'
interface_config_file = 'networks/example-filters/mycandidate/config/cisco_ios_show_ip_interfaces.cfg'
ntc_template = 'ntc-templates/cisco_ios_show_ip_interfaces.template'

'''
[{'INTF': 'Serial0', 'LINK_STATUS': 'down', 'PROTOCOL_STATUS': 'down', 'IPADDR': ['192.168.1.1/24*'],
'MASK': ['1'], 'VRF': '', 'MTU': '1500', 'IP_HELPER': [], 'OUTGOING_ACL': '', 'INBOUND_ACL': ''}]
'''

def output(interface, template):
    with open(interface, 'r') as f:
        inventory_text = f.read()

    with open(ntc_template) as f:
        #table = textfsm.TextFSM(f)
        fsm = textfsm.TextFSM(f)
        fsm_results = fsm.ParseText(inventory_text)
        parsed = [dict(zip(fsm.header, row)) for row in fsm_results]
        f.close()
    return parsed

def extract_interface(parsed):
    address_list = []
    for con in parsed:
        ipaddress = con['IPADDR']
        for add in ipaddress:
            #address.strip('*')
            address = re.sub(r'\*', ' ', add)
            address_list.append(address)

    return address_list


parsed = output(interface_config_file, ntc_template)
address_list = extract_interface(parsed)
#ip_owners_ans = bfq.ipOwners().answer()
ip_owners_ans = bfq.ipOwners().answer()
#print(ip_owners_ans)
json_frame = ip_owners_ans.frame()
print(json_frame.to_json())

for address in address_list:
    ip_flow = HeaderConstraints(srcIps=address)
                             #dstIps='255.255.255.0')
    answer = bfq.testFilters(headers=ip_flow,
                             nodes='before_summary_asa',
                             filters="SPLIT-ACL").answer()
    #show(answer.frame())
    #print(answer.to_json())

