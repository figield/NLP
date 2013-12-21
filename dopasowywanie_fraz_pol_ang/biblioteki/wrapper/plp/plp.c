#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "clp.h"
#define BUFLEN 10

void plp_init()
{
	clp_init();
}

char * plp_ver()
{
	char * result;
	result = (char *)malloc(1024*sizeof(char));
	result = clp_ver();
	return result;
}
/*
int * plp_rec(const char * inp)
{
	int * out;
	int * tmp;
	int num;
	int i;
	tmp = (int*)malloc(80*sizeof(int)); // 80 ??
	clp_rec(inp,tmp,&num);
	out = (int*)malloc((num+1)*sizeof(int));
	out[0]=num;
	for(i = 0; i < num ; i++)
	{
		out[i+1]=tmp[i];
	}
	free(tmp);
	return out;
}
*/
/*
unsigned char * plp_rec(const unsigned char * inp)
{
	int * out;
	int * tmp;
	int num;
	int i;
	tmp = (int*)malloc(20*sizeof(int));
	clp_rec(inp,tmp,&num);
	
	int buflen = 20;
	unsigned char *result = (unsigned char*)malloc(buflen*sizeof(unsigned char));
	sprintf(result, "%d", num);
	
	printf("%d", num);
	//for(int j=0;j<num;j++){
	    //printf("%d", tmp[j]);
	//}
	printf("%d\n", tmp[0]);
	printf("%d\n", tmp[1]);
	
	out = (int*)malloc((num+1)*sizeof(int));
	out[0]=num;
	for(i = 0; i < num ; i++)
	{
		out[i+1]=tmp[i];
		buflen+=20;
		result = realloc(result, buflen*sizeof(unsigned char));
	}
	free(tmp);
	free(out);
	return result;
}
*/

unsigned char * plp_rec(const unsigned char * inp)
{
	int * tmp;
	int num;
	int i;
	char id[BUFLEN]; 
	
	tmp = (int*)malloc(10*sizeof(int));
	clp_rec(inp,tmp,&num);
	
	unsigned char *result = (unsigned char*)malloc(BUFLEN*(num+1)*sizeof(unsigned char));
	sprintf(result, "%d", num);
	 
	for(i=0; i < num; i++){
	    sprintf(id, ":%d", tmp[i]);
	    strcat(result,id);
	}
	//printf("result:%s\n", result);

	free(tmp);
	return result;
}

unsigned char * plp_bform(int id)
{
	unsigned char * out;
	out = (unsigned char*)malloc(80*sizeof(unsigned char)); // ??
	clp_bform(id,out);
	return out;
}

unsigned char * plp_forms(int id)
{
	unsigned char * out;
	out = (unsigned char*)malloc(2048*sizeof(unsigned char));
	clp_forms(id, out);
	return out;
}
// NIE PRZETESTOWANA!
unsigned char * plp_vec(int id, const char * inp)
{
	int * tmp;
	int num;
	int i;
	char id_buff[BUFLEN];
	
	tmp = (int*)malloc(80*sizeof(int));
	clp_vec(id,inp,tmp,&num);
	 
	unsigned char *result = (unsigned char*)malloc(BUFLEN*(num+1)*sizeof(unsigned char));
	sprintf(result, "%d", num);
	//printf("result1:%s\n", result);
	 
	for(i=0; i < num; i++){
	    sprintf(id_buff, ":%d", tmp[i]);
	    //printf("id_buff:%s\n", id_buff);
	    strcat(result,id_buff);
	}
	//printf("result2:%s\n", result);

	free(tmp);
	return result;
}

char * plp_label(int id)
{
	char * out;
	out = (char*)malloc(20*sizeof(char));
	clp_label(id,out);
	return out;
}

