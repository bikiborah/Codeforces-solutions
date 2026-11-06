#include <bits/stdc++.h>
using namespace std;

int solve(string arr, int n) {
    int cnt = 0;
    int Mx = 0;
    int x = 0;

    for(int i = 0; i < n; i++){
        if(arr[i] == '.'){
            x++;
            cnt++;
            Mx = max(Mx,cnt);
        }
        else{
            cnt = 0;
        }
    }

    if(Mx >= 3) return 2;
    return x;
}

int main() {
    int t;
    cin >> t;

    while (t--) {
        int n;
        cin >> n;

        string arr;
        cin >> arr;

        cout << solve(arr,n) << endl;
    }
    return 0;
}