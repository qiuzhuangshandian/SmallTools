cmake_minimum_required(VERSION 2.6)

project(cnn)


include_directories(test_src)

# link_directories("")
add_library(cnn SHARED test_src/Cpluscode.cpp)