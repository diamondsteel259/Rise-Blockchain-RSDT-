#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>
#include <vector>
#include <ctime>
#include <cryptonote_basic/cryptonote_basic.h>
#include <cryptonote_basic/cryptonote_format_utils.h>
#include <crypto/crypto.h>
#include <cryptonote_config.h>
#include <ringct/rctTypes.h>
#include <common/base58.h>
#include <string_tools.h>

using namespace cryptonote;
using namespace epee;

struct PremineWallet {
    std::string name;
    uint64_t amount;
    std::string address;
    crypto::secret_key spend_key;
    crypto::secret_key view_key;
    std::string vesting_schedule;
};

void generate_premine_wallets() {
    std::vector<PremineWallet> wallets;
    
    // Premine allocation (20M RSDT total - 10% of 200M supply)
    wallets.push_back({"RSDT_Liquidity_1", 4500000 * COIN, "", crypto::secret_key{}, crypto::secret_key{}, "50% T1 listing, 50% @ $10M cap"});
    wallets.push_back({"RSDT_Development_1", 3750000 * COIN, "", crypto::secret_key{}, crypto::secret_key{}, "24-mo linear"});
    wallets.push_back({"RSDT_Marketing_1", 3000000 * COIN, "", crypto::secret_key{}, crypto::secret_key{}, "12-mo linear"});
    wallets.push_back({"RSDT_Team_1", 2250000 * COIN, "", crypto::secret_key{}, crypto::secret_key{}, "Custom vesting"});
    wallets.push_back({"RSDT_Treasury_1", 1500000 * COIN, "", crypto::secret_key{}, crypto::secret_key{}, "DAO after 6 months"});
    wallets.push_back({"RSDT_OTC_Sales", 2750000 * COIN, "", crypto::secret_key{}, crypto::secret_key{}, "18-mo linear"});
    wallets.push_back({"RSDT_Founder_Private", 2250000 * COIN, "", crypto::secret_key{}, crypto::secret_key{}, "50% launch, 25% @ 12mo, 25% @ halving"});
    
    // Generate keys and addresses for each wallet
    for (auto& wallet : wallets) {
        crypto::public_key spend_pub, view_pub;
        crypto::generate_keys(spend_pub, wallet.spend_key);
        crypto::generate_keys(view_pub, wallet.view_key);
        
        account_public_address addr;
        addr.m_spend_public_key = spend_pub;
        addr.m_view_public_key = view_pub;
        
        wallet.address = get_account_address_as_str(MAINNET, false, addr);
    }
    
    // Output to files
    std::ofstream premine_file("premine_wallets.txt");
    std::ofstream genesis_file("genesis_outputs.txt");
    
    premine_file << "RSDT Premine Wallet Configuration\n";
    premine_file << "==================================\n\n";
    
    genesis_file << "// RSDT Genesis Block Outputs\n";
    genesis_file << "// Generated: " << std::time(nullptr) << "\n\n";
    
    uint64_t total_premine = 0;
    for (const auto& wallet : wallets) {
        total_premine += wallet.amount;
        
        premine_file << "Wallet: " << wallet.name << "\n";
        premine_file << "Amount: " << wallet.amount / COIN << " RSDT\n";
        premine_file << "Address: " << wallet.address << "\n";
        premine_file << "Vesting: " << wallet.vesting_schedule << "\n";
        premine_file << "Spend Key: " << string_tools::pod_to_hex(wallet.spend_key) << "\n";
        premine_file << "View Key: " << string_tools::pod_to_hex(wallet.view_key) << "\n\n";
        
        genesis_file << "// " << wallet.name << " - " << wallet.amount / COIN << " RSDT\n";
        genesis_file << "// " << wallet.vesting_schedule << "\n";
        genesis_file << "// Address: " << wallet.address << "\n";
        genesis_file << "// Spend Key: " << string_tools::pod_to_hex(wallet.spend_key) << "\n";
        genesis_file << "// View Key: " << string_tools::pod_to_hex(wallet.view_key) << "\n\n";
    }
    
    premine_file << "Total Premine: " << total_premine / COIN << " RSDT\n";
    premine_file << "Genesis Message: \"Censorship is control; privacy is resistance\"\n";
    premine_file << "Genesis Date: 2026-01-01T00:00:00Z\n";
    
    std::cout << "Generated " << wallets.size() << " premine wallets\n";
    std::cout << "Total premine: " << total_premine / COIN << " RSDT\n";
    std::cout << "Files created: premine_wallets.txt, genesis_outputs.txt\n";
}

int main() {
    try {
        generate_premine_wallets();
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}
