#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define TRUE  (1)
#define FALSE (0)
#define NULLCHAR (char *) 0
#define NGRAM 3                   // długość n-gramu
#define WORD_LENGTH 100           // długość słowa

/******************************************************************************
Odległość Levenshteina (LD) jest miarą podobieństawaa dwóch napisów.
Dla danych dwóch napisów s, t odległość tę obliczamy jako liczbę operacji,
które należy wykonać aby przekształcić napis s w napis t.
Jako operacje przyjmuje się kasowanie znaku, wstawianie znaku, nadpisanie znaku.
Na przykład:
            
  -jeżeli napisy są identyczne, wtedy LD(s,t) = 0 ponieważ nie trzeba 
   wykonywać żadnych operacji,  
  -dla napisów telefon i telegraf LD(s,t) = 4, ponieważ 3 litery trzeba 
   nadpisać i jedną wstawić.
                      
*/
int clp_dist( const unsigned char *s1, const unsigned char *s2 ) 
{ 
  int arr[WORD_LENGTH][WORD_LENGTH]; 
  int i,j,l,m,n,add; 

  for (i=0;i<=strlen(s1);i++) arr[0][i]=i; 
  for (j=0;j<=strlen(s2);j++) arr[j][0]=j; 

  for (j=1;j<=strlen(s2);j++) { 
    for (i=1;i<=strlen(s1);i++) { 
      if (s1[i-1] == s2[j-1]) 
        { add=0; } else { add=1; } 
      m = 1+arr[j-1][i]; 
      l = 1+arr[j][i-1]; 
      n = add+arr[j-1][i-1]; 
      arr[j][i] = (m < l ? (m < n ? m : n): (l < n ? l : n)); 
    } 
  } 

  for (j=0;j<=strlen(s2);j++) { 
    for (i=0;i<=strlen(s1);i++) printf("%3d",arr[j][i]);
    printf("\n");
  }

  return arr[strlen(s2)][strlen(s1)]; 
} 

/*****************************************************************************/
/**
struct ngram {
char grams[WORD_SIZE][WORD_SIZE*WORD_SIZE];
int count;
};

char wordSpace[WORD_SIZE*DICT_SIZE];
char * wordPtr;
char * dict[DICT_SIZE];
int dictSize = 0;

static void ngramize(char * word, struct ngram * target) {
int len, i;
len = strlen(word);
target->count = len - n;
for (i=0; i<target->count; i++) {
// target->grams[i] = gram_ptr;
strncpy(target->grams[i], word + i, n);
// gram_ptr += n;
}
}

static float compare_ngrams(struct ngram * a, struct ngram * b) {
int i,j;
int counter = 0;
for(i=0; i<a->count; i++) 
for(j=0; j<b->count; j++) 
if (strncmp(a->grams[i], b->grams[j], n) == 0) 
counter++;
return (1.0 - ((float)counter)/(a->count + b->count - counter));
}
*/
/*****************************************************************************

 Odlegość n-gramowa. Dla objaśnienia metody przyjmijmy odległość 3-gramową.
   - Dane wyrazy dzielimy na części 3 literowe np.:
            zuzia = zuz, uzi, zia
            pulpecik = pul, ulp, lpe, pec, eci, cik
   - Porównując 2 wyrazy tworzymy zbiory A i B
            A - zbiór części pierwszego wyrazu,
            B - zbiór części drugiego wyrazu.
   - Wykonujemy na tych zbiorach operacje A+B i A*B, przy czym intersuje nas
     liczebność (moc - ozn. L) zbioru A+B oraz zb. A*B
   - Następnie stosujemy wzór:
            1- L(A*B)/L(A+B), czym blizej 0 tym lepiej - tzn wyrazy są tym
            bardziej do siebie zbliżone im wynik z danej operacji bliższy
            będzie zeru. 
*/


struct SET {
  char gram[WORD_LENGTH][NGRAM+1];
  int moc;        
};

void strcopy(char *from_str1, char *to_str2, int begin,int end){
 int i,j=0;
   for(i=begin;i<end;i++){
     to_str2[j++]=from_str1[i];
   } 
   to_str2[j]='\0'; 
}

void add_to_set(char *gram, struct SET * zbior){
   int i=0,add=1;  
   while(i<zbior->moc && add) if(strcmp(gram,zbior->gram[i++])==0) add=0;
   if(add) strcpy(zbior->gram[(zbior->moc)++],gram);
}

void split_word(unsigned char * word, struct SET * zbior){
     
 int i=0, pocz=0,len=strlen(word);    
 char gram[NGRAM+1];
 zbior->moc = 0;

 while(pocz < (len-NGRAM+1)){         
      strcopy(word,gram,pocz,pocz+NGRAM); 
      add_to_set(gram,zbior);
      pocz++;
 } 
 
 printf("word:%s\n",word);
 for (i=0;i<zbior->moc;i++){
  printf("%s,",zbior->gram[i]);
 }
 printf("\nmoc:%d\n",zbior->moc);

}

int moc_sumyAB(struct SET * A, struct SET * B){    
  int i,j,moc = A->moc + B->moc;
  
  for(i=0;i<A->moc;i++){
      for(j=0;j<B->moc;j++) 
        if(strcmp(A->gram[i],B->gram[j])==0){
          moc--;
          break;
         }                      
       j=0;
  }
return moc;      
}

int moc_iloczynuAB(struct SET * A, struct SET * B){
  int i,j,moc = 0;
  
  for(i=0;i<A->moc;i++){
      for(j=0;j<B->moc;j++) 
        if(strcmp(A->gram[i],B->gram[j])==0){ 
          moc++;
          break;                      
        }
      j=0;
  }
return moc;      
}

/******************************************************************************/
int main (int argc, char *argv[])
{ 
    char quit= '\0';  
    struct SET zbiorA;
    struct SET zbiorB;
    char name1[50]="Weronika";
    char name2[50]="Weronikaa";
    int I,S;
    float odp;

    while (quit != 'q')
    {
        printf("odp: %d\n\n",clp_dist(name1,name2));
        
        split_word(name1, &zbiorA); 
        printf("\n");  
        split_word(name2, &zbiorB);       
        printf("\n");   
        
        I=moc_iloczynuAB(&zbiorA,&zbiorB);
        S=moc_sumyAB(&zbiorA,&zbiorB);
        odp=1-(float)I/S;
        
        printf("moc sumy zbiorow:%d\n",S); 
        printf("moc iloczynu zbiorow:%d\n",I); 
        printf("odp:%f\n",odp); 
        
        
        scanf("%c",quit);
    }

return 0;
}
/*****************************************************************************
 *****************************************************************************/
