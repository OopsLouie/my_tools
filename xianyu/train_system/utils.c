#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#include "utils.h"
#include "types.h"

int use_time_static = 0;
struct tm time_now;
struct tm time_static;

// do not consider date anymore
//struct tm time_thirty_days_later;

int timestr_to_minutes(char * time_str) {
    char *p;
    int hours;
    int minutes;
    sscanf(time_str, "%d:%d", &hours, &minutes);
    return hours * 60 + minutes;
}

void minutes_to_timestr(int minutes, char * time_str) {
    sprintf(time_str, "%02d:%02d", (minutes - minutes % 60)/ 60, minutes % 60);
    return;
}

/* 0 based index */
int seatstr_to_index(char * seatstr) {
    char tmp[MAX_SEAT_IDX_LEN];
    memcpy(tmp, seatstr, MAX_SEAT_IDX_LEN);
    int remainder;
    switch(tmp[2]) {
        case 'A':case 'a':
            remainder = 1;break;
        case 'B':case 'b':
            remainder = 2;break;
        case 'C':case 'c':
            remainder = 3;break;
        case 'D':case 'd':
            remainder = 4;break;
        case 'F':case 'f':
            remainder = 5;break;
    }
    return ((tmp[0] - '0') * 10 + (tmp[1] - '0') - 1) * 5 + remainder - 1;
}

/* 0 based index */
void index_to_seatstr(int index, char * seatstr) {
    char c;
    switch((index % 5)) {
        case 0: c = 'A';break;
        case 1: c = 'B';break;
        case 2: c = 'C';break;
        case 3: c = 'D';break;
        case 4: c = 'F';break;
    }
    sprintf(seatstr, "%02d%C", ((index - index % 5) / 5 ) + 1, c);
}

/* 0 based index */
int get_train_index_by_train_idx(char * train_idx) {
    int i;
    for (i = 0;i < train_system.train_num;i++) {
        if (strcmp(train_system.train_infos[i].train_idx, train_idx) == 0) {
            return i;
        }
    }
    return -1;
}

static void my_flush() {
    char c;
    while ((c = getchar()) != '\n') ;   //从缓冲区清除多余字符
}

#if 0
// do not consider date anymore
static void count_thirty_days_later(struct tm * now, struct tm * after) {
    time_t t1;
    struct tm * tmp;
    t1 = mktime(now);
    t1 += 30 * 24 * 60 * 60 + 8 * 60 * 60;
    tmp = gmtime(&t1);
    memcpy(after, tmp, sizeof(struct tm));
    return;
}
#endif

void change_time() {
    char select;
    printf("请输入你想要的时间格式:\n1. 计算机时间\n2. 固定时间\n输入序号:\n");
    scanf("%c",&select);
    my_flush();
    if (select == '1') {
        use_time_static = 0;
        printf("时间设置为从计算机自动获取时间，3秒后自动返回主菜单\n");
        sleep(3);
        return;
    } else if (select == '2') {
        int hour;
        int minute;
        printf("请按正确格式输入时间(Hour:Minute):");
        if(scanf("%d:%d",&hour,&minute) == 2) {
            my_flush();
            time_static.tm_hour = hour - 8;
            time_static.tm_min = minute;
            use_time_static = 1;
            printf("设置成功，3秒后自动返回主菜单\n");
            sleep(3);
            return;
        } else {
            printf("格式错误，请再次尝试，3秒后自动返回主菜单\n");
            sleep(3);
        }
    } else {
        printf("格式错误，请再次尝试，3秒后自动返回主菜单\n");
        sleep(3);
        return;
    }
}

