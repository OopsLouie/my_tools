#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#include "file_io.h"
#include "utils.h"
#include "types.h"


// make input and output different for test
char * input_trians = "trains.txt";
char * input_peoples = "peoples.txt";
char * output_trains = "trains_1.txt";
char * output_peoples = "peoples_1.txt";

int read_trains_from_file() {
    char * filename = input_trians;
    FILE * fp = NULL;
    char line[1024];
    memset(&train_system, 0 ,sizeof(train_system_t));
    fp = fopen(filename, "r");
    if(!fp) {
        fclose(fp);
        return -1;
    }
    while(1) {
        train_info_t * train_info_ptr = &train_system.train_infos[train_system.train_num++];
        train_info_ptr->total_seats_num = MAX_PEOPLE_PER_TRAIN;
        memset(line, 0, 1024);
        if(fgets(line, 1024, fp) == NULL) {
            train_system.train_num --;
            break;
        }
        // parse train info
        char * p;
        p = strtok(line, " ");
        sprintf(train_info_ptr->train_idx, "%s", p);
        p = strtok(NULL, " ");
        while(p) {
            sprintf(train_info_ptr->start_station[train_info_ptr->station_num], "%s", p);
            p = strtok(NULL, " ");

            train_info_ptr->start_time[train_info_ptr->station_num] = timestr_to_minutes(p);
            p = strtok(NULL, " ");

            sprintf(train_info_ptr->end_station[train_info_ptr->station_num], "%s", p);
            p = strtok(NULL, " ");

            train_info_ptr->end_time[train_info_ptr->station_num] = timestr_to_minutes(p);
            p = strtok(NULL, " ");
            train_info_ptr->station_num ++;
        }
    }
    fclose(fp);
    return 0;
}

int write_trains_to_file() {
    char * filename = output_trains;
    FILE * fp = NULL;
    char line[1024];
    char timestr[10];
    int i,j;
    fp = fopen(filename, "w");
    if(!fp) {
        fclose(fp);
        return -1;
    }
    for (i = 0;i < train_system.train_num;i ++) {
        memset(line, 0, 1024);
        sprintf(line, "%s",  train_system.train_infos[i].train_idx);
        for (j = 0;j < train_system.train_infos[i].station_num;j++) {
            strcat(line, " ");
            strcat(line, train_system.train_infos[i].start_station[j]);
            strcat(line, " ");
            memset(timestr, 0, 10);
            minutes_to_timestr(train_system.train_infos[i].start_time[j], timestr);
            strcat(line, timestr);
            strcat(line, " ");
            strcat(line, train_system.train_infos[i].end_station[j]);
            strcat(line, " ");
            memset(timestr, 0, 10);
            minutes_to_timestr(train_system.train_infos[i].end_time[j], timestr);
            strcat(line, timestr);
        }
        fprintf(fp, "%s\n", line);
    }
    fclose(fp);
    return 0;
}

int read_peoples_from_file() {
    char * filename = input_peoples;
    FILE * fp = NULL;
    char line[1024];
    train_info_t * train_info_ptr;
    memset(&people_system, 0 ,sizeof(people_system_t));
    fp = fopen(filename, "r");
    if(!fp) {
        fclose(fp);
        return -1;
    }
    while(1) {
        people_info_t * people_info_ptr = &people_system.people_infos[people_system.people_num++];
        memset(line, 0, 1024);
        if(fgets(line, 1024, fp) == NULL) {
            people_system.people_num --;
            break;
        }
        // parse train info
        char * p;
        p = strtok(line, " ");
        sprintf(people_info_ptr->name, "%s", p);
        p = strtok(NULL, " ");
        sprintf(people_info_ptr->id, "%s", p);
        p = strtok(NULL, " ");
        sprintf(people_info_ptr->train_idx, "%s", p);
        p = strtok(NULL, " ");
        sprintf(people_info_ptr->seat_idx, "%s", p);
        p = strtok(NULL, " ");
        sprintf(people_info_ptr->start_station, "%s", p);
        p = strtok(NULL, " ");
        // erase '\n'
        p[strlen(p) - 1] = '\0';
        sprintf(people_info_ptr->end_station, "%s", p);
        train_info_ptr = &train_system.train_infos[get_train_index_by_train_idx(people_info_ptr->train_idx)];
        train_info_ptr->booked_seats_num ++;
        sprintf(train_info_ptr->people_id[seatstr_to_index(people_info_ptr->seat_idx)], "%s", people_info_ptr->id);
    }
}

int write_peoples_to_file() {
    char * filename = output_peoples;
    FILE * fp = NULL;
    char line[1024];
    int i;
    people_info_t * people_info_ptr;
    fp = fopen(filename, "w");
    if(!fp) {
        fclose(fp);
        return -1;
    }
    for (i = 0;i < people_system.people_num;i ++) {
        people_info_ptr = &people_system.people_infos[i];
        memset(line, 0, 1024);
        sprintf(line, "%s %s %s %s %s %s", people_info_ptr->name,
                                           people_info_ptr->id,
                                           people_info_ptr->train_idx,
                                           people_info_ptr->seat_idx,
                                           people_info_ptr->start_station,
                                           people_info_ptr->end_station);
        fprintf(fp, "%s\n", line);
    }
    fclose(fp);
    return 0;
}
