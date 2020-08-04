#! /usr/bin/python3

from scapy.all import *
from hash_table import Five_Tuple,HashTable,SIP_DIP_SAME,SIP_DIP_OPPO
from mix_list import mix_list
from copy import deepcopy
from ipaddress import ip_address,IPv4Address

global_hash_bucket_num=65521     #      < 255 * 255
global_need_output_together=True
global_need_check=True

# global_sip_start:  192.0.0.0 ~ 192.0.0.x+global_flow_one_to_n
global_sip_start=[int(ip_address('192.0.0.'+str(i))) for i in range(1,255)]

## global_sip_start:  192.0.0.0 ~ 192.0.0.x+global_flow_one_to_n
#global_sip_start=[int(ip_address('192.'+str(i)+'.0.0')) for i in range(255)]


def read_flow(h,pkts,is_check):
    if is_check:
        for i in range(len(pkts)):
            if pkts[i]["IP"].proto==6:
                t=Five_Tuple(pkts[i]["IP"].src,pkts[i]["IP"].dst,pkts[i]["IP"].proto,pkts[i]["TCP"].sport,pkts[i]["TCP"].dport)
            elif pkts[i]["IP"].proto==17:
                t=Five_Tuple(pkts[i]["IP"].src,pkts[i]["IP"].dst,pkts[i]["IP"].proto,pkts[i]["UDP"].sport,pkts[i]["UDP"].dport)
            else:
                print("SOMTHING BAD HAPPENS!\n")
            h.insert(t)
        return
    else:
        hash_pos_list=[]
        for i in range(len(pkts)):
            if pkts[i]["IP"].proto==6:
                t=Five_Tuple(pkts[i]["IP"].src,pkts[i]["IP"].dst,pkts[i]["IP"].proto,pkts[i]["TCP"].sport,pkts[i]["TCP"].dport)
            elif pkts[i]["IP"].proto==17:
                t=Five_Tuple(pkts[i]["IP"].src,pkts[i]["IP"].dst,pkts[i]["IP"].proto,pkts[i]["UDP"].sport,pkts[i]["UDP"].dport)
            else:
                print("SOMTHING BAD HAPPENS!\n")
            index,depth,sip_dip_status=h.insert(t)
            hash_pos_list.append([index,depth,sip_dip_status])
        return hash_pos_list

def change_ip_proc(ipv4_input_str,target_value):
    ip_array=ipv4_input_str.split('.')
    ip_array[1]=str(target_value)
    return '.'.join(ip_array)


def create_flow_one_to_n(pkts,hash_pos_list,need_output_together,flow_one_to_n,output_file_name):
    final_pkts_list=[]
    for j in range(flow_one_to_n):
        new_pkts=deepcopy(pkts)
        for i in range(len(new_pkts)):
            if hash_pos_list[i][2]==SIP_DIP_SAME:
                new_pkts[i]["IP"].src=str(IPv4Address((global_sip_start[j]+256*hash_pos_list[i][0])))
                new_pkts[i]["IP"].dst="223.168.3.151"
#                if pkts[i]["IP"].proto==6:
#                    if pkts[i]["TCP"].sport==80 or pkts[i]["TCP"].sport==8080:
#                        pass
#                    else:
#                        new_pkts[i]["TCP"].sport=(pkts[i]["TCP"].sport+hash_pos_list[i][1])%65536
#                    if pkts[i]["TCP"].dport==80 or pkts[i]["TCP"].dport==8080:
#                        pass
#                    else:
#                        new_pkts[i]["TCP"].dport=(pkts[i]["TCP"].dport+hash_pos_list[i][1])%65536
#                elif pkts[i]["IP"].proto==17:
#                    if pkts[i]["UDP"].sport==80 or pkts[i]["UDP"].sport==8080:
#                        pass
#                    else:
#                        new_pkts[i]["UDP"].sport=(pkts[i]["UDP"].sport+hash_pos_list[i][1])%65536
#                    if pkts[i]["UDP"].dport==80 or pkts[i]["UDP"].dport==8080:
#                        pass
#                    else:
#                        new_pkts[i]["UDP"].dport=(pkts[i]["UDP"].dport+hash_pos_list[i][1])%65536
#                else:
#                    printf("SOMETHING BAD HAPPENS!\n")
            elif hash_pos_list[i][2]==SIP_DIP_OPPO:
                new_pkts[i]["IP"].src="223.168.3.151"
                new_pkts[i]["IP"].dst=str(IPv4Address((global_sip_start[j]+256*hash_pos_list[i][0])))
#                if pkts[i]["IP"].proto==6:
#                    if pkts[i]["TCP"].sport==80 or pkts[i]["TCP"].sport==8080:
#                        new_pkts[i]["TCP"].sport=pkts[i]["TCP"].sport
#                    else:
#                        new_pkts[i]["TCP"].sport=(pkts[i]["TCP"].sport+hash_pos_list[i][1])%65536
#                    if pkts[i]["TCP"].dport==80 or pkts[i]["TCP"].dport==8080:
#                        new_pkts[i]["TCP"].dport=pkts[i]["TCP"].dport
#                    else:
#                        new_pkts[i]["TCP"].dport=(pkts[i]["TCP"].dport+hash_pos_list[i][1])%65536
#                elif pkts[i]["IP"].proto==17:
#                    if pkts[i]["UDP"].sport==80 or pkts[i]["UDP"].sport==8080:
#                        new_pkts[i]["UDP"].sport=pkts[i]["UDP"].sport
#                    else:
#                        new_pkts[i]["UDP"].sport=(pkts[i]["UDP"].sport+hash_pos_list[i][1])%65536
#                    if pkts[i]["UDP"].dport==80 or pkts[i]["UDP"].dport==8080:
#                        new_pkts[i]["UDP"].dport=pkts[i]["UDP"].dport
#                    else:
#                        new_pkts[i]["UDP"].dport=(pkts[i]["UDP"].dport+hash_pos_list[i][1])%65536
#                else:
#                    printf("SOMETHING BAD HAPPENS!\n")
            else:
                print("SOMETHINE BAD HAPPENS\n")
        if not need_output_together:
            wrpcap(output_file_name.format(j),new_pkts)
        else:
            final_pkts_list.append(new_pkts)
    if need_output_together:
        return final_pkts_list
    else:
        return None

if __name__ == "__main__":
    h=HashTable(global_hash_bucket_num)
    pkts = rdpcap(global_file_name)
    hash_pos_list=read_flow(h,pkts,0)
    origin_flow_cnt=h.get_flow_cnt()
    print("total_flow_cnt is {0}".format(str(origin_flow_cnt)))

    with open("./output",'w') as f:
        f.write(str(h))
        f.write("total_flow_cnt is {0}".format(str(origin_flow_cnt)))

    final_pkts_list=create_flow_one_to_n(pkts,hash_pos_list,global_need_output_together,global_flow_one_to_n,global_output_file_name)

    if final_pkts_list:
        final_pkts=mix_list(final_pkts_list)
        wrpcap(global_output_file_name.format("n_in_one"),final_pkts)
        if global_need_check:
            h=HashTable(global_hash_bucket_num)
            pkts = rdpcap(global_output_file_name.format("n_in_one"))
            read_flow(h,pkts,1)
            check_flow_cnt=h.get_flow_cnt()
            print("copy flow ont to n cnt is {0}".format(global_flow_one_to_n))
            print("check_flow_cnt is {0}".format(str(check_flow_cnt)))
            if check_flow_cnt==global_flow_one_to_n*origin_flow_cnt:
                print("output is correct!\n")
            else:
                print("output is incorrect!\n")
    else:
        pass