void buy_ticket() {
    int ticket_num;
    int i;
    int year;
    int month;
    int day;
    int train_index;
    char start_station[MAX_STATION_NAME_LEN];
    char end_station[MAX_STATION_NAME_LEN];
    char available_train[MAX_TRAIN_NUM][MAX_TRAIN_IDX_LEN];
    int available_train_num = 0;
    int seats[MAX_TICKETS_PER_TRADE];
    char seats_str[MAX_TICKETS_PER_TRADE][MAX_SEAT_IDX_LEN];
    printf("请输入您要购买的车票数量(根据法律规定单人最多可以用5张不同的身份证买5张火车票)\n:");
    if(scanf("%d",&ticket_num) != 1) {
        printf("格式错误，请再次尝试，3秒后自动返回主菜单\n");
        sleep(3);
        return;
    }
    if (ticket_num > 5) {
        printf("单次购票最多五张，请再次尝试，3秒后自动返回主菜单\n");
        sleep(3);
    }
    printf("请输入出发地\n:");
    scanf("%s",start_station);
    printf("请输入目的地\n:");
    scanf("%s",end_station);

    printf("\n从 %s 出发 前往 %s，共%d人\n",start_station,end_station,ticket_num);

    if(search_train_with_start_and_end(start_station, end_station, ticket_num, available_train, &available_train_num)) {
        printf("未找到可选车辆，3秒后自动返回主菜单\n");
        sleep(3);
        return;
    }

    if(choose_train(available_train, available_train_num)) {
        printf("选车失败，3秒后自动返回主菜单\n");
        sleep(3);
        return;
    } else {
        printf("您已选择 %s 次列车\n",available_train[0]);
    }

    search_train_and_print(available_train[0]);
    train_index = get_train_index_by_train_idx(available_train[0]);

    if(found_seat(available_train[0], seats, ticket_num)) {
        printf("选座失败，本列车无可坐席位，3秒后自动返回主菜单\n");
        sleep(3);
        return;
    }
    for (i = 0;i < ticket_num;i++) {
        index_to_seatstr(seats[i], seats_str[i]);
    }
    //record
    for (i = 0;i<ticket_num;i++) {
        // set people_system
        printf("请输入第%d位乘客的姓名:\n",i + 1);
        scanf("%s", people_system.people_infos[people_system.people_num].name);
        my_flush();
        printf("请输入第%d位乘客的身份证号:\n",i + 1);
        scanf("%s", people_system.people_infos[people_system.people_num].id);
        my_flush();
        sprintf(people_system.people_infos[people_system.people_num].train_idx, "%s", available_train[0]);
        sprintf(people_system.people_infos[people_system.people_num].seat_idx, "%s", seats_str[i]);
        sprintf(people_system.people_infos[people_system.people_num].start_station, "%s", start_station);
        sprintf(people_system.people_infos[people_system.people_num].end_station, "%s", end_station);
        // set train_system
        sprintf(train_system.train_infos[train_index].people_id[seats[i]], "%s", people_system.people_infos[people_system.people_num].id);
        train_system.train_infos[train_index].booked_seats_num ++;

        //output
        printf("\n\n乘客 %s 的座位位于 %s\n\n", people_system.people_infos[people_system.people_num].name, people_system.people_infos[people_system.people_num].seat_idx);
        // add variables
        people_system.people_num ++;
    }
    printf("输入回车返回主菜单");
    getchar();
}

int search_train_with_start_and_end(char * start_station, char * end_station, int people_num, char available_train[MAX_TRAIN_NUM][MAX_TRAIN_IDX_LEN], int * available_train_num) {
    int minutes_now;
    int i,j;
    int found_start;
    int found_end;
    int found_train_num = 0;
    char start_time[10];
    char end_time[10];
    train_info_t * train_info_ptr;
    if(use_time_static) {
        minutes_now = (time_static.tm_hour + 8) * 60 + time_static.tm_min;
    } else {
        minutes_now = (time_now.tm_hour + 8) * 60 + time_now.tm_min;
    }
    for (i=0;i<train_system.train_num;i++) {
        found_start = 0;
        found_end = 0;
        memset(start_time, 0 , 10);
        memset(end_time, 0 , 10);
        train_info_ptr = &train_system.train_infos[i];
        for (j=0;j<train_info_ptr->station_num;j++) {
            if(!found_start) {
                if(strcmp(train_info_ptr->start_station[j],start_station) == 0) {
                    if(minutes_now >= train_info_ptr->start_time[j] - 30) {
                        break;
                    }
                    minutes_to_timestr(train_info_ptr->start_time[j], start_time);
                    found_start = 1;
                    j--;
                    continue;
                }
            } else {
                if(strcmp(train_info_ptr->end_station[j],end_station) == 0) {
                    minutes_to_timestr(train_info_ptr->end_time[j], end_time);
                    found_end = 1;
                    break;
                }
            }
        }
        if(found_start && found_end) {
            printf("可选列车 %s 由 %s 开往 %s，%s 从 %s出发，%s 到达 %s\n", train_info_ptr->train_idx, train_info_ptr->start_station[0], train_info_ptr->end_station[train_info_ptr->station_num - 1], start_time, start_station, end_time, end_station);
            sprintf(available_train[found_train_num], "%s", train_info_ptr->train_idx);
            found_train_num ++;
        }
    }
    *available_train_num = found_train_num;
    if(found_train_num) {
        return 0;
    } else {
        return -1;
    }
}

