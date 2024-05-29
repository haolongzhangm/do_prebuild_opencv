set(ARM_CROSS_BUILD_ARCH armv7)
set(CMAKE_C_COMPILER "arm-linux-gnueabi-gcc")
set(CMAKE_CXX_COMPILER "arm-linux-gnueabi-g++")
set(CMAKE_C_FLAGS "-mfloat-abi=softfp -mfpu=neon-vfpv4 -Wno-psabi")
set(CMAKE_CXX_FLAGS "-mfloat-abi=softfp -mfpu=neon-vfpv4 -Wno-psabi")
if("$ENV{FORCE_CHECK_UNUSED_PARAMETER}" STREQUAL "true")
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Werror=unused-parameter")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Werror=unused-parameter")
endif()
set(CMAKE_STRIP "arm-linux-gnueabi-strip")
set(CMAKE_SYSTEM_PROCESSOR armv7)
set(CMAKE_SYSTEM_NAME Linux)