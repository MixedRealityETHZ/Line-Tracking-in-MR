# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.27

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
CMAKE_COMMAND = /usr/local/bin/cmake

# The command to remove a file.
RM = /usr/local/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/aidyn/Desktop/mixed-reality-line-tracking

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/aidyn/Desktop/mixed-reality-line-tracking/build

# Include any dependencies generated for this target.
include CMakeFiles/linefeature_tracker.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/linefeature_tracker.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/linefeature_tracker.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/linefeature_tracker.dir/flags.make

CMakeFiles/linefeature_tracker.dir/src/linefeature_tracker.cpp.o: CMakeFiles/linefeature_tracker.dir/flags.make
CMakeFiles/linefeature_tracker.dir/src/linefeature_tracker.cpp.o: /home/aidyn/Desktop/mixed-reality-line-tracking/src/linefeature_tracker.cpp
CMakeFiles/linefeature_tracker.dir/src/linefeature_tracker.cpp.o: CMakeFiles/linefeature_tracker.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/aidyn/Desktop/mixed-reality-line-tracking/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/linefeature_tracker.dir/src/linefeature_tracker.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/linefeature_tracker.dir/src/linefeature_tracker.cpp.o -MF CMakeFiles/linefeature_tracker.dir/src/linefeature_tracker.cpp.o.d -o CMakeFiles/linefeature_tracker.dir/src/linefeature_tracker.cpp.o -c /home/aidyn/Desktop/mixed-reality-line-tracking/src/linefeature_tracker.cpp

CMakeFiles/linefeature_tracker.dir/src/linefeature_tracker.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/linefeature_tracker.dir/src/linefeature_tracker.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/aidyn/Desktop/mixed-reality-line-tracking/src/linefeature_tracker.cpp > CMakeFiles/linefeature_tracker.dir/src/linefeature_tracker.cpp.i

CMakeFiles/linefeature_tracker.dir/src/linefeature_tracker.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/linefeature_tracker.dir/src/linefeature_tracker.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/aidyn/Desktop/mixed-reality-line-tracking/src/linefeature_tracker.cpp -o CMakeFiles/linefeature_tracker.dir/src/linefeature_tracker.cpp.s

# Object files for target linefeature_tracker
linefeature_tracker_OBJECTS = \
"CMakeFiles/linefeature_tracker.dir/src/linefeature_tracker.cpp.o"

# External object files for target linefeature_tracker
linefeature_tracker_EXTERNAL_OBJECTS =

liblinefeature_tracker.a: CMakeFiles/linefeature_tracker.dir/src/linefeature_tracker.cpp.o
liblinefeature_tracker.a: CMakeFiles/linefeature_tracker.dir/build.make
liblinefeature_tracker.a: CMakeFiles/linefeature_tracker.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/home/aidyn/Desktop/mixed-reality-line-tracking/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX static library liblinefeature_tracker.a"
	$(CMAKE_COMMAND) -P CMakeFiles/linefeature_tracker.dir/cmake_clean_target.cmake
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/linefeature_tracker.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/linefeature_tracker.dir/build: liblinefeature_tracker.a
.PHONY : CMakeFiles/linefeature_tracker.dir/build

CMakeFiles/linefeature_tracker.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/linefeature_tracker.dir/cmake_clean.cmake
.PHONY : CMakeFiles/linefeature_tracker.dir/clean

CMakeFiles/linefeature_tracker.dir/depend:
	cd /home/aidyn/Desktop/mixed-reality-line-tracking/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/aidyn/Desktop/mixed-reality-line-tracking /home/aidyn/Desktop/mixed-reality-line-tracking /home/aidyn/Desktop/mixed-reality-line-tracking/build /home/aidyn/Desktop/mixed-reality-line-tracking/build /home/aidyn/Desktop/mixed-reality-line-tracking/build/CMakeFiles/linefeature_tracker.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : CMakeFiles/linefeature_tracker.dir/depend

