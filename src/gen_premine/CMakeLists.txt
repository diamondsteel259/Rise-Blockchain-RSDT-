# Copyright (c) 2025, The RSDT Project
# 
# All rights reserved.

set(gen_premine_sources
    gen_premine.cpp
)

add_executable(gen_premine ${gen_premine_sources})

target_link_libraries(gen_premine
    cryptonote_basic
    crypto
    common
    epee
)

set_property(TARGET gen_premine PROPERTY FOLDER "bin")

