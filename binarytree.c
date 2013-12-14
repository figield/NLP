#include <stdlib.h>
#include <stdio.h>
#define DLWYRAZU 20

struct pwezel{
             int pole;
	     struct pwezel *left;
	     struct pwezel *right;
	     };

struct pwezelstr{
             char pole[DLWYRAZU];
	     struct pwezelstr *left;
	     struct pwezelstr *right;
	     };

/*******************************************************************************************************************/

int ktorystrmniejszy(char *pierwszeslowo ,char *drugieslowo) /*zwraca nr slowa w nawiasie , ktore jest mniejsze*/
 {
   int i=0;
   while ((pierwszeslowo[i]==drugieslowo[i])&&(pierwszeslowo[i]!='\0')&&(drugieslowo[i]!='\0'))
      i++;

   if (pierwszeslowo[i]<drugieslowo[i])               
     return 1;
   else if (pierwszeslowo[i]>drugieslowo[i])
     return 2;
   else return 0;              
 }

void str_copy(char *cel ,char *zrodlo )
 {
   int i=0;
   while (cel[i]=zrodlo[i])
     i++;
 }


int porownajstringi(char *str1 ,char *str2)
 {
   int i=0;
   int p=1;
   int k=1;

   while (k==1)
     {
        if (str1[i]==str2[i])
	 {
           if (str1[i]=='\0')
	    k=0;

           i++;
	 }
        else {p=0;
	      k=0;}
     }

  return p;
 }

/****************************************************************************************************************/


int dodajdodrzewa(struct pwezel **wezel ,int temp)
 {

   if ((*wezel)==NULL)
    {

     (*wezel)=(struct pwezel*)malloc(1* sizeof (struct pwezel));
     (**wezel).pole=temp;
    }

  else

    {
     if ((**wezel).pole > temp)
       {
         if ((**wezel).left==NULL)
            { 
             (**wezel).left=(struct pwezel*)malloc(1 *sizeof (struct pwezel));
             (**wezel).left->pole=temp;
            }	
          else
    	    { 
	     dodajdodrzewa(&(**wezel).left,temp);
  	    } 
 
       }
     else if((**wezel).pole < temp)
       {
         if ((**wezel).right==NULL)
            { 
             (**wezel).right=(struct pwezel*)malloc(1 *sizeof (struct pwezel));
             (**wezel).right->pole=temp;
            }	
          else
  	    { 
	     dodajdodrzewa(&(**wezel).right,temp);
	    } 
       }
             
    }
 }

/*------------------------------------------------------------------------------------------------------------*/	     
 
int dodajdodrzewastr(struct pwezelstr **wezel ,char wyraz[])
 {

   if ((*wezel)==NULL)
    {
     (*wezel)=(struct pwezelstr*)malloc(1* sizeof (struct pwezelstr));
     str_copy((**wezel).pole,wyraz);
    }

  else

    {
     if (ktorystrmniejszy((**wezel).pole,wyraz)==2)  
       {
         if ((**wezel).left==NULL)
            { 
             (**wezel).left=(struct pwezelstr*)malloc(1 *sizeof (struct pwezelstr));
             str_copy((**wezel).left->pole,wyraz);
            }	
          else
    	    { 
	     dodajdodrzewastr(&(**wezel).left,wyraz);
  	    } 
 
       }
     else if(ktorystrmniejszy((**wezel).pole,wyraz)==1)
       {
         if ((**wezel).right==NULL)
            { 
             (**wezel).right=(struct pwezelstr*)malloc(1 *sizeof (struct pwezelstr));
              str_copy((**wezel).right->pole,wyraz);
            }	
          else
  	    { 
	     dodajdodrzewastr(&(**wezel).right,wyraz);
	    } 
       }
             
    }
 }
 
 
