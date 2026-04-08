class Solution {
    public:
        bool isPalindrome(string s) {
            if (s.size() == 1){
                return true;
            }
            int i = 0, j = s.length();
            while (i < j) {
                while(!isalnum(s[i]) && (i < j)) {
                    i++;
                }
                while(!isalnum(s[j]) && (j > i)) {
                    j--;
                }
                if ((i < j) && tolower(s[i]) != tolower(s[j])){
                    return false;
                }
                i++;
                j--;
            }
            return true;
        }
    };