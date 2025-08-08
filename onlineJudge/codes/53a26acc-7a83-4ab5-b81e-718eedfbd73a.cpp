//write your solution
#include <iostream>
#include <sstream>
using namespace std;

int main() {
    string input;
    getline(cin, input); // Read entire line like "5,6"

    stringstream ss(input);
    string a_str, b_str;

    // Split on comma
    getline(ss, a_str, ',');
    getline(ss, b_str);

    // Convert to integers
    int a = stoi(a_str);
    int b = stoi(b_str);

    cout << a + b << endl;

    return 0;
}
