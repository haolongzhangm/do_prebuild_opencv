set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR riscv64)
set(RISCV_CROSS_BUILD_ARCH riscv64)

if(DEFINED ENV{RISCV_TOOLCHAIN_ROOT})
  file(TO_CMAKE_PATH $ENV{RISCV_TOOLCHAIN_ROOT} RISCV_TOOLCHAIN_ROOT)
else()
  message(FATAL_ERROR "RISCV_TOOLCHAIN_ROOT env must be defined")
endif()

set(RISCV_TOOLCHAIN_ROOT
    ${RISCV_TOOLCHAIN_ROOT}
    CACHE STRING "root path to riscv toolchain")

set(CMAKE_C_COMPILER "${RISCV_TOOLCHAIN_ROOT}/bin/riscv64-unknown-linux-gnu-gcc")
set(CMAKE_CXX_COMPILER "${RISCV_TOOLCHAIN_ROOT}/bin/riscv64-unknown-linux-gnu-g++")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -march=rv64gcv0p7_zfh -mabi=lp64d")
set(CMAKE_CXX_FLAGS
    "${CMAKE_CXX_FLAGS} -march=rv64gcv0p7_zfh -mabi=lp64d -Wno-error=attributes")
set(CMAKE_FIND_ROOT_PATH "${RISCV_TOOLCHAIN_ROOT}/riscv64-unknown-linux-gnu")
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)