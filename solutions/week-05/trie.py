"""
Problem: Implement Trie (Prefix Tree) (LeetCode #208)
Difficulty: Medium

A trie (prefix tree) is a tree data structure used to efficiently store 
and retrieve keys in a dataset of strings.

Implement the Trie class:
- Trie() Initializes the trie object.
- void insert(String word) Inserts word into the trie.
- boolean search(String word) Returns true if word is in the trie.
- boolean startsWith(String prefix) Returns true if there is a word with prefix.

Time Complexity: O(m) for all operations where m is the word/prefix length
Space Complexity: O(ALPHABET_SIZE * m * n) where n is number of words
"""

from typing import List, Optional


class TrieNode:
    """A node in the Trie"""
    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.is_end = False  # Marks end of a complete word
        self.word = None  # Optional: store the complete word


class Trie:
    """
    Prefix Tree (Trie) Implementation
    
    Use cases:
    - Autocomplete
    - Spell checker
    - IP routing (longest prefix match)
    - Word games (Boggle, Wordle)
    """
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        """Insert a word into the trie. O(m)"""
        node = self.root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end = True
        node.word = word  # Store complete word for easy retrieval
    
    def search(self, word: str) -> bool:
        """Returns true if word is in the trie. O(m)"""
        node = self._find_node(word)
        return node is not None and node.is_end
    
    def startsWith(self, prefix: str) -> bool:
        """Returns true if there's any word with given prefix. O(m)"""
        return self._find_node(prefix) is not None
    
    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        """Find the node corresponding to prefix, or None if not found."""
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        
        return node
    
    # Additional useful methods
    
    def get_all_words_with_prefix(self, prefix: str) -> List[str]:
        """Get all words starting with prefix (autocomplete)"""
        result = []
        node = self._find_node(prefix)
        
        if node is None:
            return result
        
        self._collect_words(node, result)
        return result
    
    def _collect_words(self, node: TrieNode, result: List[str]) -> None:
        """DFS to collect all words from this node"""
        if node.is_end and node.word:
            result.append(node.word)
        
        for child in node.children.values():
            self._collect_words(child, result)
    
    def delete(self, word: str) -> bool:
        """Delete a word from the trie. Returns True if word existed."""
        def _delete(node: TrieNode, word: str, depth: int) -> bool:
            if depth == len(word):
                if not node.is_end:
                    return False  # Word doesn't exist
                node.is_end = False
                node.word = None
                return len(node.children) == 0  # Can delete if no children
            
            char = word[depth]
            if char not in node.children:
                return False
            
            should_delete_child = _delete(node.children[char], word, depth + 1)
            
            if should_delete_child:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end
            
            return False
        
        _delete(self.root, word, 0)
        return True


class WordDictionary:
    """
    Design Add and Search Words Data Structure (LeetCode #211)
    
    Supports '.' wildcard that matches any single character.
    """
    
    def __init__(self):
        self.root = TrieNode()
    
    def addWord(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word: str) -> bool:
        """Search with '.' wildcard support using DFS"""
        def dfs(node: TrieNode, i: int) -> bool:
            if i == len(word):
                return node.is_end
            
            char = word[i]
            
            if char == '.':
                # Try all possible characters
                for child in node.children.values():
                    if dfs(child, i + 1):
                        return True
                return False
            else:
                if char not in node.children:
                    return False
                return dfs(node.children[char], i + 1)
        
        return dfs(self.root, 0)


def visualize_trie(trie: Trie, prefix: str = ""):
    """Visualize trie structure"""
    
    def _visualize(node: TrieNode, prefix: str, indent: str):
        for char, child in sorted(node.children.items()):
            end_marker = "*" if child.is_end else ""
            print(f"{indent}├── {char}{end_marker}")
            _visualize(child, prefix + char, indent + "│   ")
    
    print(f"\nTrie Structure:")
    print("root")
    _visualize(trie.root, "", "")


# Test cases
if __name__ == "__main__":
    # Test basic Trie
    trie = Trie()
    
    words = ["apple", "app", "application", "banana", "band", "bandana"]
    for word in words:
        trie.insert(word)
    
    print("Basic Trie Operations:")
    print(f"  search('apple'): {trie.search('apple')}")  # True
    print(f"  search('app'): {trie.search('app')}")      # True
    print(f"  search('appl'): {trie.search('appl')}")    # False
    print(f"  startsWith('app'): {trie.startsWith('app')}")  # True
    print(f"  startsWith('ban'): {trie.startsWith('ban')}")  # True
    print(f"  startsWith('cat'): {trie.startsWith('cat')}")  # False
    
    # Autocomplete
    print(f"\n  Words with prefix 'app': {trie.get_all_words_with_prefix('app')}")
    print(f"  Words with prefix 'ban': {trie.get_all_words_with_prefix('ban')}")
    
    # Visualize
    visualize_trie(trie)
    
    # Test WordDictionary with wildcards
    print("\n" + "=" * 50)
    print("WordDictionary with Wildcards:")
    
    wd = WordDictionary()
    wd.addWord("bad")
    wd.addWord("dad")
    wd.addWord("mad")
    
    print(f"  search('pad'): {wd.search('pad')}")    # False
    print(f"  search('bad'): {wd.search('bad')}")    # True
    print(f"  search('.ad'): {wd.search('.ad')}")    # True
    print(f"  search('b..'): {wd.search('b..')}")    # True
    print(f"  search('...'): {wd.search('...')}")    # True (matches 3-letter words)
    
    print("\n✓ All tests passed!")

