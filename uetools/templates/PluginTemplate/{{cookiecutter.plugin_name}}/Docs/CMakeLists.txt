#       Doxygen
# ==================================
#   Doxygen parse the C++ files/comments to generate the documentation
FIND_PACKAGE(Doxygen REQUIRED)
FIND_PACKAGE(Sphinx REQUIRED)

SET(DOXYGEN_OUTPUT_DIR "${CMAKE_BINARY_DIR}")

IF(DOXYGEN_FOUND)
    CONFIGURE_FILE(${CMAKE_CURRENT_SOURCE_DIR}/Doxyfile.in
                   ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile @ONLY)

    ADD_CUSTOM_TARGET(doxygen ${DOXYGEN_EXECUTABLE}
                              ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile
              WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
         COMMENT "Generating API documentation with Doxygen" VERBATIM
    )
ENDIF(DOXYGEN_FOUND)

#       Sphinx
# ==================================
#   Sphinx use the information generate by doxygen to display nice documentation

IF(SPHINX_FOUND)
    # build documentation
    ADD_CUSTOM_TARGET(sphinx ALL
        COMMAND sphinx-build -W --color
            -Dbreathe_projects.GameKit=${DOXYGEN_OUTPUT_DIR}
            -c "${CMAKE_SOURCE_DIR}/Docs/"
            -b html "${CMAKE_SOURCE_DIR}/Docs/" "${CMAKE_BINARY_DIR}/Docs/html")
    ADD_DEPENDENCIES(sphinx doxygen)

    # Serve documentation locally
    ADD_CUSTOM_TARGET(sphinx-serve ALL
        COMMAND sphinx-serve -b Docs)

    ADD_DEPENDENCIES(sphinx-serve sphinx)
ENDIF(SPHINX_FOUND)


# Dummy target for IDE that need files to be used in a target to display them
FILE(GLOB_RECURSE DOC_SRC *.rst *.py *.txt Doxyfile.in)
ADD_CUSTOM_TARGET(docs ALL SOURCES ${DOC_SRC})



