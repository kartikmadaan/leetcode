class Solution {
    public:
        vector<int> twoSum(vector<int>& nums, int target) {
            vector<int> ans(2);
            unordered_map<int, int> hashMap;
            for (int ii = 0; ii < nums.size(); ii++) {
                if (hashMap.count(target - nums[ii])) {
                    ans[0] = hashMap[target-nums[ii]];
                    ans[1] = ii;
                    return ans;
                }
                hashMap[nums[ii]] = ii;
            }
            return ans;
        }
    };