#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;

    int x;
    for (int i = 0; i < n; i++) {
        cin >> x;

        if (x == 1) {
            cout << "HARD";
            return 0;
        }
    }

    cout << "EASY";

    return 0;
}