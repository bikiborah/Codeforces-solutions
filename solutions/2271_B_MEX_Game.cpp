#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;

    while (t--) {
        int n, k;
        cin >> n >> k;

        vector<int> freq(n + 1, 0);

        for (int i = 0; i < n; i++) {
            int x;
            cin >> x;
            freq[x]++;
        }

        int mex = 0;

        while (mex <= n && freq[mex] >= 2 * k) {
            mex++;
        }

        cout << (freq[mex] == 2 * k - 1 ? "YES" : "NO") << '\n';
    }

    return 0;
}