cmake_minimum_required(VERSION 3.10)

project(WebSocketListener)

set(CMAKE_CXX_STANDARD 17)

include_directories(
    ${CMAKE_SOURCE_DIR}/websocketpp
    /usr/include/boost
    /usr/include/openssl
    /usr/include/jsoncpp
)

set(SOURCE_FILES listener_wbsckt.cpp)

add_executable(main ${SOURCE_FILES})

target_link_libraries(main
    boost_system
    ssl
    crypto
    jsoncpp
)

# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17")
