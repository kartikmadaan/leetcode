/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
 class Solution {
    public:
    
        int minDepth(TreeNode* root) {
            if (!root)
                return 0;
            queue<pair<TreeNode*, int>> q;
            q.push({root, 1});
            while(!q.empty()) {
                auto top = q.front();
                if (!top.first->left && !top.first->right)
                    return top.second;
                q.pop();
                if (top.first->left)
                    q.push({top.first->left, 1 + top.second});
                if (top.first->right)
                    q.push({top.first->right, 1 + top.second});
            }
            return 0;
        }
    };