#include <iostream>
#include <cstdint>

int main() {
    const uint64_t COIN = 1000000000000ULL;
    std::cout << "COIN = " << COIN << std::endl;
    
    // Test each allocation
    uint64_t val1 = (uint64_t)4500000 * COIN;
    uint64_t val2 = (uint64_t)3750000 * COIN;
    uint64_t val3 = (uint64_t)3000000 * COIN;
    uint64_t val4 = (uint64_t)2250000 * COIN;
    uint64_t val5 = (uint64_t)1500000 * COIN;
    uint64_t val6 = (uint64_t)2750000 * COIN;
    uint64_t val7 = (uint64_t)2250000 * COIN;
    
    std::cout << "val1 = " << val1 << std::endl;
    std::cout << "val2 = " << val2 << std::endl;
    std::cout << "val3 = " << val3 << std::endl;
    std::cout << "val4 = " << val4 << std::endl;
    std::cout << "val5 = " << val5 << std::endl;
    std::cout << "val6 = " << val6 << std::endl;
    std::cout << "val7 = " << val7 << std::endl;
    
    uint64_t total = val1 + val2 + val3 + val4 + val5 + val6 + val7;
    std::cout << "total = " << total << std::endl;
    
    return 0;
}
