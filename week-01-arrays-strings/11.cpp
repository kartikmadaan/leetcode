class Solution {
    public:
        int maxArea(vector<int>& height) {
            int bestLeft = 0, bestRight = height.size() - 1, maxArea = 0;
            int i = 0, j = height.size() - 1;
            while(i < j) {
                int area = min(height[i], height[j]) * (j - i);
                if (area > maxArea) {
                    maxArea = area;
                    bestLeft = i;
                    bestRight = j;
                }
                if ((i + 1 < j) && height[j] > height[i]){
                    i++;
                } else {
                    j--;
                }
            }
            return maxArea;
        }
    };