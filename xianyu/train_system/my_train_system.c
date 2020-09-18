#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

#include "utils.h"
#include "types.h"
#include "file_io.h"


train_system_t train_system;
people_system_t people_system;

int main() {
    read_trains_from_file();
    read_peoples_from_file();
    paintmenu();
//    write_trains_to_file();
    write_peoples_to_file();


#if 0
    // test index <---> seatstr
    char tmp[100];
    int i;
    for (i = 0;i<100;i++){
        index_to_seatstr(i,tmp);printf("%s ----", tmp);printf("%d\n", seatstr_to_index(tmp));
    }
    return 0;
#endif
}
