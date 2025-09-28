// genesis_builder.cpp - Complete version
#include "cryptonote_basic/cryptonote_format_utils.h"
#include "cryptonote_basic/cryptonote_basic.h"
#include "contrib/epee/include/string_tools.h"
#include <iostream>

int main() {
    cryptonote::transaction tx = AUTO_VAL_INIT(tx);
    
    // Set transaction version to 1
    tx.version = 1;
    
    // Create coinbase input
    cryptonote::txin_v txin;
    txin.type() = typeid(cryptonote::txin_gen);
    cryptonote::txin_gen& txin_gen = boost::get<cryptonote::txin_gen>(txin);
    txin_gen.height = 0;
    
    // Create output for 17.25M RSDT (17250000000000000000 atomic units)
    cryptonote::txout_to_key txout;
    // Use a standard Monero public key hash
    txout.key = crypto::public_key{{
        0x29,0xb2,0xe4,0xc0,0x28,0x1c,0x0b,0x02,
        0xe7,0xc5,0x32,0x91,0xa9,0x4d,0x1d,0x0c,
        0xbf,0xf8,0x88,0x3f,0x80,0x24,0xf5,0x14,
        0x2e,0xe4,0x94,0xff,0xbb,0xd0,0x88,0x07
    }};
    
    cryptonote::txout_target_v txout_target = txout;
    cryptonote::tx_out tx_out;
    tx_out.amount = 17250000000000000000ULL; // 17.25M RSDT in atomic units
    tx_out.target = txout_target;
    
    // Add input and output
    tx.vin.push_back(txin);
    tx.vout.push_back(tx_out);
    
    // Set unlock time
    tx.unlock_time = 0;
    
    // Set extra data - your message
    tx.extra = std::vector<uint8_t>{
        'C','e','n','s','o','r','s','h','i','p',' ','i','s',' ','c','o','n','t','r','o','l',';',' ','p','r','i','v','a','c','y',' ','i','s',' ','r','e','s','i','s','t','a','n','c','e'
    };
    
    // Convert to blob
    std::string blob;
    cryptonote::tx_to_blob(tx, blob);
    
    // Convert to hex
    std::string hex = epee::string_tools::buff_to_hex_nodelimer(blob);
    
    std::cout << "Genesis transaction: " << hex << std::endl;
    return 0;
}
