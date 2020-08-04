#! /usr/bin/python3

from change_five_tuple import create_flow_one_to_n,read_flow
from hash_table import HashTable
from scapy.all import rdpcap,wrpcap
from mix_list import mix_list
import sys
import os


global_hash_bucket_num=65521
#global_flow_one_to_n=350
global_flow_one_to_n=8


global_http_file_name="./pkts/http.pcap"
global_dns_file_name="./pkts/dns.pcap"
global_ssh_file_name="./pkts/ssh.pcap"
global_other_file_name="./pkts/other.pcap"

global_output_file_name="./result_pkts/sm.pcap"

if __name__=="__main__":
    h=HashTable(global_hash_bucket_num)
    pkts_list=[]
    hash_pos_list=[]

    #read http
    print("start to read http")
    pkt=rdpcap(global_http_file_name)
    hash_pos=read_flow(h,pkt,0)
    pkts_list.append(pkt)
    hash_pos_list.append(hash_pos)
    print("read http finish!")

    #read dns
    print("start to read dns")
    pkt=rdpcap(global_dns_file_name)
    hash_pos=read_flow(h,pkt,0)
    pkts_list.append(pkt)
    hash_pos_list.append(hash_pos)
    print("read dns finish!")

    #read ssh
    print("start to read ssh")
    pkt=rdpcap(global_ssh_file_name)
    hash_pos=read_flow(h,pkt,0)
    pkts_list.append(pkt)
    hash_pos_list.append(hash_pos)
    print("read ssh finish!")


    #read other
    print("start to read other")
    pkt=rdpcap(global_other_file_name)
    hash_pos=read_flow(h,pkt,0)
    pkts_list.append(pkt)
    hash_pos_list.append(hash_pos)
    print("read other finish!")

    #create new pkts
    print("start to create pkts")
    final_pkts_inorder=[]
    for i in range(len(pkts_list)):
        final_pkts_inorder+=create_flow_one_to_n(pkts_list[i],hash_pos_list[i],True,global_flow_one_to_n,global_output_file_name)
    print("create pkts finish")



    #mix pkts
    dont_mix=0
    if dont_mix:
        print("start to combine not mix")
    else:
        print("start to mix pkts")
    final_pkts=mix_list(final_pkts_inorder,dont_mix)
    wrpcap(global_output_file_name,final_pkts)
    os.system("tcprewrite --fixcsum -i {0} -o {1}".format(global_output_file_name,"./result_pkts/sm_out.pcap"))
    os.system("mv ./result_pkts/sm_out.pcap {0}".format(global_output_file_name))
    pkts_list=[]
    hash_pos_list=[]
    final_pkts_inorder=[]
    final_pkts=[]
    print("create pkts finish")

    #check pkts
    print("start to check results")
    origin_flow_cnt=h.get_flow_cnt()
    h=HashTable(global_hash_bucket_num)
    pkt=rdpcap(global_output_file_name)
    read_flow(h,pkt,1)
    result_flow_cnt=h.get_flow_cnt()
    print("origin flow cnt is {0}".format(origin_flow_cnt))
    print("result flow cnt is {0}".format(result_flow_cnt))
    if origin_flow_cnt * global_flow_one_to_n == result_flow_cnt:
        print("check results finish")
    else:
        print("bad result!\n")
        sys.exit(1)

    print("all proc finish!\n\n\n")
