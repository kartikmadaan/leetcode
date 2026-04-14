class Solution {
    public:
        int maxProfit(vector<int>& prices) {
            if(prices.size() == 1) return 0;
            int minTillNow = prices[0];
            int maxProfit = 0;
            int i = 0, j = prices.size() - 1;
            while (i < j) {
                if (i + 1 < prices.size() && prices[i+1] < minTillNow) {
                    minTillNow = prices[i + 1];
                }
                i++;
                maxProfit = max(maxProfit, prices[i] - minTillNow);
            }
            return maxProfit;
        }
    };