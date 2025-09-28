#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>
#include <vector>
#include <ctime>
#include <sstream>
#include <algorithm>
#include <cstdint>

// Simplified structure for public-only premine information
struct PremineAllocation {
    std::string name;
    uint64_t amount_rsdt;
    uint64_t amount_atomic;
    std::string vesting_schedule;
    std::string purpose;
    
    // Constructor for easier initialization
    PremineAllocation(const std::string& n, uint64_t rsdt, uint64_t atomic, 
                     const std::string& vesting, const std::string& purp)
        : name(n), amount_rsdt(rsdt), amount_atomic(atomic), 
          vesting_schedule(vesting), purpose(purp) {}
};

// Define COIN constant (1 RSDT = 10^12 atomic units)
const uint64_t COIN = 1000000000000ULL;

void generate_public_premine_info() {
    std::vector<PremineAllocation> allocations;
    
    // Premine allocation (20M RSDT total - 10% of 200M supply)
    allocations.push_back(PremineAllocation("RSDT_Liquidity_1", 4500000, (uint64_t)4500000 * COIN, "50% T1 listing, 50% @ $10M cap", "Exchange liquidity and market making"));
    allocations.push_back(PremineAllocation("RSDT_Development_1", 3750000, (uint64_t)3750000 * COIN, "24-mo linear", "Core development and maintenance"));
    allocations.push_back(PremineAllocation("RSDT_Marketing_1", 3000000, (uint64_t)3000000 * COIN, "12-mo linear", "Marketing and community growth"));
    allocations.push_back(PremineAllocation("RSDT_Team_1", 2250000, (uint64_t)2250000 * COIN, "Custom vesting", "Core team compensation"));
    allocations.push_back(PremineAllocation("RSDT_Treasury_1", 1500000, (uint64_t)1500000 * COIN, "DAO after 6 months", "DAO treasury and governance"));
    allocations.push_back(PremineAllocation("RSDT_OTC_Sales", 2750000, (uint64_t)2750000 * COIN, "18-mo linear", "Over-the-counter sales"));
    allocations.push_back(PremineAllocation("RSDT_Founder_Private", 2250000, (uint64_t)2250000 * COIN, "50% launch, 25% @ 12mo, 25% @ halving", "Founder allocation"));
    
    // Create output files
    std::ofstream premine_file("premine_public_info.txt");
    std::ofstream csv_file("premine_allocations.csv");
    
    if (!premine_file.is_open() || !csv_file.is_open()) {
        std::cerr << "Error: Could not create output files" << std::endl;
        return;
    }
    
    // Write header for text file
    premine_file << "RSDT Premine Public Information (No Private Keys)\n";
    premine_file << "==================================================\n\n";
    premine_file << "Generated: " << std::time(nullptr) << "\n";
    premine_file << "Genesis Message: \"Censorship is control; privacy is resistance\"\n";
    premine_file << "Genesis Date: 2026-01-01T00:00:00Z\n\n";
    
    // Write CSV header
    csv_file << "wallet_name,amount_rsdt,amount_atomic,vesting_schedule,purpose\n";
    
    // Note: Due to uint64_t limitations, we calculate total in RSDT units to avoid overflow
    uint64_t total_rsdt = 0;
    for (const auto& allocation : allocations) {
        total_rsdt += allocation.amount_rsdt;
        
        // Write to text file
        premine_file << "Wallet: " << allocation.name << "\n";
        premine_file << "Amount: " << allocation.amount_rsdt << " RSDT\n";
        premine_file << "Amount (atomic): " << allocation.amount_atomic << "\n";
        premine_file << "Purpose: " << allocation.purpose << "\n";
        premine_file << "Vesting: " << allocation.vesting_schedule << "\n\n";
        
        // Write to CSV file (escape quotes in strings)
        csv_file << allocation.name << ","
                 << allocation.amount_rsdt << ","
                 << allocation.amount_atomic << ",\""
                 << allocation.vesting_schedule << "\",\""
                 << allocation.purpose << "\"\n";
    }
    
    premine_file << "Total Premine: " << total_rsdt << " RSDT\n";
    premine_file << "Total Premine (atomic): [OVERFLOW - use individual amounts]\n";
    premine_file << "Percentage of total supply: " << (total_rsdt * 100 / 200000000) << "%\n\n";
    
    premine_file << "IMPORTANT NOTE:\n";
    premine_file << "===============\n";
    premine_file << "The total premine amount in atomic units exceeds uint64_t limits.\n";
    premine_file << "Individual wallet amounts are calculated correctly.\n";
    premine_file << "For genesis block creation, use individual amounts or upgrade to uint128_t.\n\n";
    
    premine_file << "SECURITY NOTICE:\n";
    premine_file << "================\n";
    premine_file << "This file contains only public allocation information.\n";
    premine_file << "No private keys, addresses, or sensitive cryptographic material included.\n";
    premine_file << "Official addresses must be generated offline using air-gapped systems.\n";
    premine_file << "Private keys should never be stored in version control systems.\n";
    
    premine_file.close();
    csv_file.close();
    
    std::cout << "Generated public premine information files:\n";
    std::cout << "- premine_public_info.txt (detailed text format)\n";
    std::cout << "- premine_allocations.csv (CSV format for processing)\n";
    std::cout << "Total allocations: " << allocations.size() << "\n";
    std::cout << "Total premine: " << total_rsdt << " RSDT\n";
    std::cout << "\nWARNING: Total atomic amount exceeds uint64_t - individual amounts are correct.\n";
    std::cout << "NOTE: This generator creates only public allocation information.\n";
    std::cout << "Address generation and private key management should be done offline.\n";
}

int main() {
    try {
        generate_public_premine_info();
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}
