#include<iostream>
unsigned int char_in_string(const char * str,char ch);
int main(){
	std::cout << char_in_string("jlkjkkkkjk",'j') << std::endl;
}

unsigned int char_in_string(const char * str,char ch){
	unsigned int cnt =0;
	while(* str){
		if(*str == ch)
			cnt++;
		str++;
	}
	return cnt;
}
