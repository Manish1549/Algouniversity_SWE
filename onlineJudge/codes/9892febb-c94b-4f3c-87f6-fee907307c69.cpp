// Write your C++ solution here
#include <bits/stdc++.h>
using namespace std;

// Function to reverse the string in-place
void reverseString(vector<char>& s) {
    int left = 0, right = s.size() - 1;
    while (left < right) {
        swap(s[left], s[right]);
        left++;
        right--;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n; // length of the string array

    vector<char> s(n);
    for (int i = 0; i < n; i++) {
        cin >> s[i];
    }

    reverseString(s);

    // Output in the same array form
    cout << "[";
    for (int i = 0; i < n; i++) {
        cout << "\"" << s[i] << "\"";
        if (i != n - 1) cout << ",";
    }
    cout << "]\n";

    return 0;
}
