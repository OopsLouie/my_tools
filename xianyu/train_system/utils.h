#ifndef __UTILS_H__
#define __UTILS_H__


#include "types.h"

int timestr_to_minutes(char * time_str);
void minutes_to_timestr(int minutes, char * time_str);

int seatstr_to_index(char * seatstr);
void index_to_seatstr(int index, char * seatstr);
void delete_people(char * name, char * id);
void delete_seat_from_train(char * train_idx, char * seat_str);

void change_time();

void paintmenu();

#endif