void search_train() {
    char train_idx[MAX_TRAIN_IDX_LEN];
    printf("请输入你想搜索的列车编号,输入ALL显示所有\n:");
    scanf("%s", train_idx);
    my_flush();
    if(train_idx[0] == 'A' && train_idx[1] == 'L' && train_idx[2] == 'L') {
        if(search_train_and_print(NULL)) {
            printf("找不到该列车，3秒后自动返回主菜单\n");
            sleep(3);
            return;
        }
    } else {
        if(search_train_and_print(train_idx)) {
            printf("搜索列车失败，3秒后自动返回主菜单\n");
            sleep(3);
            return;
        }
    }
    printf("输入回车返回主菜单");
    getchar();
    return;
}

int search_train_and_print(char * train_idx) {
    if (train_idx) {
        int i,j;
        char buf[1024];
        char start_time[10];
        char end_time[10];
        char middle_time[10];
        train_info_t * train_info_ptr;
        i = get_train_index_by_train_idx(train_idx);
        if (i == -1) {
            return -1;
        }
        train_info_ptr = &train_system.train_infos[i];
        minutes_to_timestr(train_info_ptr->start_time[0], start_time);
        minutes_to_timestr(train_info_ptr->end_time[train_info_ptr->station_num - 1], end_time);
        sprintf(buf, "列车 %s 由 %s 开往 %s， 开点: %s , 到点: %s, 途径:", train_info_ptr->train_idx, train_info_ptr->start_station[0], train_info_ptr->end_station[train_info_ptr->station_num - 1], start_time, end_time);
        for(j = 0;j < train_info_ptr->station_num - 1;j ++) {
            memset(middle_time, 0, 10);
            minutes_to_timestr(train_info_ptr->start_time[j + 1], middle_time);
            strcat(buf, " ");
            strcat(buf, train_info_ptr->end_station[j]);
            strcat(buf, "(开点:");
            strcat(buf, middle_time);
            strcat(buf, ")");
        }
        strcat(buf, ".");
        printf("%s\n", buf);
        printf("仍有余票 %d 张\n", train_info_ptr->total_seats_num - train_info_ptr->booked_seats_num);
        printf("    A  B  C  | D  F\n");
        for(j = 0;j < train_info_ptr->total_seats_num; j++) {
            if (j % 5 == 0) {
                printf("%02d  ", (j - j % 5) / 5 + 1);
            }
            if (strlen(train_info_ptr->people_id[j])) {
                i --;
                printf("■  ");
            } else {
                printf("□  ");
            }
            if (j % 5 == 2) {
                printf("| ");
            }
            if (j % 5 == 4) {
                printf("\n");
            }
        }
        return 0;
    } else {
        int i,j;
        char buf[1024];
        char start_time[10];
        char end_time[10];
        char middle_time[10];
        train_info_t * train_info_ptr;
        printf("\n今日车次:\n");
        for(i = 0; i < train_system.train_num; i++) {
            train_info_ptr = &train_system.train_infos[i];
            minutes_to_timestr(train_info_ptr->start_time[0], start_time);
            minutes_to_timestr(train_info_ptr->end_time[train_info_ptr->station_num - 1], end_time);
            sprintf(buf, "列车 %s 由 %s 开往 %s， 开点: %s , 到点: %s, 仍有余票 %d 张, 途径:", train_info_ptr->train_idx, train_info_ptr->start_station[0], train_info_ptr->end_station[train_info_ptr->station_num - 1], start_time, end_time, train_info_ptr->total_seats_num-train_info_ptr->booked_seats_num);
            for(j = 0;j < train_info_ptr->station_num - 1;j ++) {
                memset(middle_time, 0, 10);
                minutes_to_timestr(train_info_ptr->start_time[j + 1], middle_time);
                strcat(buf, " ");
                strcat(buf, train_info_ptr->end_station[j]);
                strcat(buf, "(开点:");
                strcat(buf, middle_time);
                strcat(buf, ")");
            }
            strcat(buf, ".");
            printf("%s\n", buf);
        }
        return 0;
    }
}

