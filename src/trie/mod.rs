use std::collections::HashMap;

#[derive(Clone, Debug)]
pub struct Triers {
    children: HashMap<char, Box<Triers>>,
    is_end: bool,
}

impl Default for Triers {
    fn default() -> Self {
        Self::new()
    }
}

impl Triers {
    pub fn new() -> Self {
        Self {
            children: HashMap::new(),
            is_end: false,
        }
    }

    pub fn insert(&mut self, word: &str) {
        let mut node = self;
        for ch in word.chars() {
            node = node
                .children
                .entry(ch)
                .or_insert_with(|| Box::new(Triers::new()));
        }
        node.is_end = true;
    }

    pub fn search(&self, word: &str) -> bool {
        let mut node = self;
        for ch in word.chars() {
            match node.children.get(&ch) {
                Some(child) => node = child,
                None => return false,
            }
        }
        node.is_end
    }

    pub fn starts_with(&self, prefix: &str) -> bool {
        let mut node = self;
        for ch in prefix.chars() {
            match node.children.get(&ch) {
                Some(child) => node = child,
                None => return false,
            }
        }
        true
    }

    pub fn delete(&mut self, word: &str) -> bool {
        Self::delete_rec(self, word, 0)
    }

    fn delete_rec(node: &mut Triers, word: &str, depth: usize) -> bool {
        if depth == word.len() {
            if !node.is_end {
                return false;
            }
            node.is_end = false;
            return node.children.is_empty();
        }

        let ch = word[depth..].chars().next().unwrap();
        if let Some(child) = node.children.get_mut(&ch) {
            if Self::delete_rec(child, word, depth + 1) {
                node.children.remove(&ch);
                return node.children.is_empty() && !node.is_end;
            }
        }
        false
    }

    pub fn word_count(&self) -> usize {
        let mut count = 0;
        if self.is_end {
            count += 1;
        }
        for child in self.children.values() {
            count += child.word_count();
        }
        count
    }

    pub fn collect_words(&self) -> Vec<String> {
        let mut result = Vec::new();
        let mut prefix = String::new();
        Self::collect_rec(self, &mut prefix, &mut result);
        result
    }

    fn collect_rec(
        node: &Triers,
        prefix: &mut String,
        result: &mut Vec<String>,
    ) {
        if node.is_end {
            result.push(prefix.clone());
        }
        for (&ch, child) in &node.children {
            prefix.push(ch);
            Self::collect_rec(child, prefix, result);
            prefix.pop();
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use rstest::rstest;

    #[rstest]
    #[case("hello", "hello", true)]
    #[case("case", "cast", false)]
    #[case("cat", "cat", true)]
    #[case("card", "capt", false)]
    #[case("some_word", "", false)]
    fn search_checks(
        #[case] word_to_insert: &str,
        #[case] word: &str,
        #[case] expected: bool,
    ) {
        let mut t = Triers::new();
        t.insert(word_to_insert);
        assert_eq!(t.search(word), expected);
    }

    #[rstest]
    #[case("hello", "h", true)]
    #[case("case", "cast", false)]
    #[case("cat", "at", false)]
    #[case("pinned", "pinn", true)]
    #[case("pinned", "", true)]

    fn start_with_checks(
        #[case] word_to_insert: &str,
        #[case] prefix: &str,
        #[case] expected: bool,
    ) {
        let mut t = Triers::new();
        t.insert(word_to_insert);
        assert_eq!(t.starts_with(prefix), expected);
    }

    #[rstest]
    #[case("hello", "world", false)]
    #[case("cup", "cup", true)]
    #[case("", "", true)]
    #[case("map", "mat", false)]
    fn delete_checks(
        #[case] word_to_insert: &str,
        #[case] word_to_delete: &str,
        #[case] expected: bool,
    ) {
        let mut t = Triers::new();
        t.insert(word_to_insert);
        assert_eq!(t.delete(word_to_delete), expected);
    }

    #[rstest]
    #[case(&["hi", "honey"], 2)]
    #[case(&["default"], 1)]
    #[case(&[], 0)]
    fn word_count_checks(#[case] words: &[&str], #[case] expected_count: u32) {
        let mut t = Triers::new();
        for word in words {
            t.insert(word);
        }
        assert!(t.word_count() as u32 == expected_count);
    }

    #[rstest]
    #[case(vec!["hi".to_string(), "honey".to_string()], vec!["hi".to_string(), "honey".to_string()], true)]
    #[case(vec!["we love".to_string(), "python".to_string()], vec!["python".to_string()], false)]
    fn collect_word_checks(
        #[case] words: Vec<String>,
        #[case] expected_words: Vec<String>,
        #[case] expected: bool,
    ) {
        let mut t = Triers::new();
        for word in words {
            t.insert(&word);
        }
        let mut res: Vec<String> = t.collect_words();
        res.sort();
        assert_eq!(res == expected_words, expected);
    }
}

#[cfg(feature = "pyo3")]
use pyo3::prelude::*;

#[cfg(feature = "pyo3")]
#[pyclass]
pub struct Trie {
    inner: Triers,
}

#[cfg(feature = "pyo3")]
#[pymethods]
impl Trie {
    #[new]
    fn new() -> Self {
        Self {
            inner: Triers::new(),
        }
    }

    fn insert(&mut self, word: &str) {
        self.inner.insert(word);
    }

    fn search(&self, word: &str) -> bool {
        self.inner.search(word)
    }

    fn starts_with(&self, prefix: &str) -> bool {
        self.inner.starts_with(prefix)
    }

    fn delete(&mut self, word: &str) -> bool {
        self.inner.delete(word)
    }

    fn word_count(&self) -> usize {
        self.inner.word_count()
    }

    fn collect_words(&self) -> Vec<String> {
        self.inner.collect_words()
    }

    fn __contains__(&self, word: &str) -> bool {
        self.inner.search(word)
    }

    fn __len__(&self) -> usize {
        self.inner.word_count()
    }
}
