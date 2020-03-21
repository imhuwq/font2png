# Distributed under the original FontForge BSD 3-clause license

add_library(fontforge_pymodule SHARED python.c)
target_link_libraries(fontforge_pymodule PUBLIC Python3::Python)

set_target_properties(fontforge_pymodule PROPERTIES OUTPUT_NAME "fontforge" PREFIX "")

if (WIN32)
    set_target_properties(fontforge_pymodule PROPERTIES SUFFIX ".pyd")
endif ()

target_link_libraries(fontforge_pymodule PRIVATE fontforge)
