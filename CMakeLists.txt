cmake_minimum_required(VERSION 3.0)


project(Module_Image)

add_executable(test 
src/mainTest.cpp
src/Image.cpp
)

add_executable(exemple 
src/mainExemple.cpp
src/Image.cpp
)

#target_link_libraries(affichage SDL2)

set(EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/bin)