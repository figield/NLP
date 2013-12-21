#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "clp.h"
#define BUFLEN 10
#define CLP_BUF_SIZE 16
#define CLP_ID_DIGITS 8

void plp_init() {
    clp_init();
}

char * plp_ver() {
    return clp_ver();
}

unsigned char* plp_rec(const unsigned char * inp) {
    int i;
    int ids[CLP_BUF_SIZE];
    int num_ids;
    char *result = malloc(CLP_BUF_SIZE * CLP_ID_DIGITS);
    clp_rec(inp, ids, &num_ids);

    char *end = result;
    end += sprintf(result, "%d", num_ids);
    for (i=0; i<num_ids; i++) {
        end += sprintf(end, ":%d", ids[i]);
    }
    return result;
}

unsigned char* plp_bform(int id) {
    unsigned char * out;
    out = malloc(1024);
    clp_bform(id, out);
    return out;
}

unsigned char * plp_forms(int id) {
    unsigned char* out = malloc(4096);
    clp_forms(id, out);
    return out;
}

unsigned char* plp_vec(int id, const char* inp) {
    int *tmp;
    int num;
    int i;
    char id_buff[BUFLEN];

    tmp = malloc(256);
    clp_vec(id, inp, tmp, &num);

    unsigned char *result = malloc(BUFLEN*(num+1));
    sprintf(result, "%d", num);

    for(i=0; i < num; i++){
        sprintf(id_buff, ":%d", tmp[i]);
        strcat(result, id_buff);
    }

    free(tmp);
    return result;
}

char* plp_label(int id) {
    char* out = malloc(20);
    clp_label(id, out);
    return out;
}

