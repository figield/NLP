#include <cstdio>
#include <cstring>
const int LEN = 50;
char line[LEN];

int main(){
  long int T = 1;   
  FILE * pFile = fopen("flex_dict_pol.txt","w+");
  char descr[12];
  char dn[4];
  while(fgets(line, LEN, stdin)){    
    if (sscanf(line, "%*d: %s", &descr)){
      switch (descr[0]){
      case 'A': strcpy(dn,"nou"); break; // noun
      case 'B': strcpy(dn,"ver"); break; // verb
      case 'C': strcpy(dn,"adj"); break; // adjective
      case 'D': strcpy(dn,"num"); break; // numeral
      case 'E': strcpy(dn,"pro"); break; // pronoun
      case 'F': strcpy(dn,"adv"); break; // adverb
      case 'G': strcpy(dn,"ind"); break; // indeclinable
      default: 
        printf("unrecongnised: %s\n",descr);
      }    
      fprintf (pFile, "%d: %s\n",T++, dn);    
    } else 
      fprintf (pFile, "%s",line);
  }
  fclose (pFile);
  return 0;
}  

// How to run:
// > ./update_indexes < flex_dict.txt