/********************************************************************************************************************/ 
 
 
int szukajwdrzewie(struct pwezel *wezel,int temp)  
 {
  int d=0;
  
  if (wezel==NULL)
      printf(" Brak zmiennych w drzewie\n"); 
   else if ((*wezel).pole > temp)
       {
       if ((*wezel).left==NULL)
          d=0;	
        else
	  d=szukajwdrzewie((*wezel).left,temp);
       }
       
   else if((*wezel).pole < temp)
       {
       if ((*wezel).right==NULL)
	  d=0;
        else
	  d=szukajwdrzewie((*wezel).right,temp);
       }       
   else d=1; 
    
       
  return d;
 } 

/*------------------------------------------------------------------------------------------------------------*/	     
 
 int szukajwdrzewiestr(struct pwezelstr *wezel,char wyraz[])     
 {
  int d=0;
  
  if (wezel==NULL)
      printf(" Brak zmiennych w drzewie\n"); 
   else if (ktorystrmniejszy((*wezel).pole,wyraz)==2)
       {
       if ((*wezel).left==NULL)
          d=0;
        else
	  d=szukajwdrzewiestr((*wezel).left,wyraz);
       }
       
   else if(ktorystrmniejszy((*wezel).pole,wyraz)==1)
       {
       if ((*wezel).right==NULL)
	  d=0;
        else
	 d=szukajwdrzewiestr((*wezel).right,wyraz);
       }
       
   else d=1; 
    
       
  return d;
 } 


/********************************************************************************************************************/ 


void usun(struct pwezel **r,struct pwezel **q)          /* funkcja pomocnicza dofunkcji usunwezel*/
 { 
  if((**r).right!=NULL)
    usun(&(**r).right,q);
  else 
    {
     (**q).pole=(**r).pole;
     (*q)=(*r);
     (*r)=(**r).left;
    }     
 }    

/*------------------------------------------------------------------------------------------------------------*/	     

void usunstr(struct pwezelstr **r,struct pwezelstr **q)          /* funkcja pomocnicza dofunkcji usunwezelstr*/
 { 
  if((**r).right!=NULL)
    usunstr(&(**r).right,q);
  else 
    {
      str_copy((**q).pole,(**r).pole);
     (*q)=(*r);
     (*r)=(**r).left;
    }     
 }    

/********************************************************************************************************************/ 


void usunwezel(struct pwezel **wezel, int temp)  
  {
   struct pwezel *q; 
  
   if ((*wezel)==NULL)
      printf(" Brak zmiennych w drzewie\n"); 
   else if ((**wezel).pole > temp)
  	    usunwezel(&(**wezel).left,temp);                    
   else if((**wezel).pole < temp)
	    usunwezel(&(**wezel).right,temp); 
   else
       {
        q=*wezel;
	if ((*q).right==NULL) 
	  (*wezel)=(*q).left; 
	else if ((*q).left==NULL)
	  (*wezel)=(*q).right;
	else
	  usun(&(**wezel).left,&q);   
 
	free(q);	          
       }
       
  }                    

/*------------------------------------------------------------------------------------------------------------*/	     

void usunwezelstr(struct pwezelstr **wezel, char * wyraz)  
  {
   struct pwezelstr *q; 

   if ((*wezel)==NULL)  
      printf(" Brak wyrazow  w drzewie\n");
   else if ((ktorystrmniejszy((**wezel).pole,wyraz)==2))
  	  usunwezelstr(&(**wezel).left,wyraz);                    
   else if ((ktorystrmniejszy((**wezel).pole,wyraz)==1)) 
          usunwezelstr(&(**wezel).right,wyraz); 
   else
       {
        q=*wezel;
	if ((*q).right==NULL) 
	  (*wezel)=(*q).left; 
	else if ((*q).left==NULL)
	  (*wezel)=(*q).right;
	else
	  usunstr(&(**wezel).left,&q);   
 
	free(q);	          
       }
       
  }                    
        
/********************************************************************************************************************/ 
  
void usundrzewo(struct pwezel **wezel)
 { 
  if ((*wezel)!=NULL)
    { 
     usundrzewo(&(**wezel).left);
     usundrzewo(&(**wezel).right);
     free(*wezel);
     *wezel=NULL;
    }
 }