int choose_train(char available_train[MAX_TRAIN_NUM][MAX_TRAIN_IDX_LEN], int available_train_num) {
    char input[1024];
    int i;
    printf("请输入你要选择的车次\n:");
    scanf("%s",input);
    my_flush();
    for(i = 0;i < available_train_num;i++) {
        if (strcmp(available_train[i], input) == 0) {
            memcpy(available_train[0], available_train[i], MAX_TRAIN_IDX_LEN);
            return 0;
        }
    }
    return -1;
}

void search_people() {
    int i,j;
    int train_index;
    char name[MAX_NAME_LEN];
    char id[MAX_ID_LEN];
    char start_time[10];
    people_info_t * people_info_ptr;
    train_info_t * train_info_ptr;
    printf("请输入乘客姓名\n:");
    scanf("%s", name);
    my_flush();
    printf("请输入乘客身份证号码\n:");
    scanf("%s", id);
    my_flush();
    for (i = 0;i < people_system.people_num; i ++) {
        people_info_ptr = &people_system.people_infos[i];
        if (strcmp(people_info_ptr->name,name) == 0 &&
            strcmp(people_info_ptr->id,id) == 0) {
            printf("乘客 %s 身份证号 %s 乘坐 %s  从 %s 出发 前往 %s 座位号 %s\n", people_info_ptr->name,
                                                                         people_info_ptr->id,
                                                                         people_info_ptr->train_idx,
                                                                         people_info_ptr->start_station,
                                                                         people_info_ptr->end_station,
                                                                         people_info_ptr->seat_idx);
            train_index = get_train_index_by_train_idx(people_info_ptr->train_idx);
            train_info_ptr = &train_system.train_infos[train_index];
            for(j = 0;j < train_info_ptr->station_num;j++) {
                if (strcmp(train_info_ptr->start_station[j], people_info_ptr->start_station) == 0) {
                    minutes_to_timestr(train_info_ptr->start_time[j], start_time);
                    printf("您的车将于 %s 发车,请做好准备!!!\n", start_time);
                    return;
                }
            }
            printf("程序发生严重错误,乘客信息有误!!!\n");
        }
    }
    printf("未找到乘客信息,3秒后自动返回主菜单\n");
    sleep(3);
    return;
}

/* 1人搜AC,没有再搜DF
 * 2人搜DF,没有再搜ABC
 * 3人搜ABC
 * 4人搜ABCDF
 * 5人搜ABCDF
 * 座位从头占到尾，不考虑不同区间坐不同人
 */
