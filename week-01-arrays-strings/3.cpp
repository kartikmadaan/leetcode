class Solution {
    public:
        int lengthOfLongestSubstring(string s) {
            if(s.size() <= 1) return s.size();
            unordered_map<char, int> charMap;
            int start = 0, maxLen = 1;
            charMap[s[0]] = 0;
            for (int i = 1; i < s.size(); i++) {
                if (!charMap.count(s[i])) {
                    charMap[s[i]] = i;
                    maxLen = max(maxLen, i - start + 1);
                } else {
                    for (auto it = charMap.begin(); it != charMap.end();) {
                        if (it->second < charMap[s[i]]) {
                           it = charMap.erase(it);
                        } else{
                            it++;
                        }
                    }
                    start = charMap[s[i]] + 1;
                    charMap[s[i]] = i;
                }
            }
            return maxLen;
        }
    };