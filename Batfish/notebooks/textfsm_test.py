import os
import sys
#sys.path.append('/Users/lisago/python/ansible/venv/lib/python3.7/site-packages')

import textfsm
#from pybatfish.client.commands import *
#from pybatfish.question.question import load_questions, list_questions
#from pybatfish.question import bfq
#sys.path.append("User/lisago/python/ansible/venv/lib/python3.7/site-packages/")
#import textfsm

'''
出力結果の見方:
Line_Contentはどのアクセスリストがその通信を許可しているのか表示
'''
#acl_file = 'networks/example-filters/mycandidate/config/ASA_acl.cfg'
#ntc_template = 'ntc-templates/cisco_asa_show_access-list.template'
acl_file = 'networks/example-filters/mycandidate/config/cisco_ios_show_ip_interfaces.cfg'
ntc_template = os.path.join('ntc-templates/', 'cisco_ios_show_ip_interfaces.template')
#acl_file = 'networks/example-filters/mycandidate/config/ios_show_inventory.cfg'
#ntc_template = os.path.join('ntc-templates/', 'cisco_ios_show_inventory.template')


with open(acl_file, 'r') as f:
    inventory_text = f.read()

with open(ntc_template) as f:
    #table = textfsm.TextFSM(f)
    fsm = textfsm.TextFSM(f)
    fsm_results = fsm.ParseText(inventory_text)
    parsed = [dict(zip(fsm.header, row)) for row in fsm_results]
    print(parsed)
    print('#################')