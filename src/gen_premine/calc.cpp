#include <iostream>
#include <cstdint>

int main() {
    const uint64_t COIN = 1000000000000ULL;
    uint64_t total = 20000000ULL * COIN;
    std::cout << "20M RSDT should be: " << total << " atomic units" << std::endl;
    return 0;
}
