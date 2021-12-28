cmake_minimum_required(VERSION 2.6)
project(simuRun)
file(GLOB src_file *.cpp *.h)
add_executable(${PROJECT_NAME} ${src_file})