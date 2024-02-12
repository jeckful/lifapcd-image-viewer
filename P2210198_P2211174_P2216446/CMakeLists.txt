cmake_minimum_required(VERSION 3.0)

# Notre projet est étiqueté hello
project(Module_Image)

# Crée des variables avec les fichiers à compiler
set(SRCS
    src/mainTest.cpp
    src/Image.cpp
    )


# On indique que l'on veut un exécutable "hello" compilé à partir des fichiers décrits par les variables SRCS et HEADERS
add_executable(mainTest ${SRCS})

target_include_directories(mainTest PUBLIC src/include)
target_link_directories(mainTest PUBLIC src/lib)
target_link_libraries(mainTest SDL2)

set(EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/bin)