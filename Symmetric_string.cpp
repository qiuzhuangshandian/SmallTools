#include<stdio.h>
#include<string>
int getLengthMaxStr(char* str) {
	int L = strlen(str);
	int i, Maxnum = 1;
	int left, right;
	for (i = 0; i < L; i++) {
		//偶
		left = i;
		right = i + 1;
		while (1) {
			if (left < 0 || right>L - 1 || str[left] != str[right])
				break;
			left--;
			right++;
		}
		if (Maxnum < right - left - 1) {
			Maxnum = right - left - 1;
		}
		//奇
		left = i - 1;
		right = i + 1;
		while (1) {
			if (left < 0 || right>L - 1 || str[left] != str[right])
				break;
			left--;
			right++;
		}
		if (Maxnum < right - left - 1) {
			Maxnum = right - left - 1;
		}
	}
	return Maxnum;

}

int main() {
	char str[30] = "google!";
	printf("%d\n", getLengthMaxStr(str));
	puts(str);
	getchar();
	return 0;

}