int found_seat(char * train_idx, int seats[MAX_TICKETS_PER_TRADE], int ticket_num) {
    int train_index,i;
    train_info_t * train_info_ptr;
    train_index = get_train_index_by_train_idx(train_idx);
    train_info_ptr = &train_system.train_infos[train_index];
    if (ticket_num == 5 || ticket_num == 4) {
        for(i = 0;i < train_info_ptr->total_seats_num / 5;i ++) {
            if (strlen(train_info_ptr->people_id[5 * i + 0]) == 0 &&
                strlen(train_info_ptr->people_id[5 * i + 1]) == 0 &&
                strlen(train_info_ptr->people_id[5 * i + 2]) == 0 &&
                strlen(train_info_ptr->people_id[5 * i + 3]) == 0 &&
                strlen(train_info_ptr->people_id[5 * i + 4]) == 0) {
                seats[0] = 5 * i + 0;
                seats[1] = 5 * i + 1;
                seats[2] = 5 * i + 2;
                seats[3] = 5 * i + 3;
                if(ticket_num == 5) {
                    seats[4] = 5 * i + 4;
                }
                return 0;
            }
        }
        return -1;
    } else if (ticket_num == 3) {
        for(i = 0;i < train_info_ptr->total_seats_num / 5;i ++) {
            if (strlen(train_info_ptr->people_id[5 * i + 0]) == 0 &&
                strlen(train_info_ptr->people_id[5 * i + 1]) == 0 &&
                strlen(train_info_ptr->people_id[5 * i + 2]) == 0) {
                seats[0] = 5 * i + 0;
                seats[1] = 5 * i + 1;
                seats[2] = 5 * i + 2;
                return 0;
            }
        }
        return -1;
    } else if (ticket_num == 2) {
        for(i = 0;i < train_info_ptr->total_seats_num / 5;i ++) {
            if (strlen(train_info_ptr->people_id[5 * i + 3]) == 0 &&
                strlen(train_info_ptr->people_id[5 * i + 4]) == 0) {
                seats[0] = 5 * i + 3;
                seats[1] = 5 * i + 4;
                return 0;
            }
        }
        for(i = 0;i < train_info_ptr->total_seats_num / 5;i ++) {
            if (strlen(train_info_ptr->people_id[5 * i + 0]) == 0 &&
                strlen(train_info_ptr->people_id[5 * i + 1]) == 0 &&
                strlen(train_info_ptr->people_id[5 * i + 2]) == 0) {
                seats[0] = 5 * i + 0;
                seats[1] = 5 * i + 1;
                return 0;
            }
        }
        return -1;
    } else if (ticket_num == 1) {
        for(i = 0;i < train_info_ptr->total_seats_num / 5;i ++) {
            if (strlen(train_info_ptr->people_id[5 * i + 1]) != 0) continue;
            if (strlen(train_info_ptr->people_id[5 * i + 0]) == 0) {
                seats[0] = 5 * i + 0;
                return 0;
            }
            if (strlen(train_info_ptr->people_id[5 * i + 2]) == 0) {
                seats[0] = 5 * i + 2;
                return 0;
            }
        }
        for(i = 0;i < train_info_ptr->total_seats_num / 5;i ++) {
            if (strlen(train_info_ptr->people_id[5 * i + 3]) == 0 &&
                strlen(train_info_ptr->people_id[5 * i + 4]) == 0) {
                seats[0] = 5 * i + 3;
                return 0;
            }
        }
        return -1;
    }
    return -1;
}

void refund_ticket() {
    char name[MAX_NAME_LEN];
    char id[MAX_ID_LEN];
    char train_idx[MAX_TRAIN_IDX_LEN];
    char seat_idx[MAX_SEAT_IDX_LEN];

    printf("请输入待退票乘客名\n:");
    scanf("%s", name);
    my_flush();
    printf("请输入待退票乘客身份证号\n:");
    scanf("%s", id);
    my_flush();

    printf("1\n");
    if (get_train_info_by_name_and_id(name, id, train_idx, seat_idx)) {
        printf("未找到该乘客，3秒后自动返回主菜单\n");
        sleep(3);
        return;
    }
    delete_people(name, id);
    delete_seat_from_train(train_idx, seat_idx);
    return;
}

int get_train_info_by_name_and_id(char * name, char * id, char * train_idx, char * seat_idx) {
    int i;
    people_info_t * people_info_ptr;
    for (i = 0;i < people_system.people_num;i ++) {
        people_info_ptr = &people_system.people_infos[i];
        if (strcmp(people_info_ptr->name, name) == 0 &&
            strcmp(people_info_ptr->id, id) == 0) {
            sprintf(train_idx, people_info_ptr->train_idx);
            sprintf(seat_idx, people_info_ptr->seat_idx);
            return 0;
        }
    }
    return -1;
}

