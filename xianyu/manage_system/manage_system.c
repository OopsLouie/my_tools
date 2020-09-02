#include <stdio.h>
#include <string.h>

int num[5];
int total_num = 0;

#define number_of_touziren 100

typedef struct data    /*建立结构体*/
{
    char DanWei[1024];
    int ZiZhi;
    int JiaGe;
    long DianHua;
} data_t;

void my_print();
void delete();
void search();
void input();
void output();

data_t my_data[number_of_touziren];   /*数据*/

int main()
{
    char c;
    do{
        my_print();
        c = getchar();
        switch(c)
        {
            case '1':
                input();
                break;
            case '2':
                output();
                break;
            case '3':
                search();
                break;
            case '4':
                delete();
                break;
            case '5':
                return 0;
            default:
                printf("请输入正确的操作代码\n");
                break;
        }
        while ((c = getchar()) != '\n' && c != EOF) ;
    }while (1);
    return 0;
}

void my_print() {
    printf("请输入你要执行的操作代码：\n");
    printf("1. 输入信息(投标人上限100)\n");
    printf("2. 打印投标人信息\n");
    printf("3. 根据价格查询投标人\n");
    printf("4. 根据资质删除投标人\n");
    printf("5. 退出\n");
    return;
}

void input() {
    printf("请按序输入信息，以回车分割（单位、资质、价格、电话）：\n");
    scanf("%s%d%d%ld",my_data[total_num].DanWei,&my_data[total_num].ZiZhi,&my_data[total_num].JiaGe,&my_data[total_num].DianHua);
    total_num ++;
    return;
}

void search() {
    int i;
    int price;
    printf("请输入想要查询的价格：\n");
    scanf("%d",&price);
    for(i=0;i<total_num;i++)
    {
        if(my_data[i].JiaGe==price)
        {
            printf("***\n");
            printf("投资人：%s\n资质：%d\n价格：%d\n电话%ld\n",my_data[i].DanWei,my_data[i].ZiZhi,my_data[i].JiaGe,my_data[i].DianHua);
        }
    }
    return;
}

void output() {
    int i;
    for(i=0;i<total_num;i++)
    {
        printf("***\n");
        printf("投资人：%s\n资质：%d\n价格：%d\n电话%ld\n",my_data[i].DanWei,my_data[i].ZiZhi,my_data[i].JiaGe,my_data[i].DianHua);
    }
}

void delete()
{
    int level;
    printf("请输入不想要的资质：\n");
    scanf("%d",&level);
    int i=0;
    for(i=0; i<total_num; i++)
    {
        if(my_data[i].ZiZhi==level)
            break;   /* 找到要删除的记录就退出 */
    }
    for(;i < number_of_touziren - 1;i++)
    {
        memcpy(&my_data[i],&my_data[i+1],sizeof(data_t));/* 将后面的记录向前移 */
    }
    total_num--;
    return;
}
