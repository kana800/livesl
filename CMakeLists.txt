cmake_minimum_required(VERSION 3.8)

project(generator CXX)

set(SRCES 
	"generator/generator.cpp"
)

set(HEADERS 
	"generator/htmltemplate.hpp"
)

add_subdirectory("external/json")

add_executable(generator ${SRCES})

target_link_libraries(generator 
	PRIVATE nlohmann_json::nlohmann_json
)

if (CMAKE_VERSION VERSION_GREATER 3.12)
  set_property(TARGET generator PROPERTY CXX_STANDARD 20)
endif()
