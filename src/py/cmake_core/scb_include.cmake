set(SCB_MSG_HEADER "Schmiddy's C/C++ Bootstrapper")
message("${SCB_MSG_HEADER}: Include file loaded")

# Call this macro at the top of your CMakeLists.txt
macro(scb_init_project)
    scb_load_config_file()
    scb_vcpkg_bootstrap()
    scb_vcpkg_install_packages()
endmacro()

# LOAD CONFIG DATA:
macro(scb_load_config_file)
    # Reading Project info from the config file:
    message("${SCB_MSG_HEADER}: Loading config at '${CMAKE_SOURCE_DIR}/scb_project_config.json'")
    set(SCB_CONFIG_PATH "${CMAKE_SOURCE_DIR}/scb_project_config.json")
    file(READ "${SCB_CONFIG_PATH}" SCB_CONFIG_STRING)
    
    # Loading Config Variables:
    string(JSON SCB_PROJECT_NAME GET "${SCB_CONFIG_STRING}" "name")
    string(JSON SCB_PROJECT_VERSION GET "${SCB_CONFIG_STRING}" "version")
    string(JSON SCB_PROJECT_DESCRIPTION GET "${SCB_CONFIG_STRING}" "description")
    string(JSON SCB_PROJECT_AUTHORS GET "${SCB_CONFIG_STRING}" "authors")
    string(JSON SCB_PROJECT_VCPKG_PATH_STR GET "${SCB_CONFIG_STRING}" "vcpkg" "local_path")
    string(JSON SCB_PROJECT_VCPKG_PACKAGE_COUNT LENGTH "${SCB_CONFIG_STRING}" "vcpkg" "packages")
    string(JSON SCB_PROJECT_VCPKG_PACKAGES GET "${SCB_CONFIG_STRING}" "vcpkg" "packages")

    set(SCB_PROJECT_VCPKG_PATH "${CMAKE_SOURCE_DIR}/${SCB_PROJECT_VCPKG_PATH_STR}")
    message("${SCB_MSG_HEADER}: Project VCPKG instance located at '${SCB_PROJECT_VCPKG_PATH}'")

endmacro()

## VCPKG HANDLING:
macro(scb_vcpkg_bootstrap)
    _scb_install_or_update_vcpkg()

    # Find out whether the user supplied their own VCPKG toolchain file
    if(NOT DEFINED ${CMAKE_TOOLCHAIN_FILE})
        # We know this wasn't set before so we need point the toolchain file to the newly found SCB_PROJECT_VCPKG_PATH
        set(CMAKE_TOOLCHAIN_FILE ${SCB_PROJECT_VCPKG_PATH}/scripts/buildsystems/vcpkg.cmake CACHE STRING "")
    endif()

    # Just setting vcpkg.cmake as toolchain file does not seem to actually pull in the code
    include(${SCB_PROJECT_VCPKG_PATH}/scripts/buildsystems/vcpkg.cmake)
    
    message(STATUS "${SCB_MSG_HEADER}: VCPKG Status:")
    message(STATUS "\tVCPKG Location: ${SCB_PROJECT_VCPKG_PATH}")
    message(STATUS "\tVCPKG Executable : ${VCPKG_EXEC}")
    message(STATUS "\tVCPKG Bopotstrapper Script: ${VCPKG_BOOTSTRAP}")
endmacro()

macro(_scb_install_or_update_vcpkg)
    if(NOT EXISTS ${SCB_PROJECT_VCPKG_PATH})
        message(STATUS "Cloning VCPKG in ${SCB_PROJECT_VCPKG_PATH}")
        execute_process(COMMAND git clone https://github.com/Microsoft/vcpkg.git ${SCB_PROJECT_VCPKG_PATH})

        # If a reproducible build is desired (and potentially old libraries are # ok), uncomment the
        # following line and pin the vcpkg repository to a specific githash.
        # execute_process(COMMAND git checkout 745a0aea597771a580d0b0f4886ea1e3a94dbca6 WORKING_DIRECTORY ${SCB_PROJECT_VCPKG_PATH})
    else()
        # The following command has no effect if the vcpkg repository is in a detached head state.
        message(STATUS "Auto-updating VCPKG in ${SCB_PROJECT_VCPKG_PATH}")
        execute_process(COMMAND git pull WORKING_DIRECTORY ${SCB_PROJECT_VCPKG_PATH})
    endif()

    if(NOT EXISTS ${SCB_PROJECT_VCPKG_PATH}/README.md)
        message(FATAL_ERROR "***** FATAL ERROR: Could not clone VCPKG *****")
    endif()

    if(WIN32)
        set(VCPKG_EXEC ${SCB_PROJECT_VCPKG_PATH}/vcpkg.exe)
        set(VCPKG_BOOTSTRAP ${SCB_PROJECT_VCPKG_PATH}/bootstrap-vcpkg.bat)
    else()
        set(VCPKG_EXEC ${SCB_PROJECT_VCPKG_PATH}/vcpkg)
        set(VCPKG_BOOTSTRAP ${SCB_PROJECT_VCPKG_PATH}/bootstrap-vcpkg.sh)
    endif()

    if(NOT EXISTS ${VCPKG_EXEC})
        message("Bootstrapping vcpkg in ${SCB_PROJECT_VCPKG_PATH}")
        execute_process(COMMAND ${VCPKG_BOOTSTRAP} WORKING_DIRECTORY ${SCB_PROJECT_VCPKG_PATH})
    endif()

    if(NOT EXISTS ${VCPKG_EXEC})
        message(FATAL_ERROR "***** FATAL ERROR: Could not bootstrap VCPKG *****")
    endif()
   
endmacro()

# Installs the list of packages from the config
macro(scb_vcpkg_install_packages)

    message(STATUS "${SCB_MSG_HEADER}: Installing/Updating the following packages: ${SCB_PROJECT_VCPKG_PACKAGES}")
    message(STATUS "${SCB_MSG_HEADER}: Target VCPKG Triplet = ${VCPKG_TARGET_TRIPLET}")
    math(EXPR MAX_INDEX "${SCB_PROJECT_VCPKG_PACKAGE_COUNT} - 1" )
    # Loop through each element of the JSON array
    foreach(IDX RANGE ${MAX_INDEX})
        # Get the name from the current JSON element.
        string(JSON CUR_PACKAGE GET ${SCB_PROJECT_VCPKG_PACKAGES} ${IDX})

        if(NOT DEFINED VCPKG_TARGET_TRIPLET)
            set(INSTALL_STR "${CUR_PACKAGE}")
        else()
            set(INSTALL_STR "${CUR_PACKAGE}:${VCPKG_TARGET_TRIPLET}")
        endif()
        message(STATUS "> Installing ${INSTALL_STR}")

        execute_process(
            COMMAND ${VCPKG_EXEC} install "${INSTALL_STR}"
            WORKING_DIRECTORY ${SCB_PROJECT_VCPKG_PATH}
        )
    endforeach()
endmacro()
