INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_DVBC dvbc)

FIND_PATH(
    DVBC_INCLUDE_DIRS
    NAMES dvbc/api.h
    HINTS $ENV{DVBC_DIR}/include
        ${PC_DVBC_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    DVBC_LIBRARIES
    NAMES gnuradio-dvbc
    HINTS $ENV{DVBC_DIR}/lib
        ${PC_DVBC_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(DVBC DEFAULT_MSG DVBC_LIBRARIES DVBC_INCLUDE_DIRS)
MARK_AS_ADVANCED(DVBC_LIBRARIES DVBC_INCLUDE_DIRS)

