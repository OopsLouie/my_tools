#ifndef __TYPES_H__
#define __TYPES_H__

#include <stdint.h>
#include <time.h>

#define MAX_TRAIN_IDX_LEN               10
#define MAX_TRAIN_NUM                   20

#define MAX_STATION_NUM                 10
#define MAX_STATION_NAME_LEN            20

#define MAX_PEOPLE_PER_TRAIN            100

#define MAX_NAME_LEN                    20
#define MAX_ID_LEN                      20
#define MAX_SEAT_IDX_LEN                10
#define MAX_TICKETS_PER_TRADE           5

#define MAX_PEOPLE_NUM      MAX_PEOPLE_PER_TRAIN * MAX_TRAIN_NUM

typedef struct {
    char train_idx[MAX_TRAIN_IDX_LEN];
    uint8_t station_num;
    char start_station[MAX_STATION_NUM][MAX_STATION_NAME_LEN];
    char end_station[MAX_STATION_NUM][MAX_STATION_NAME_LEN];
    uint32_t start_time[MAX_STATION_NUM];
    uint32_t end_time[MAX_STATION_NUM];
    uint8_t total_seats_num;
    uint8_t booked_seats_num;
    char people_id[MAX_PEOPLE_PER_TRAIN][MAX_ID_LEN];
} train_info_t;

typedef struct {
    train_info_t train_infos[MAX_TRAIN_NUM];
    uint8_t train_num;
} train_system_t;

typedef struct {
    char name[MAX_NAME_LEN];
    char id[MAX_ID_LEN];
    struct tm travel_start_time;
    char train_idx[MAX_TRAIN_IDX_LEN];
    char seat_idx[MAX_SEAT_IDX_LEN];
    char start_station[MAX_STATION_NAME_LEN];
    char end_station[MAX_STATION_NAME_LEN];
} people_info_t;

typedef struct {
    people_info_t people_infos[MAX_PEOPLE_NUM];
    uint8_t people_num;
} people_system_t;

extern train_system_t train_system;
extern people_system_t people_system;

#endif
