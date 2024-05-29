set(ARM_CROSS_BUILD_ARCH aarch64)
set(CMAKE_C_COMPILER "aarch64-none-linux-gnu-gcc")
set(CMAKE_CXX_COMPILER "aarch64-none-linux-gnu-g++")
set(CMAKE_C_FLAGS "-Wno-psabi")
set(CMAKE_CXX_FLAGS "-Wno-psabi")
if("$ENV{FORCE_CHECK_UNUSED_PARAMETER}" STREQUAL "true")
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Werror=unused-parameter")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Werror=unused-parameter")
endif()
set(CMAKE_STRIP "aarch64-none-linux-gnu-strip")
set(CMAKE_SYSTEM_PROCESSOR aarch64)
set(CMAKE_SYSTEM_NAME Linux)