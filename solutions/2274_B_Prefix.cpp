#include <bits/stdc++.h>
using namespace std;

int main() {
    int t;
    cin >> t;

    while (t--) {
        int n;
        cin >> n;

        vector<long long> arr(n);

        for (int i = 0; i < n; i++) {
            cin >> arr[i];
        }

        long long mn = arr[0];
        long long mx = arr[0];
        long long ans = arr[0];

        for (int i = 1; i < n; i++) {
            long long a = arr[i];

            ans = max({ans, a - mn, a, a + mx});

            long long newMn = min({a, a + mn, a + 2 * mn});
            long long newMx = max({a, a + mx, a + 2 * mx});

            mn = newMn;
            mx = newMx;
        }

        cout << ans << '\n';
    }

    return 0;
}