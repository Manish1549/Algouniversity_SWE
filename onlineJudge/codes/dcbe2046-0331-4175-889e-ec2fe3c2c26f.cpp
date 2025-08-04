//write your solution
#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> seen;  // value -> index

    for (int i = 0; i < nums.size(); i++) {
        int complement = target - nums[i];

        // Check if complement exists in map
        if (seen.find(complement) != seen.end()) {
            return {seen[complement], i};
        }

        // Store current number with index
        seen[nums[i]] = i;
    }

    return {}; // Should never reach here if one solution exists
}

int main() {
    vector<int> nums = {2, 7, 11, 15};
    int target = 9;

    vector<int> result = twoSum(nums, target);

    cout << "[" << result[0] << "," << result[1] << "]" << endl;

    return 0;
}