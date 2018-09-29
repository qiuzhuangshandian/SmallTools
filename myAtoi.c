#include<stdio.h>
#include<stdlib.h>
#include<limits.h>
#include<ctype.h>
int myatoi(char* pstr) {
	char symbol = 1;
	long long num = 0;
	if (pstr == NULL) {
		printf("pstr is null\n");
		return 0;
	}
	while (isspace(*pstr)) {
		pstr++;
	}

	//if () {
	//	symbol = 0;
	//}
	if ((*pstr >= '0'&&*pstr <= '9')||*pstr == '+'|| *pstr == '-') {
		if (*pstr == '-'){
			symbol = -1;
			pstr++;
		}
		if (*pstr == '+') {
			pstr++;
		}
		while (*pstr >= '0'&&*pstr <= '9'&&*pstr!='\0') {
			num = num * 10 + (*pstr - '0');
			if ((num >0x7FFFFFFF &&symbol == 1)|| (num > 0x80000000 && symbol == -1)) {
				return 0;
			}
			pstr++;
		}
	}
	else {
		return 0;
	}
	return symbol ==1? num:-num;
}

int main() {
	int val = 0;
	char str[100] = " -97879sdf";
	char *p = str;
	val = myatoi(p);
	printf("%d\n",val);
	int j, k, l, m;
	int i = (j=4,k=8,l=16,m=2);
	printf("%d\n",i);
	getchar();
}
