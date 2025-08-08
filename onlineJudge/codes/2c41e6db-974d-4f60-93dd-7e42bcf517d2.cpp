#include <bits/stdc++.h>
using namespace std;

static inline string trim(const string &s) {
    size_t a = s.find_first_not_of(" \t\r\n");
    if (a == string::npos) return "";
    size_t b = s.find_last_not_of(" \t\r\n");
    return s.substr(a, b - a + 1);
}

vector<char> parse_input_to_chars() {
    // Read whole stdin into a string
    std::ostringstream oss;
    oss << cin.rdbuf();
    string s = oss.str();
    s = trim(s);
    vector<char> res;
    if (s.empty()) return res;

    // If it looks like an array or contains quotes, parse quoted tokens first
    if (s.find('[') != string::npos || s.find('"') != string::npos || s.find('\'') != string::npos || s.find(',') != string::npos) {
        // Extract stuff inside quotes (handles ["h","e"] and ['h','e'])
        for (size_t i = 0; i < s.size(); ++i) {
            if (s[i] == '"' || s[i] == '\'') {
                char q = s[i];
                size_t j = i + 1;
                while (j < s.size() && s[j] != q) ++j;
                if (j >= s.size()) break;
                string token = s.substr(i + 1, j - (i + 1));
                // If token is empty it could be a space character: treat it as single space
                if (token.size() == 0) {
                    res.push_back(' ');
                } else {
                    // Most judge inputs have single-char tokens; if multi-char token found,
                    // push each character (safe fallback).
                    for (char c : token) res.push_back(c);
                }
                i = j;
            }
        }
        if (!res.empty()) return res;
        // If no quotes were found or parsing failed, try to parse comma-separated unquoted tokens: [h,a,n]
        {
            string token;
            for (size_t i = 0; i < s.size(); ++i) {
                char c = s[i];
                if (c == ',' || c == '[' || c == ']' || isspace((unsigned char)c)) {
                    if (!token.empty()) {
                        // token might be like h or "h", take first char
                        res.push_back(token[0]);
                        token.clear();
                    }
                } else {
                    token.push_back(c);
                }
            }
            if (!token.empty()) res.push_back(token[0]);
            if (!res.empty()) return res;
        }
    }

    // Fallback: whitespace-separated tokens (maybe "5 h e l l o" or "h e l l o")
    {
        istringstream iss(s);
        vector<string> toks;
        string t;
        while (iss >> t) toks.push_back(t);

        if (toks.empty()) return res;

        // If first token is an integer and matches count, skip it
        bool first_is_int = true;
        for (char c : toks[0]) if (!isdigit((unsigned char)c)) { first_is_int = false; break; }
        size_t start = 0;
        if (first_is_int) {
            // try to parse and ensure there are tokens following it
            try {
                int n = stoi(toks[0]);
                if ((size_t)n <= toks.size() - 1) start = 1;
            } catch (...) {
                start = 0;
            }
        }
        for (size_t i = start; i < toks.size(); ++i) {
            if (!toks[i].empty()) res.push_back(toks[i][0]);
        }
        return res;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<char> s = parse_input_to_chars();

    // Reverse in-place using two pointers (O(1) extra)
    int left = 0, right = (int)s.size() - 1;
    while (left < right) {
        swap(s[left], s[right]);
        ++left; --right;
    }

    // Print exactly like ["o","l","l","e","h"]
    cout << "[";
    for (size_t i = 0; i < s.size(); ++i) {
        cout << "\"" << s[i] << "\"";
        if (i + 1 != s.size()) cout << ",";
    }
    cout << "]";
    // newline (optional)
    cout << "\n";
    return 0;
}
