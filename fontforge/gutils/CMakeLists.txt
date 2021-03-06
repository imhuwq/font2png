# Distributed under the original FontForge BSD 3-clause license

add_library(gutils OBJECT
  dlist.c
  fsys.c
  gcol.c
  g_giomime.c
  gimagebmpP.h
  gimage.c
  gimagereadbmp.c
  gimageread.c
  gimagereadgif.c
  gimagereadjpeg.c
  gimagereadpng.c
  gimagereadras.c
  gimagereadrgb.c
  gimagereadtiff.c
  gimagereadxbm.c
  gimagereadxpm.c
  gimagewritebmp.c
  gimagewritegimage.c
  gimagewritejpeg.c
  gimagewritepng.c
  gimagewritexbm.c
  gimagewritexpm.c
  gio.c
  giofile.c
  giofuncP.h
  giotrans.c
  gutils.c
  gwwintl.c
  prefs.c
  unicodelibinfo.c
)

set_property(TARGET gutils PROPERTY POSITION_INDEPENDENT_CODE ON)

list(APPEND gutils_LIBRARIES GIF::GIF)
list(APPEND gutils_LIBRARIES JPEG::JPEG)
list(APPEND gutils_LIBRARIES PNG::PNG)
list(APPEND gutils_LIBRARIES TIFF::TIFF)

if(${CMAKE_VERSION} VERSION_LESS "3.12.0")
  make_object_interface(gutils
    fontforge_common_headers
    gunicode_interface
    ${gutils_LIBRARIES}
  )
else()
  target_link_libraries(gutils
    PUBLIC
      fontforge_common_headers
      gunicode
      ${gutils_LIBRARIES}
  )
endif()
