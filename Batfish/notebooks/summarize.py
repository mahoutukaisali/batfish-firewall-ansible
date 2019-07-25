#!/usr/bin/python

import os
import re
import sys
import json
import netaddr
import ipaddress
from ipaddress import *
from netaddr import *

param1 = sys.argv[1]

# Function to get Object Information
def get_object_info(name):
  os.chdir(os.path.join(os.environ['HOME'], "KIaI_Tool_Build", "param", param1, "input"))
  source_file = 'Show_RunningConfig_' + param1 + '.txt'
  with open(source_file, 'r') as sf:
    for line in sf:
      line = line.strip()
      if line.startswith('object network ' + name):
        i = next(sf, '').strip().split(' ')[1:]
        object_info = [name] + i
      
  return object_info

# Function to get Network Object Group Information
def get_network_object_group_info(name):
  add_lines = False
  nwobject_group_info = []
  os.chdir(os.path.join(os.environ['HOME'], "KIaI_Tool_Build", "param", param1, "input"))
  source_file = 'Show_RunningConfig_' + param1 + '.txt'
  with open(source_file, 'r') as sf:
    for line in sf:
      if line.startswith('object-group network ' + name):
        add_lines = True
      elif line.startswith("object-group") or line.startswith("access-list"):
        add_lines = False
      
      if add_lines:
        nwobject_group_info.append(line.replace('\n', ''))
      
  return nwobject_group_info

# Function to get Service Object Group Information
def get_service_object_group_info(name):
  add_lines = False
  srvobject_group_info = []
  os.chdir(os.path.join(os.environ['HOME'], "KIaI_Tool_Build", "param", param1, "input"))
  source_file = 'Show_RunningConfig_' + param1 + '.txt'
  with open(source_file, 'r') as sf:
    for line in sf:
      if line.startswith('object-group service ' + name):
        add_lines = True
      elif line.startswith("object-group") or line.startswith("access-list"):
        add_lines = False
      
      if add_lines:
        srvobject_group_info.append(line.replace('\n', ''))
      
  return srvobject_group_info

