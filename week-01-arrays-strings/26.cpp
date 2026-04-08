class Solution {
    public:
        int removeDuplicates(vector<int>& nums) {
            if (nums.size() < 2) {
                return nums.size();
            }
            int uniqueCount = 1, ii = 1;
            while (ii < nums.size()) {
                if (nums[ii] == nums[ii-1]) {
                    ii++;
                } else {
                    // found a unique element
                    nums[uniqueCount++] = nums[ii++];
                }
            }
            return uniqueCount;
        }
    };