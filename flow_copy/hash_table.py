#! /usr/bin/python3

import hashlib
import ipaddress

SIP_DIP_SAME=0
SIP_DIP_OPPO=1

#global value
flow_idx=0

class Five_Tuple:
    def __init__(self,sip,dip,proto,sport,dport):
        self.sip=sip
        self.dip=dip
        self.proto=proto
        self.sport=sport
        self.dport=dport
        md5=hashlib.md5()
        md5.update(str(int(ipaddress.ip_address(self.sip))^int(ipaddress.ip_address(self.dip))).encode('utf-8'))
        md5.update(str(self.sport^self.dport).encode('utf-8'))
        md5.update(str(proto).encode('utf-8'))
        self.hash_value = md5.hexdigest()
    def __repr__(self):
        return "<sip:{0},dip:{1},proto:{2},sport:{3},dport:{4}>".format(self.sip,self.dip,self.proto,self.sport,self.dport)

class HashTable:
    def __init__(self,size=10000):
        global flow_idx
        flow_idx=0
        self.size=size
        self.L=[HashList(i) for i in range(self.size)]
    def myhash(self,hash_value):
        return int(hash_value,base=16)%self.size
    def get_flow_cnt(self):
        flow_cnt=0
        for i in range(len(self.L)):
            flow_cnt+=self.L[i].flow_cnt
        return flow_cnt
    def five_tuple_cmp(self,t1,t2):
        if t1.sip==t2.sip and t1.dip==t2.dip and t1.sport==t2.sport and t1.dport==t2.dport and t1.proto==t2.proto:
            return True
        if t1.sip==t2.dip and t1.dip==t2.sip and t1.sport==t2.dport and t1.dport==t2.sport and t1.proto==t2.proto:
            return True
        return False
    def insert(self,five_tuple):
        hash_index,Lnode=self.find(five_tuple)
        if Lnode:
            cur_node=Lnode.head
        else:
            cur_node=None
        depth=0
        while cur_node:
            if self.five_tuple_cmp(cur_node.item,five_tuple):
                break
            cur_node=cur_node.next
            depth=depth+1
        if cur_node:
            if cur_node.item.sip==five_tuple.sip:
                return cur_node.idx,depth,SIP_DIP_SAME
            elif cur_node.item.sip==five_tuple.dip:
                return cur_node.idx,depth,SIP_DIP_OPPO
            else:
                print("SOMETHINE BAD HAPPENS!\n")
        else:
            hash_index=self.myhash(five_tuple.hash_value)
            idx,depth=self.L[hash_index].append(five_tuple)
            return idx,depth,SIP_DIP_SAME
    def find(self,five_tuple):
        hash_index=self.myhash(five_tuple.hash_value)
        node=self.L[hash_index]
        if node:
            return node.hash_index,node
        else:
            return -1,None
    def __iter__(self):
        return (self.L[i] for i in range(len(self.L)))
    def __repr__(self):
        return '******\n' + '\n'.join(map(str, self)) + '\n*******\n'

class HashList:
    class Node:
        def __init__(self,item,idx):
            self.item=item
            self.next=None
            self.idx=idx
        def __str__(self):
            return str(self.item)
    class NodeIterator:
        def __init__(self,node):
            self.node=node
        def __next__(self):
            if self.node:
                cur_node=self.node
                self.node=cur_node.next
                return cur_node.item
            else:
                raise StopIteration
        def __iter__(self):
            return self

    def __init__(self,hash_index):
        self.flow_cnt=0
        self.hash_index=hash_index
        self.head=None
        self.tail=None
    def __repr__(self):
        if self.head:
            return 'bucket {0} :'.format(self.hash_index)+'->'.join(map(str , self.NodeIterator(self.head)))
        else:
            return 'bucket {0} :empty!'.format(self.hash_index)
    def append(self,obj):
        global flow_idx
        flow_idx+=1
        node = HashList.Node(obj,flow_idx)
        self.flow_cnt+=1
        if not self.head:
            self.head=node
            self.tail=node
            return flow_idx,self.flow_cnt-1
        else:
            self.tail.next=node
            self.tail=node
            return flow_idx,self.flow_cnt-1


if __name__ == "__main__":
    h=HashTable()
    ip1="192.168.3.1"
    ip2="192.168.4.1"
    ip3="192.168.5.1"
    sport=1234
    dport=4321
    proto=6
    t1=Five_Tuple(ip1,ip2,proto,sport,dport)
    t2=Five_Tuple(ip2,ip1,proto,dport,sport)
    t3=Five_Tuple(ip1,ip3,proto,sport,dport)
    h.insert(t1)
    h.insert(t2)
    h.insert(t3)
    print(h)