# Function to group Standard Type ACLs
def acl_standard(listname):
  acl_type_std_permit = []
  acl_type_std_deny = []
  for i in listname:
    if i['acl_filter'] == 'permit':
      acl_type_std_permit.append(i)
    elif i['acl_filter'] == 'deny':
      acl_type_std_deny.append(i)
  
  tmp1_1 = []
  tmp2_1 = []
  tmp3_1 = []
  tmp4_1 = []
  tmp5_1 = []
  tmp6_1 = []
  tmp7_1 = []
  tmp8_1 = []
  tmp9_1 = []
  tmp10_1 = []
  if len(acl_type_std_permit) != 0:
    for i in acl_type_std_permit:
      if i['src_network'] != '' and i['src_mask'] != '':
        tmp2_1.append('access-list ' + ' '.join(filter(None, i.values())))
      elif i['src_host'] != 0:
        tmp2_1.append('access-list ' + ' '.join(filter(None, i.values())))
      else:
        tmp1_1.append('access-list ' + ' '.join(filter(None, i.values())))
  
  for i in tmp2_1:
    tmp3_1.append(i.split(' ')[4])
  
  for i in tmp3_1:
    if re.match(r'\d+\.\d+\.\d+\.\d+', i):
      tmp4_1.append('IP')
    elif re.match(r'\S+', i):
      tmp4_1.append('STR')
  
  if tmp4_1.count('IP') > 1 or tmp4_1.count('STR') > 1:
    for i, j in enumerate(tmp4_1):
      if j == 'IP':
        tmp5_1.extend(list(e for d, e in enumerate(tmp2_1) if i == d))
      elif j == 'STR':
        tmp6_1.extend(list(e for d, e in enumerate(tmp3_1) if i == d))	
  elif tmp4_1.count('IP') <= 1 or tmp4_1.count('STR') <= 1:
    for i, j in enumerate(tmp3_1):
      tmp7_1.extend(list(e for d, e in enumerate(tmp2_1) if i == d))
  
  if len(tmp5_1) <= 1:
    tmp7_1.extend(tmp5_1)
  elif len(tmp5_1) > 1:
    tmp8_1.extend(tmp5_1)
  
  for i, j in enumerate(tmp2_1):
    if len(set(tmp6_1)) > 1:
      tmp7_1.extend(list(e for d, e in enumerate(tmp2_1) if i == d))
    elif len(set(tmp6_1)) == 1:
      tmp9_1.extend(set(d for d in tmp2_1 if d.split(' ')[4] in tmp6_1))
  
  tmp10_1 = list(set(tmp9_1)) + tmp8_1
  
  tmp1_2 = []
  tmp2_2 = []
  tmp3_2 = []
  tmp4_2 = []
  tmp5_2 = []
  tmp6_2 = []
  tmp7_2 = []
  tmp8_2 = []
  tmp9_2 = []
  tmp10_2 = []
  if len(acl_type_std_deny) != 0:
    for i in acl_type_std_deny:
      if i['src_network'] != '' and i['src_mask'] != '':
        tmp2_2.append('access-list ' + ' '.join(filter(None, i.values())))
      elif i['src_host'] != 0:
        tmp2_2.append('access-list ' + ' '.join(filter(None, i.values())))
      else:
        tmp1_2.append('access-list ' + ' '.join(filter(None, i.values())))
  
  for i in tmp2_2:
    tmp3_2.append(i.split(' ')[4])
  
  for i in tmp3_2:
    if re.match(r'\d+\.\d+\.\d+\.\d+', i):
      tmp4_2.append("IP")
    elif re.match(r'\S+', i):
      tmp4_2.append("STR")
  
  if len(set(tmp4_2)) > 1 and tmp4_2.count('IP') <= 1 or tmp4_2.count('STR') <= 1:
    for i, j in enumerate(tmp3_2):
      tmp7_2.extend(list(e for d, e in enumerate(tmp2_2) if i == d))
  else:
    for i, j in enumerate(tmp4_2):
      if j == 'IP':
        tmp5_2.extend(list(e for d, e in enumerate(tmp2_2) if i == d))
      elif j == 'STR':
        tmp6_2.extend(list(e for d, e in enumerate(tmp3_2) if i == d))
  
  if len(tmp5_2) <= 1:
    tmp7_2.extend(tmp5_2)
  elif len(tmp5_2) > 1:
    tmp8_2.extend(tmp5_2)
  
  for i, j in enumerate(tmp2_2):
    if len(set(tmp6_2)) > 1:
      tmp7_2.extend(list(e for d, e in enumerate(tmp2_2) if i == d))
    elif len(set(tmp6_2)) == 1:
      tmp9_2.extend(set(d for d in tmp2_2 if d.split(' ')[4] in tmp6_2))
  
  tmp10_2 = list(set(tmp9_2)) + tmp8_2
  
  non_sum_tmp = tmp7_1 + tmp7_2
  sum_tmp = tmp10_1 + tmp10_2
  
  if len(non_sum_tmp) != 0:
    non_sum_tmp.insert(0, '-------------- Non Summarized ACL --------------')
    non_sum_tmp.append('                                                ')
    acl_standard_non_summary_list.extend(non_sum_tmp)
  
  if len(sum_tmp) != 0:
    sum_tmp.insert(0, '-------------- Original ACL --------------')
    sum_tmp.append('                                                ')
    acl_standard_summary_list.extend(sum_tmp)

# Load source FSM data
os.chdir(os.path.join(os.environ['HOME'], "KIaI_Tool_Build", "param", param1, "results"))
input_file = 'ACL_Parsed_Results_' + param1 + '.txt'

with open(input_file, 'r') as f:
  data =  json.loads(f.read().replace("'", "\""))

# Sort source data
data_sorted = sorted(data, key = lambda i: (i['acl_name'], i['remark'], i['acl_type'], i['acl_filter']))

# Create individual list of all Unique ACL names to be summarized & group ACLs
unique_acl_name = sorted(set([d['acl_name'] for d in data_sorted]))
sorted_acl_name_lists = [[] for i in range(len(sorted(set([d['acl_name'] for d in data_sorted]))))]
j = 0
for i in unique_acl_name:
  sorted_acl_name_lists[j] = [d for d in data_sorted if d['acl_name'] == i]
  j += 1

# Create ACL groups based on FSM Headers over list of Unique ACL names
acl_summarize_list = []
acl_non_summarize_list = []
acl_type_ext = []
acl_type_std = []
acl_type_rem = []
acl_type_std_permit = []
acl_type_std_deny = []
acl_type_ext_permit = []
acl_type_ext_deny = []

