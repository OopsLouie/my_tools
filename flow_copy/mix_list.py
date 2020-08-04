#! /usr/bin/python3
from random import randint
from copy import deepcopy

global_max_pick_num=3

def mix_list(list_in_list,dont_mix):
    if dont_mix:
        final_list=[]
        for i in range(len(list_in_list)):
            final_list+=list_in_list[i]
        return final_list
    else:
        ll=deepcopy(list_in_list)
        final_list=[]
        total_list_num=len(ll)
        list_index=[i for i in range(total_list_num)]
        while len(list_index):
            need_delete_index=[]
            for i in range(len(list_index)):
                max_pick_num=len(ll[list_index[i]])
                if max_pick_num > global_max_pick_num:
                    max_pick_num=global_max_pick_num
                pic_num=randint(1,max_pick_num)
                for j in range(pic_num):
                    final_list.append(ll[list_index[i]].pop(0))
                if len(ll[list_index[i]]):
                    continue
                else:
                    need_delete_index.append(list_index[i])
            while need_delete_index:
                list_index.remove(need_delete_index.pop(0))
        return final_list


if __name__=="__main__":
    l1=[1,2,3,4,5,6,7]
    l2=['a','b','c','d','e','f','g']
    l3=['!','@','#','$','%','^','&']
    ll=[l1,l2,l3]
    print(ll)
    final_list=mix_list(ll)
    print(final_list)
