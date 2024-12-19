set(SCB_MSG_HEADER "Schmiddy's C/C++ Bootstrapper")
message("${SCB_MSG_HEADER}: Toolchain loaded")

set(VCPKG_TRIPLET_INCLUDE_DIR ${SCB_PROJECT_VCPKG_PATH}/installed/${VCPKG_TARGET_TRIPLET}/include) #-local-include
include_directories(${VCPKG_TRIPLET_INCLUDE_DIR})

message("Including triplet headers at '${VCPKG_TRIPLET_INCLUDE_DIR}'")
# THis file is primarily here to prevent CMAKE from trying to use another toolchain on your system.
# This way, we can avoid a lot of compatibility problems.