for li in sorted_acl_name_lists:
  if len(li) <= 1:
    acl_non_summarize_list.append(li)
  elif len(li) > 1:
    for i in li:
      if i['acl_type'] == 'extended':
        acl_type_ext.append(i)
      elif i['acl_type'] == 'standard':
        acl_type_std.append(i)
      elif i['remark'] != '':
        acl_type_rem.append(i)

# Summarize Remark Type ACLs
acl_remark_summary_list = []
acl_remark_non_summary_list = []
acl_name_type_remark_unique = sorted(set([i for i in [i['acl_name'] for i in acl_type_rem] if [i['acl_name'] for i in acl_type_rem].count(i)>1]))
acl_name_type_remark_unique_lists = [[] for i in range(len(acl_name_type_remark_unique))]
i = 0
for j in acl_name_type_remark_unique:
  for k in acl_type_rem:
    if j == k['acl_name']:
      acl_name_type_remark_unique_lists[i].append(k)
    elif j != k['acl_name']:
      acl_remark_non_summary_list.append('-------------- Non Summarized ACL --------------')
      acl_remark_non_summary_list.append(k)
      acl_remark_non_summary_list.append('                                                ')
      
  i += 1

new_remark = [[] for i in range(len(acl_name_type_remark_unique))]
i = 0
for j in acl_name_type_remark_unique_lists:
  for k in j:
    new_remark[i].append(k['remark'].split('remark ')[1])
  i += 1

for i in acl_name_type_remark_unique_lists:
   acl_remark_summary_list.append('-------------- Original ACL --------------')
   for j in i:
     acl_remark_summary_list.append('access-list ' + ' '.join(filter(None, j.values())))

k = 0
for i in acl_name_type_remark_unique_lists:
  acl_remark_summary_list.append('                                            ')
  acl_remark_summary_list.append('-------------- Summarized ACL --------------')
  for j in i[k]:
    acl_remark_summary_list.append('access-list ' + ' '.join(filter(None, i[k].values())).replace(' '.join(filter(None, i[k].values())).split(' ')[-1], str(set(new_remark[k])).replace('{', '').replace('}', '')))
    acl_remark_summary_list.append('                                            ')	
    break

# Summarize Standard Type ACLs
acl_standard_summary_list = []
acl_standard_non_summary_list = []
acl_name_type_std_unique = sorted(set([d['acl_name'] for d in acl_type_std]))
acl_name_type_std_unique_lists = [[] for i in range(len(acl_name_type_std_unique))]
j = 0
for i in acl_name_type_std_unique:
  acl_name_type_std_unique_lists[j] = [d for d in acl_type_std if d['acl_name'] == i]
  j += 1

x = 0
for acl_list in acl_name_type_std_unique_lists:
  acl_standard(acl_name_type_std_unique_lists[x])
  x += 1

# Write to file
os.chdir(os.path.join(os.environ['HOME'], "KIaI_Tool_Build", "param", param1, "results"))
with open('ACL_Non_Summarize_Results_' + param1 + '.txt', 'w') as f:
  for i in acl_remark_non_summary_list:
    if type(i) == str:
      f.write("%s\r\n" % i)
    elif type(i) == dict:
      j = 'access-list ' + ' '.join(filter(None, i.values()))
      f.write("%s\r\n" % j)

os.chdir(os.path.join(os.environ['HOME'], "KIaI_Tool_Build", "param", param1, "results"))
with open('ACL_Summarize_Results_' + param1 + '.txt', 'w') as f:
  for i in acl_remark_summary_list:
    f.write("%s\r\n" % i)

os.chdir(os.path.join(os.environ['HOME'], "KIaI_Tool_Build", "param", param1, "results"))
with open('ACL_Non_Summarize_Results_' + param1 + '.txt', 'a') as f:
  for i in acl_standard_non_summary_list:
    f.write("%s\r\n" % i)

os.chdir(os.path.join(os.environ['HOME'], "KIaI_Tool_Build", "param", param1, "results"))
with open('ACL_Summarize_Results_' + param1 + '.txt', 'a') as f:
  for i in acl_standard_summary_list:
    f.write("%s\r\n" % i)

