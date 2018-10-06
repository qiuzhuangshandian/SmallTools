#define _CRT_SECURE_NO_DEPRECATE
#include<stdio.h>
#include <iostream>

#define LINE 1
#define COLUMN 0
#define P_DIRECTION 1
#define N_DIRECTION -1
#define N 100
int tensor[N][N];
int main() {
	int n, m;
	while (scanf("%d%d",&n,&m)) {
		
		int flag = LINE;
		int line_direction = P_DIRECTION;
		int column_direction =	P_DIRECTION;
		int i, j;
		for (i = 0; i < n;i++) {
			for (j = 0; j < m;j++) {
				scanf("%d",&tensor[i][j]);
			}
		}
		
		/*
		int l = sizeof(tensor)/sizeof(tensor[0]);
		int c = sizeof(tensor[0]) / sizeof(tensor[0][0]);*/
		int L = n * m;
		int cnt_l = L;
		int l_cnt = n-1, c_cnt = m;
		int i_base = 0, j_base = 0;
		i = 0; j = 0;

		while (L > 0) {	
			if (line_direction == P_DIRECTION && flag == LINE) {	
				i = i_base;
				for (j = j_base; j < j_base + c_cnt; j++) {
					printf("%d ",tensor[i][j]);
					L--;
				}
				i_base++;
				j_base = j - 1;
				//printf("\n ibase: %d jbase %d \\", i_base, j_base);
				line_direction = N_DIRECTION;
				flag = COLUMN;
				c_cnt--;
			}
			else if (column_direction == P_DIRECTION && flag == COLUMN) {
				j = j_base;
				for (i = i_base; i < i_base + l_cnt;i++) {
					printf("%d ",tensor[i][j]);
					L--;
				}
				i_base = i - 1;
				j_base--;
				//printf("\n ibase: %d jbase %d \\", i_base, j_base);
				column_direction = N_DIRECTION;
				flag = LINE;
				l_cnt--;
			}
			else if (line_direction == N_DIRECTION && flag == LINE) {
				i = i_base;
				for (j = j_base; j > j_base - c_cnt;j--) {
					printf("%d ",tensor[i][j]);
					L--;
				}
			
				i_base--;
				j_base = j + 1;
				//printf("\n ibase: %d jbase %d \\ ", i_base, j_base);
				line_direction = P_DIRECTION;
				flag = COLUMN;
				c_cnt--;
			}
			else {
				j = j_base;
				for (i = i_base; i > i_base - l_cnt; i--) {
					printf("%d ", tensor[i][j]);
					L--;
				}
				i_base = i+1;
				j_base++;
				//printf("\n ibase: %d jbase %d \\", i_base, j_base);
				column_direction = P_DIRECTION;
				flag = LINE;
				l_cnt--;
			}
		}
	}
	printf("\n");
	getchar();
	return 0;

}