void delete_people(char * name, char * id) {
    int i;
    int have_found = 0;
    people_info_t * people_info_ptr;
    for (i = 0;i < people_system.people_num;i ++) {
        people_info_ptr = &people_system.people_infos[i];
        if(have_found) {
            memcpy(&people_system.people_infos[i - 1], &people_system.people_infos[i], sizeof(people_info_t));
        } else {
            if (strcmp(people_info_ptr->name, name) == 0 &&
                strcmp(people_info_ptr->id, id) == 0) {
                have_found = 1;
            }
        }
    }
    people_system.people_num--;
    return;
}
void delete_seat_from_train(char * train_idx, char * seat_str) {
    int train_index;
    int seat_index;
    train_info_t * train_info_ptr;
    train_index = get_train_index_by_train_idx(train_idx);
    seat_index = seatstr_to_index(seat_str);
    train_info_ptr = &train_system.train_infos[train_index];
    memset(train_info_ptr->people_id[seat_index], 0, sizeof(MAX_ID_LEN));
    train_info_ptr->booked_seats_num --;
    return;
}

int get_people_index_by_name_and_id(char * name, char * id) {
    int i;
    people_info_t * people_info_ptr;
    for(i = 0;i < people_system.people_num; i++) {
        people_info_ptr = &people_system.people_infos[i];
        if( strcmp(people_info_ptr->name, name) == 0 &&
            strcmp(people_info_ptr->id, id) == 0) {
            return i;
        }
    }
    return -1;
}

void rebook() {
    char name[MAX_NAME_LEN];
    char id[MAX_ID_LEN];
    char start_station[MAX_STATION_NAME_LEN];
    char end_station[MAX_STATION_NAME_LEN];
    char old_train_idx[MAX_STATION_NAME_LEN];
    int train_index;
    int people_index;
    char old_seat_idx[MAX_SEAT_IDX_LEN];
    char seat_idx[MAX_SEAT_IDX_LEN];
    char available_train[MAX_TRAIN_NUM][MAX_TRAIN_IDX_LEN];
    int available_train_num = 0;
    int seats[MAX_TICKETS_PER_TRADE];
    char seats_str[MAX_TICKETS_PER_TRADE][MAX_SEAT_IDX_LEN];

    printf("请输入待改签乘客名\n");
    scanf("%s", name);
    my_flush();
    printf("请输入待改签乘客身份证\n");
    scanf("%s", id);
    my_flush();
    if(get_train_info_by_name_and_id(name, id, old_train_idx, old_seat_idx)) {
        printf("未找到该乘客，3秒后自动返回主菜单\n");
        sleep(3);
        return;
    }
    printf("请输入改签出发地\n:");
    scanf("%s", start_station);
    my_flush();
    printf("请输入改签目的地\n:");
    scanf("%s", end_station);
    my_flush();

    printf("\n从 %s 出发 前往 %s\n",start_station,end_station);

    if(search_train_with_start_and_end(start_station, end_station, 1, available_train, &available_train_num)) {
        printf("未找到可选车辆，3秒后自动返回主菜单\n");
        sleep(3);
        return;
    }

    if(choose_train(available_train, available_train_num)) {
        printf("选车失败，3秒后自动返回主菜单\n");
        sleep(3);
        return;
    } else {
        printf("您已选择 %s 次列车\n",available_train[0]);
    }

    search_train_and_print(available_train[0]);
    train_index = get_train_index_by_train_idx(available_train[0]);

    if(found_seat(available_train[0], seats, 1)) {
        printf("选座失败，本列车无可坐席位，3秒后自动返回主菜单\n");
        sleep(3);
        return;
    }
    index_to_seatstr(seats[0], seats_str[0]);

    // 改变乘客原有信息
    people_index = get_people_index_by_name_and_id(name, id);
    sprintf(people_system.people_infos[people_index].train_idx, "%s", available_train[0]);
    sprintf(people_system.people_infos[people_index].seat_idx, "%s", seats_str[0]);
    sprintf(people_system.people_infos[people_index].start_station, "%s", start_station);
    sprintf(people_system.people_infos[people_index].end_station, "%s", end_station);

    // 原车删除座位占用
    delete_seat_from_train(old_train_idx, old_seat_idx);
    // 新车增加座位占用
    sprintf(train_system.train_infos[train_index].people_id[seats[0]], "%s", id);
    printf("改签成功！新座位位于 %s\n", seats_str[0]);

    printf("输入回车返回主菜单");
    getchar();

    return;

}