/*------------------------------------------------------------------------------------------------------------*/	     

void usundrzewostr(struct pwezelstr **wezel)
 { 
  if ((*wezel)!=NULL)
    { 
     usundrzewostr(&(**wezel).left);
     usundrzewostr(&(**wezel).right);
     free(*wezel);
     *wezel=NULL; 
    }
 }



/********************************************************************************************************************/ 

void drukujdrzewo(struct pwezel *wezel,int k)
 {
   int i; 
   
  if (wezel!=NULL)
   { 
    drukujdrzewo((*wezel).right,k+1);
    for (i=0;i<=k;i++)
        printf("   ");
    printf("%d\n",(*wezel).pole);
    drukujdrzewo((*wezel).left,k+1);        
   }    
    
 }
      
/*------------------------------------------------------------------------------------------------------------*/	     
  
void drukujdrzewostr(struct pwezelstr *wezel,int k)
 {
   int i; 
   
  if (wezel!=NULL)
   { 
    drukujdrzewostr((*wezel).right,k+1);
    for (i=0;i<=k;i++)
        printf("    ");
    printf("%s\n",(*wezel).pole);
    drukujdrzewostr((*wezel).left,k+1);        
   }    
    
 }     
  
/********************************************************************************************************************/ 
/********************************************************************************************************************/ 
  
 
 
 main()	     
{

 struct pwezel * root;
 struct pwezelstr * rootstr;
 char odp[15]={"t"};
 char odp2='t';
 int temp;
 char wyraz[DLWYRAZU];
 int n=1;
 int m=5;
 
 
 
 root=NULL;
 rootstr=NULL;
 printf("\n\t W celu poznania komend wpisz: help\n\n ");
 
 while (!(porownajstringi(odp,"exit")||porownajstringi(odp,"quit")))

 { 
  printf("\n\t> "); 
  scanf("%s",odp);
  
  
  if (porownajstringi(odp,"treeint"))                     /* stworz  drzewo lub dodaj do niego elementy*/
        {
         printf("\t\tDodaj elementy do drzewa, jesli drzewo nie bylo stworzone wczesnej to pierwsza wartosc jest dla roota \n\t\t (by skonczyc wpisz k ) :\n\t\t ");
	 n=1;
         while (n)
            { 
              n=scanf("%d",&temp);	                /* jezeli wpisany znak bedzie innego typu niz int to zwroci 0 */
              if (n!=0)                          
                   dodajdodrzewa(&root,temp);
	      if (n==0) 
	         odp2=getchar(); 
             }
        }
  else if (porownajstringi(odp,"treestr"))
  	{
         printf("\t\tDodaj wyrazy do drzewa, jesli drzewo nie bylo stworzone wczesnej to pierwszy wyraz jest dla roota \n\t\t (by skonczyc wpisz 'end' ) :\n\t\t ");
	 n=1;
         while (n)
           {
	    
              scanf("%s",wyraz);
	      if (porownajstringi(wyraz,"end")) n=0;	                              	        
              if (n!=0)                          
                dodajdodrzewastr(&rootstr,wyraz);
	      /*if (n==0) 
	        odp2=getchar(); */
             }
        }   
  else if (porownajstringi(odp,"printint"))
        {
          drukujdrzewo(root, m); 
        }  
  else if (porownajstringi(odp,"printstr"))
        {
          drukujdrzewostr(rootstr, m);  
        }  
  else if (porownajstringi(odp,"delint"))	               /* usuwanie elementu */
	{
         odp2='t';	
         while (odp2!='n')
            {
              printf("\n\t\tWpisz element, ktory chcesz usunac :  ");
              scanf("%d",&temp);
   
              if(szukajwdrzewie(root,temp)!=NULL)	                     
               {    
                usunwezel(&root,temp);
	        printf("\n\t\tTej wartosci nie ma juz na drzewie!(drzewo zostalo przebudowane)\n");
               }	
              else
                printf("\n\t\tTej wartosci NIE MA  na drzewie\n");
     
              printf("\t\tCzy chcesz usuwac  dalej  (t/n)  : ");
              odp2=getchar();
              scanf("%c",&odp2);
            }
	}
  else if (porownajstringi(odp,"delstr"))
        {
         odp2='t';	
         while (odp2!='n')
            {
              printf("\n\t\tWpisz element, ktory chcesz usunac :  ");
              scanf("%s",wyraz);
              if(szukajwdrzewiestr(rootstr,wyraz))	                     
               {   
                usunwezelstr(&rootstr,wyraz);
	           /*printf("\n\t\tTego wyrazu nie ma juz na drzewie!(drzewo zostalo przebudowane)\n");*/
               }	
              else
                printf("\n\t\tTego wyrazu - NIE MA -  na drzewie\n");
              
              printf("\t\tCzy chcesz usuwac  dalej  (t/n)  : ");
              odp2=getchar();
              scanf("%c",&odp2);
            }
  	}
  else if (porownajstringi(odp,"deltreeint"))	
	{
	 usundrzewo(&root);
	}
  else if (porownajstringi(odp,"deltreestr"))	
	{
	 usundrzewostr(&rootstr);
	}	
  else if (porownajstringi(odp,"findint"))	
	{
	 odp2='t';
         while (odp2!='n')
              {
              printf("\t\tPodaj szukana wartosc : ");
              scanf("%d",&temp);
   
              if (szukajwdrzewie(root,temp))	
              printf("\n\t\tTa wartosc - JEST - na drzewie");
              else
              printf("\n\t\tTej wartosci - NIE MA - na drzewie");
     
              printf("\n\t\tCzy chcesz szukac dalej  (t/n)  : ");
              odp2=getchar();
              scanf("%c",&odp2);
              } 
	}	
  else if (porownajstringi(odp,"findstr")){
	 odp2='t';
         while (odp2!='n'){
	          odp2=getchar();
              printf("\t\tPodaj szukany wyraz : ");
              scanf("%s",wyraz);
   
              if (szukajwdrzewiestr(rootstr,wyraz))                          	
              printf("\n\t\tTen wyraz - JEST - na drzewie");
              else
              printf("\n\t\tTego wyrazu - NIE MA - na drzewie");
     
              printf("\n\t\tCzy chcesz szukac dalej  (t/n)  : ");
              odp2=getchar();
              scanf("%c",&odp2);
              }
  	}
  else if (porownajstringi(odp,"help")){
         printf("\n\n\t\t treeint     - stworzenie drzewa liczb lub jesli istnieje dodanie do niego elementu\n\n");
	 printf("\t\t treestr     = stworzenie drzewa wyrazow lub jesli istnieje dodanie do niego slowa\n\n");      
         printf("\t\t findint     - sprawdzenie czy istnieje dany element na drzewie liczb\n\n");     
         printf("\t\t findstr     = sprawdzenie czy istnieje dany wyraz  na drzewie wyrazow\n\n");
	 printf("\t\t delint      - usuniecie danej liczby \n\n");
         printf("\t\t delstr      = usuniecie danego wyrazu \n\n");
	 printf("\t\t deltreeint  - usuniecie drzewa liczb\n\n");
         printf("\t\t deltreestr  = usuniecie drzewa wyrazow\n\n");
	 printf("\t\t printint    - wydrukowanie szkicu drzewa liczb w orientacji poziomej\n\n");
	 printf("\t\t printstr    = wydrukowanie szkicu drzewa wyrazow  w orientacji poziomej\n\n");
         printf("\t\t exit        - wyjscie z programu\n\n");
	 printf("\t\t quit        - wyjscie z programu\n\n");
	 printf("\t\t help        - komendy programu\n\n");
        }
 } 
   
  usundrzewo(&root);
  usundrzewostr(&rootstr);
 
}   



          
