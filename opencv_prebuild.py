#!/usr/bin/env python3

import argparse
import logging
import os
import platform
import subprocess
from enum import Flag, auto
from pathlib import Path


class DependsHostType(Flag):
    # for example, NDK_ROOT
    ENVIRONMENT = auto()
    # for example, gcc
    COMMAND = auto()


class FrameworkFailCheckHostDepends(Exception):
    """
    check depends host env or cmd failed
    """

    pass


class Build:
    BUILD_ENV = "Linux"
    SUPPORT_BUILD_ENV = ["Linux"]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    toolchain_dir = os.path.join(current_dir, "toolchains")
    _common_env_cmd_describe = {
        "cmake": [
            DependsHostType.COMMAND,
            "build tools, please install by: apt install cmake, or install from http://www.cmake.org/",
        ],
    }
    common_config = " -DCMAKE_BUILD_TYPE=Release -DBUILD_opencv_world=ON  -DBUILD_ANDROID_EXAMPLES=OFF  -DBUILD_ANDROID_PROJECTS=ON  -DBUILD_ANDROID_SERVICE=OFF  -DBUILD_CUDA_STUBS=OFF  -DBUILD_DOCS=OFF  -DBUILD_EXAMPLES=OFF  -DBUILD_FAT_JAVA_LIB=OFF  -DBUILD_JAVA=OFF  -DBUILD_PACKAGE=ON -DOPENCV_FORCE_3RDPARTY_BUILD=ON -DBUILD_opencv_gapi=OFF -DBUILD_PERF_TESTS=OFF -DBUILD_SHARED_LIBS=OFF -DBUILD_TBB=OFF -DBUILD_TESTS=OFF -DBUILD_WITH_DEBUG_INFO=ON -DBUILD_WITH_DYNAMIC_IPP=OFF -DBUILD_SHARED_LIBS=OFF -DBUILD_ZLIB:BOOL=ON -DBUILD_OPENJPEG:BOOL=OFF -DWITH_OPENJPEG=OFF -DWITH_ADE=OFF -DWITH_CUDA=OFF -DWITH_EIGEN=ON -DWITH_IMGCODEC_HDR=OFF -DWITH_IMGCODEC_PXM=OFF -DWITH_JPEG=ON -DWITH_LIBREALSENSE=OFF -DWITH_OPENEXR=OFF -DWITH_OPENMP=OFF -DWITH_PNG=OFF -DWITH_PROTOBUF=OFF -DWITH_PTHREADS_PF=OFF -DWITH_TBB=OFF -DWITH_TIFF=OFF -DWITH_CLP=OFF -DWITH_OPENCL_SVM=OFF -DWITH_IMGCODEC_SUNRAS=OFF -DWITH_IMGCODEC_SUNRASTER:BOOL=OFF -DWITH_JASPER:BOOL=OFF -DWITH_QUIRC:BOOL=OFF -DWITH_WEBP:BOOL=OFF -DWITH_ITT=OFF -D__ARM_NEON__=1 -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DOPENCV_ENABLE_MEMORY_SANITIZER=OFF -DANDROID_ARM_NEON=1 -DCMAKE_CXX_FLAGS=-Ofast -DCMAKE_C_FLAGS=-Ofast -DBUILD_ANDROID_EXAMPLES=OFF"

    def detect_build_env(self):
        self.BUILD_ENV = platform.system()
        assert (
            self.BUILD_ENV in self.SUPPORT_BUILD_ENV
        ), "now only support build env at: {}".format(self.SUPPORT_BUILD_ENV)

    def check_env(self):
        # env check
        self._common_env_cmd_describe["NDK_ROOT"] = [
            DependsHostType.ENVIRONMENT,
            "toolchain for build Android, please download from https://developer.android.google.cn/ndk/downloads ,then set it path to NDK_ROOT env",
        ]
        self._common_env_cmd_describe["gcc"] = [
            DependsHostType.COMMAND,
            "toolchain for host build, please install by: apt install gcc build-essential",
        ]
        self._common_env_cmd_describe["g++"] = [
            DependsHostType.COMMAND,
            "toolchain for host build, please install by: apt install g++ build-essential",
        ]
        self._common_env_cmd_describe["aarch64-linux-gnu-gcc"] = [
            DependsHostType.COMMAND,
            "toolchain for cross build, please download from: https://snapshots.linaro.org/gnu-toolchain/, then append it bin path to PATH env",
        ]
        self._common_env_cmd_describe["aarch64-linux-gnu-g++"] = [
            DependsHostType.COMMAND,
            "toolchain for cross build, please download from: https://snapshots.linaro.org/gnu-toolchain/, then append it bin path to PATH env",
        ]
        self._common_env_cmd_describe["arm-linux-gnueabi-gcc"] = [
            DependsHostType.COMMAND,
            "toolchain for cross build, please download from: https://snapshots.linaro.org/gnu-toolchain/, then append it bin path to PATH env",
        ]
        self._common_env_cmd_describe["arm-linux-gnueabi-g++"] = [
            DependsHostType.COMMAND,
            "toolchain for cross build, please download from: https://snapshots.linaro.org/gnu-toolchain/, then append it bin path to PATH env",
        ]

        for i in self._common_env_cmd_describe:
            key = i
            depends_type, help_msg = self._common_env_cmd_describe[i]
            if depends_type is DependsHostType.ENVIRONMENT:
                if key in os.environ:
                    env_value = os.environ.get(key)
                    logging.debug("env: {} value: {}".format(key, env_value))
                else:
                    logging.debug(
                        "check {}: {} failed, help msg: {}".format(
                            depends_type, key, help_msg
                        )
                    )
                    raise FrameworkFailCheckHostDepends
            elif depends_type is DependsHostType.COMMAND:
                try:
                    subprocess.check_output("which {}".format(key), shell=True)
                    logging.debug(
                        "host depends check {}: {} success".format(depends_type, key)
                    )
                except:
                    logging.debug(
                        "check {}: {} failed, help msg: {}".format(
                            depends_type, key, help_msg
                        )
                    )
                    raise FrameworkFailCheckHostDepends
            else:
                raise FrameworkFailCheckHostDepends

        ndk_path = os.environ.get("NDK_ROOT")
        self.android_toolchains = os.path.join(
            ndk_path, "build/cmake/android.toolchain.cmake"
        )
        assert os.path.isfile(
            self.android_toolchains
        ), "error config env: NDK_ROOT: {}, can not find android toolchains: {}".format(
            ndk_path, self.android_toolchains
        )
        logging.debug("use NDK toolchains: {}".format(self.android_toolchains))

    def build(self):
        self.detect_build_env()
        self.check_env()
        parser = argparse.ArgumentParser(description="prebuild for opencv project")

        parser.add_argument(
            "--opencv_repo_dir", type=str, required=True, help="opencv repo dir",
        )
        parser.add_argument(
            "--build_id",
            type=str,
            required=True,
            help="build id for opencv, for example: 4.5.5,",
        )

        args = parser.parse_args()
        # check opencv_repo_dir is valid and convert to abs path
        args.opencv_repo_dir = os.path.abspath(args.opencv_repo_dir)
        assert os.path.isdir(
            args.opencv_repo_dir
        ), "error config --opencv_repo_dir {} is not a valid dir: is not dir".format(
            args.opencv_repo_dir
        )

        # check args.opencv_repo_dir should have CMakeLists.txt
        assert os.path.isfile(
            os.path.join(args.opencv_repo_dir, "CMakeLists.txt")
        ), "error config --opencv_repo_dir {} is not a valid dir: can not find CMakeLists.txt".format(
            args.opencv_repo_dir
        )

        # do git fetch and checkout
        os.chdir(args.opencv_repo_dir)
        logging.info(
            "will do git reset --hard, which is dangerous, please make sure you know what you are doing!"
        )
        subprocess.check_call("git reset --hard && git clean -xdf", shell=True)
        logging.info("git fetch and checkout")
        subprocess.check_call("git fetch", shell=True)
        subprocess.check_call("git checkout {}".format(args.build_id), shell=True)

        # loop arch_os to build
        ARCH_OS_MAPS = {
            "x86_64_Linux": "",
            # "i386_Linux": "",
            "aarch64_Linux": f"-DCMAKE_TOOLCHAIN_FILE={os.path.join(self.toolchain_dir, 'aarch64-linux-gnu.toolchain.cmake')}",
            "armv7-a_Linux": f"-DCMAKE_TOOLCHAIN_FILE={os.path.join(self.toolchain_dir, 'arm-linux-gnueabi.toolchain.cmake')}",
            "aarch64_Android": f"-DCMAKE_TOOLCHAIN_FILE={self.android_toolchains} -DANDROID_ABI=arm64-v8a -DANDROID_PLATFORM=android-21",
            "armv7-a_Android": f"-DCMAKE_TOOLCHAIN_FILE={self.android_toolchains} -DANDROID_ABI=armeabi-v7a -DANDROID_PLATFORM=android-21",
        }

        for arch_os, toolchains_config in ARCH_OS_MAPS.items():
            build_dir = os.path.join(self.current_dir, "build_dir", arch_os)
            install_dir = os.path.join(
                self.current_dir, "opencv_build", args.build_id, arch_os
            )
            # force remove old
            if os.path.isdir(build_dir):
                subprocess.check_call(f"rm -rf {build_dir}", shell=True)
            if os.path.isdir(install_dir):
                subprocess.check_call(f"rm -rf {install_dir}", shell=True)
            # create new
            os.makedirs(build_dir, exist_ok=True)
            os.makedirs(install_dir, exist_ok=True)
            logging.info(
                f"start build for {arch_os} with toolchains_config: {toolchains_config} build_dir: {build_dir} install_dir: {install_dir}"
            )
            cmake_config = 'cmake -H\\"{}\\" -B\\"{}\\" {} -DCMAKE_INSTALL_PREFIX=\\"{}\\" {}'.format(
                args.opencv_repo_dir,
                build_dir,
                toolchains_config,
                install_dir,
                self.common_config,
            )

            if arch_os == "i386_Linux":
                cmake_config = "{} -DCMAKE_C_FLAGS=-m32 -DCMAKE_CXX_FLAGS=-m32".format(
                    cmake_config
                )

            config_cmd = "{}".format(cmake_config)
            logging.debug("cmake config: {}".format(config_cmd))
            subprocess.check_call('bash -c "{}"'.format(config_cmd), shell=True)
            build_cmd = f"cd {build_dir} && make -j$(nproc) install VERBOSE=1"
            logging.debug("cmake build: {}".format(build_cmd))
            subprocess.check_call('bash -c "{}"'.format(build_cmd), shell=True)


if __name__ == "__main__":
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y/%m/%d %H:%M:%S"
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

    b = Build()
    b.build()
