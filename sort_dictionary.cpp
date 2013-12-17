#include <cstdio>
#include <cstring>
#include <string>
#include <iostream>
#include <map>
#include <vector>
#include <utility>
using namespace std;

class BaseWord {
  
  friend ostream &operator<<(ostream &, const BaseWord &);
  
public:
  long int id; 
  string descr;
  string easy_descr;
  vector<string> collection;
  
  BaseWord(){};
  BaseWord(const BaseWord &);
  ~BaseWord(){};

  BaseWord &operator=(const BaseWord &baseword);
  int operator==(const BaseWord &baseword) const;
  int operator<(const BaseWord &baseword) const;
};

// Copy constructor to handle pass by value.
BaseWord::BaseWord(const BaseWord &baseword) {                            
  id = baseword.id;
  descr = baseword.descr;
  easy_descr = baseword.easy_descr;
  collection = baseword.collection;
}

ostream &operator<<(ostream &output, const BaseWord &baseword){
  output << baseword.id << ":";
  output << baseword.collection.at(0) << ":";
  output << baseword.descr << ":" << baseword.easy_descr << '\n';
  for (unsigned i=0; i < baseword.collection.size(); i++)
    output << ' ' << i+1 << " - " << baseword.collection.at(i) << '\n';        
  return output;
}

BaseWord& BaseWord::operator=(const BaseWord &baseword){
  this->id = baseword.id;
  this->descr = baseword.descr;
  this->easy_descr = baseword.easy_descr;
  this->collection = baseword.collection;
  return *this;
}

int BaseWord::operator==(const BaseWord &baseword) const {
  // compare the first word (the base) from the vector
  return this->collection.at(0) == baseword.collection.at(0); 
  //return this->collection.at(0).compare(baseword.collection.at(0)); // ok
}

int BaseWord::operator<(const BaseWord &baseword) const {
  return this->collection.at(0) < baseword.collection.at(0);
}

int main(){
  const int LEN = 50;
  char line[LEN];
  int T = 1;   
  char descr[12];
  char word[50];
  string easy_descr;
  multimap<string, BaseWord> MapOfBaseWords;
  /********************* creating structures ****************************/
  BaseWord * baseword = NULL;
  while(fgets(line, LEN, stdin)){  
    //cout << "current line: "<< line;
    if (sscanf(line, "%*d: %s", descr)){
      if (baseword != NULL) {
        //MapOfBaseWords[baseword.collection.at(0)] = *baseword;
        MapOfBaseWords.insert(pair<string,BaseWord>(baseword->collection.at(0), 
                                                    *baseword));
        //cout << *baseword;
        //cout << "Map size:" << MapOfBaseWords.size() << endl;
        baseword->~BaseWord();       
        baseword = NULL;
      }
      baseword = new BaseWord();
      switch (descr[0]){
      case 'A': baseword->easy_descr = "nou"; break; // noun
      case 'B': baseword->easy_descr = "ver"; break; // verb
      case 'C': baseword->easy_descr = "adj"; break; // adjective
      case 'D': baseword->easy_descr = "num"; break; // numeral
      case 'E': baseword->easy_descr = "pro"; break; // pronoun
      case 'F': baseword->easy_descr = "adv"; break; // adverb
      case 'G': baseword->easy_descr = "ind"; break; // indeclinable
      default: 
        cout << "unrecongnised:" << descr << endl; 
        cout << "line:" << line << endl; 
        break;   // break the loop
      }    
      //string descrstr(descr); // ok
      //baseword->descr.append(descr); // ok
      baseword->descr = string(descr);
    } else if(sscanf(line, " %*d - %s", word)){
      //cout << "word: "<< word << endl;
      baseword->collection.push_back(string(word));  
    } else {
      cout << "Not matched line: "<<  line << endl;
      break;
    }
    line[0] = '\0'; // not needed
  }
  // store the last one (TODO: make a function)
  if (baseword != NULL) {
    //MapOfBaseWords[baseword.collection.at(0)] = *baseword; // for map
    MapOfBaseWords.insert(pair<string,BaseWord>(baseword->collection.at(0), 
                                                *baseword));
    //cout << *baseword;
    //cout << "Map size:" << MapOfBaseWords.size() << endl;
    baseword->~BaseWord();       
    baseword = NULL;
  }

  /********************* update structure by indexes ********************/
  long int i = 1;
  for(multimap<string, BaseWord>::iterator ii=MapOfBaseWords.begin(); 
      ii!=MapOfBaseWords.end(); ++ii){
    (*ii).second.id = i++ ;
  }

  /********************* save structures to file  ***********************/
  freopen("flex_pol_dict_sorted.txt","w",stdout);
  for(multimap<string, BaseWord>::iterator ii=MapOfBaseWords.begin(); 
      ii!=MapOfBaseWords.end(); ++ii){
    cout << (*ii).second;
  }
  fclose(stdout);

  /********************* convert structure by reverting it **************/

  /********************* save structures as binary term *****************/



  /*********************************************************************/
  return 0;
} 

// How to run:
// > ./sort_dictionary < flex_dict.txt