void paintmenu()
{
    time_t now_time;
    struct tm *tp;
    while(1)
    {
        char select;
        do{
            //system("clear");//清屏
            time(&now_time);
            tp = gmtime(&now_time);
            memcpy(&time_now, tp, sizeof(struct tm));
            printf("\n\t ╭════╮ ┌════════┐ ┌══════════┐ ┌══════════┐");
            printf("\n\t╭╯╭　 ║═║  列车  ║═║   售票   ║═║   系统   ║");
            printf("\n\t╰⊙═⊙═⊙╯ └⊙═⊙═⊙═⊙...└⊙═⊙═⊙═⊙═~...└⊙═⊙═⊙═⊙=⊙~");
            if (use_time_static) {
                printf("\n\t 现在是北京时间 %02d:%02d",8+time_static.tm_hour,time_static.tm_min);
                //count_thirty_days_later(&time_now, &time_thirty_days_later);
                //原考虑日期，现精简不予考虑
                //printf("\n\t 现在是北京时间%d.%02d.%02d %02d:%02d:%02d",1900+time_now.tm_year,1+time_now.tm_mon,time_now.tm_mday,8+time_now.tm_hour,time_now.tm_min,time_now.tm_sec);
                //printf("\n\t 可购票时间截至%d.%02d.%02d %02d:%02d:%02d",1900+time_thirty_days_later.tm_year,1+time_thirty_days_later.tm_mon,time_thirty_days_later.tm_mday,8+time_thirty_days_later.tm_hour,time_thirty_days_later.tm_min,time_thirty_days_later.tm_sec);
            } else {
                printf("\n\t 现在是北京时间 %02d:%02d",8+time_now.tm_hour,time_now.tm_min);
                //count_thirty_days_later(&time_now, &time_thirty_days_later);
                //printf("\n\t 现在是北京时间%d.%02d.%02d %02d:%02d:%02d",1900+time_now.tm_year,1+time_now.tm_mon,time_now.tm_mday,8+time_now.tm_hour,time_now.tm_min,time_now.tm_sec);
                //printf("\n\t 可购票时间截至%d.%02d.%02d %02d:%02d:%02d",1900+time_thirty_days_later.tm_year,1+time_thirty_days_later.tm_mon,time_thirty_days_later.tm_mday,8+time_thirty_days_later.tm_hour,time_thirty_days_later.tm_min,time_thirty_days_later.tm_sec);
            }
            printf("\n\t ┌═════════════════════════════════════════┐");
            printf("\n\t ║1.设置时间                               │");
            printf("\n\t ║2.售票                                   │");
            printf("\n\t ║3.退票                                   │");
            printf("\n\t ║4.改签                                   │");
            printf("\n\t ║5.查询列车                               │");
            printf("\n\t ║6.查询用户                               │");
            printf("\n\t ║7.保存                                   │");
            printf("\n\t ║0.退出                                   │");
            printf("\n\t └⊙═⊙═⊙═⊙═⊙═⊙═⊙═⊙=⊙═⊙═⊙═⊙═⊙═⊙═⊙═⊙═⊙═⊙═⊙═⊙═⊙┘");
            printf("\n\t 请选择：");
            select=getchar();                   //等待用户输入数据
            my_flush();
        } while (select<'0'||select>'8');

        switch(select)
        {
            case '0':return;
            case '1':change_time();break;
            case '2':buy_ticket();break;
            case '3':refund_ticket();break;
            case '4':rebook();break;
            case '5':search_train();break;
            case '6':search_people();break;
            case '7':write_peoples_to_file();break;
            default:break;
        }
    }
}
