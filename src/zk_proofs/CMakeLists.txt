# Copyright (c) 2025, The RSDT Project
# 
# All rights reserved.

set(zk_proofs_sources
    zk_proofs.cpp
)

add_library(zk_proofs ${zk_proofs_sources})

target_link_libraries(zk_proofs
    crypto
    common
)

target_include_directories(zk_proofs PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

set_property(TARGET zk_proofs PROPERTY FOLDER "lib")

