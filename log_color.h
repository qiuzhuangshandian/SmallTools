#ifndef __LOG_H__
#define __LOG_H__
#include <stdio.h>

#define __LOG(...)\
    do{ \
        printf(__VA_ARGS__); \
    } while(0)

#define __format(__fmt__) "%d " __fmt__ "\n"

#define LOG(__fmt__, ...)  \
	do{ \
		__LOG(__format(__fmt__), __LINE__,##__VA_ARGS__); \
	}while(0)

//#define LOG_DEBUG "DEBUG"
//#define LOG_TRACE "TRACE"
//#define LOG_ERROR "ERROR"
//#define LOG_INFO  "INFOR"
//#define LOG_CRIT  "CRTCL"

//#define LOG(level, format, ...) \
//    do { \
//        fprintf(stderr, "[%s|%s@%s,%d] " format "\n", \
//            level, __func__, __FILE__, __LINE__, ##__VA_ARGS__ ); \
//    } while (0)
#define RESET_C0LOR	printf("\033[0m");
#define ERROR_LOG(format, ...)  \
	do{  \
		fprintf(stderr, "\033[31m[%s|%s@%s,%d] " format "\n",  \
			"error", __func__, __FILE__, __LINE__, ##__VA_ARGS__ );  \
			RESET_C0LOR  \
	}while(0)

#define INFO_LOG(format, ...)  \
	do{  \
		fprintf(stderr, "\033[32m[%s|%s,%d] " format "\n",  \
			"infor", __func__, __LINE__, ##__VA_ARGS__  );  \
			RESET_C0LOR  \
	}while(0)

#define DEBUG_LOG(format, ...)  \
	do{  \
		fprintf(stderr, "\033[35m[%s|%s,%d] " format "\n",  \
			"debug", __func__, __LINE__, ##__VA_ARGS__ );  \
			RESET_C0LOR  \
	}while(0)

#define WARNING_LOG(format, ...)  \
	do{  \
		fprintf(stderr, "\033[33m[%s|%s,%d] " format "\n",  \
			"warn", __func__, __LINE__, ##__VA_ARGS__ );  \
			RESET_C0LOR  \
	}while(0)


#define JSON_DUMP(jsonObject)jsonObject.dump(4).c_str()
#define LINE_FEEDS printf("\n");
#define JsonPrint(jsonObject) printf(JSON_DUMP(jsonObject)); LINE_FEEDS

#endif // !__LOG_H__
