#include <iostream>
#include <cstdint>

int main() {
    const uint64_t COIN = 1000000000000ULL;
    uint64_t test = (uint64_t)4500000 * COIN;
    std::cout << "COIN = " << COIN << std::endl;
    std::cout << "4500000 * COIN = " << test << std::endl;
    std::cout << "4500000 * COIN / COIN = " << test / COIN << std::endl;
    return 0;
}
