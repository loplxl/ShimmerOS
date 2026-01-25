#include <iostream>
#include <thread>
#include <vector>
#include <cmath>
//thank you chatgptttttttt
void stressCPU(int id) {
    volatile double x = 0.0; // prevents compiler optimization
    while (true) {
        for (int i = 1; i < 1000000; ++i) {
            x += std::sqrt(i) * std::sin(i) * std::cos(i);
        }
    }
}

int main() {
    int numThreads = std::thread::hardware_concurrency(); // uses all CPU cores

    std::cout << "Starting infinite CPU stress test on " 
              << numThreads << " threads.\n";

    std::vector<std::thread> threads;
    for (int i = 0; i < numThreads; ++i) {
        threads.emplace_back(stressCPU, i);
    }

    for (auto &t : threads) {
        t.join(); // will never return
    }

    return 0;
}
