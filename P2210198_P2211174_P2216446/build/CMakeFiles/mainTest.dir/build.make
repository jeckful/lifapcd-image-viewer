# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/raphale/dev/lifapcd/team-kachow/P2210198_P2211174_P2216446

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/raphale/dev/lifapcd/team-kachow/P2210198_P2211174_P2216446/build

# Include any dependencies generated for this target.
include CMakeFiles/mainTest.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/mainTest.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/mainTest.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/mainTest.dir/flags.make

CMakeFiles/mainTest.dir/src/mainTest.cpp.o: CMakeFiles/mainTest.dir/flags.make
CMakeFiles/mainTest.dir/src/mainTest.cpp.o: ../src/mainTest.cpp
CMakeFiles/mainTest.dir/src/mainTest.cpp.o: CMakeFiles/mainTest.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/raphale/dev/lifapcd/team-kachow/P2210198_P2211174_P2216446/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/mainTest.dir/src/mainTest.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/mainTest.dir/src/mainTest.cpp.o -MF CMakeFiles/mainTest.dir/src/mainTest.cpp.o.d -o CMakeFiles/mainTest.dir/src/mainTest.cpp.o -c /home/raphale/dev/lifapcd/team-kachow/P2210198_P2211174_P2216446/src/mainTest.cpp

CMakeFiles/mainTest.dir/src/mainTest.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/mainTest.dir/src/mainTest.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/raphale/dev/lifapcd/team-kachow/P2210198_P2211174_P2216446/src/mainTest.cpp > CMakeFiles/mainTest.dir/src/mainTest.cpp.i

CMakeFiles/mainTest.dir/src/mainTest.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/mainTest.dir/src/mainTest.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/raphale/dev/lifapcd/team-kachow/P2210198_P2211174_P2216446/src/mainTest.cpp -o CMakeFiles/mainTest.dir/src/mainTest.cpp.s

CMakeFiles/mainTest.dir/src/Image.cpp.o: CMakeFiles/mainTest.dir/flags.make
CMakeFiles/mainTest.dir/src/Image.cpp.o: ../src/Image.cpp
CMakeFiles/mainTest.dir/src/Image.cpp.o: CMakeFiles/mainTest.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/raphale/dev/lifapcd/team-kachow/P2210198_P2211174_P2216446/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/mainTest.dir/src/Image.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/mainTest.dir/src/Image.cpp.o -MF CMakeFiles/mainTest.dir/src/Image.cpp.o.d -o CMakeFiles/mainTest.dir/src/Image.cpp.o -c /home/raphale/dev/lifapcd/team-kachow/P2210198_P2211174_P2216446/src/Image.cpp

CMakeFiles/mainTest.dir/src/Image.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/mainTest.dir/src/Image.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/raphale/dev/lifapcd/team-kachow/P2210198_P2211174_P2216446/src/Image.cpp > CMakeFiles/mainTest.dir/src/Image.cpp.i

CMakeFiles/mainTest.dir/src/Image.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/mainTest.dir/src/Image.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/raphale/dev/lifapcd/team-kachow/P2210198_P2211174_P2216446/src/Image.cpp -o CMakeFiles/mainTest.dir/src/Image.cpp.s

# Object files for target mainTest
mainTest_OBJECTS = \
"CMakeFiles/mainTest.dir/src/mainTest.cpp.o" \
"CMakeFiles/mainTest.dir/src/Image.cpp.o"

# External object files for target mainTest
mainTest_EXTERNAL_OBJECTS =

../bin/mainTest: CMakeFiles/mainTest.dir/src/mainTest.cpp.o
../bin/mainTest: CMakeFiles/mainTest.dir/src/Image.cpp.o
../bin/mainTest: CMakeFiles/mainTest.dir/build.make
../bin/mainTest: CMakeFiles/mainTest.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/raphale/dev/lifapcd/team-kachow/P2210198_P2211174_P2216446/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking CXX executable ../bin/mainTest"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/mainTest.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/mainTest.dir/build: ../bin/mainTest
.PHONY : CMakeFiles/mainTest.dir/build

CMakeFiles/mainTest.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/mainTest.dir/cmake_clean.cmake
.PHONY : CMakeFiles/mainTest.dir/clean

CMakeFiles/mainTest.dir/depend:
	cd /home/raphale/dev/lifapcd/team-kachow/P2210198_P2211174_P2216446/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/raphale/dev/lifapcd/team-kachow/P2210198_P2211174_P2216446 /home/raphale/dev/lifapcd/team-kachow/P2210198_P2211174_P2216446 /home/raphale/dev/lifapcd/team-kachow/P2210198_P2211174_P2216446/build /home/raphale/dev/lifapcd/team-kachow/P2210198_P2211174_P2216446/build /home/raphale/dev/lifapcd/team-kachow/P2210198_P2211174_P2216446/build/CMakeFiles/mainTest.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/mainTest.dir/depend

