# Create a library called "libfluxDet" which includes the source files given in
# the array .
# The extension is already found.  Any number of sources could be listed here.

set(INCLUDE_DIRECTORIES
${CMAKE_SOURCE_DIR}/shipdata
${CMAKE_SOURCE_DIR}/fluxDet
)

include_directories( ${INCLUDE_DIRECTORIES} ${FAIRROOT_INCLUDE_DIR} ${FairLogger_INCDIR} ${FMT_INCLUDE_DIR}
)
include_directories(SYSTEM ${SYSTEM_INCLUDE_DIRECTORIES})

set(LINK_DIRECTORIES
${ROOT_LIBRARY_DIR}
${FAIRROOT_LIBRARY_DIR}
) 

link_directories( ${LINK_DIRECTORIES})

set(SRCS
#Put here your sourcefiles
fluxDetPoint.cxx
fluxDetHit.cxx
fluxDet.cxx
)

Set(LINKDEF fluxDetLinkDef.h)
Set(LIBRARY_NAME fluxDet)
Set(DEPENDENCIES
    Base ShipData
)

GENERATE_LIBRARY()
