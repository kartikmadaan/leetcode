class Solution {
    public:
        TreeNode* sortedArrayToBST(vector<int>& nums) {
            if (nums.size() == 0)
                return NULL;
            if (nums.size() == 1)
                return new TreeNode(nums[0]);
            int mid = (nums.size()/2);
            vector<int> leftHalf(nums.begin(), nums.begin() + mid);
            TreeNode* left = sortedArrayToBST(leftHalf);
            vector<int> rightHalf(nums.begin() + mid + 1, nums.end());
            TreeNode* right = sortedArrayToBST(rightHalf);
            TreeNode* root = new TreeNode(nums[mid], left, right);
            return root;
        }
    };