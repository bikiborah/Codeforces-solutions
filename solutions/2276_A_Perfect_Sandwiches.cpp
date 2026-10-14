#include <iostream>
#include <algorithm>
using namespace std;

int main() {
    int t;
    cin >> t;

    while (t--) {
        int cnt = 0;
        int a, b;
        cin >> a >> b;

        if (a <= b) {
            cout << -1 << endl;
        } else {
            cnt = min(b, a - b);
            cout << cnt << endl;
        }
    }

    return 0;
}