#include <iostream>
#include <unordered_map>
using namespace std;

int main()
{
    int t;
    cin >> t;

    while(t--)
    {
        int n;
        cin >> n;

        int nums[n];

        for(int i = 0; i < n; i++)
        {
            cin >> nums[i];
        }

        unordered_map<long long, long long> mp;

        long long cnt = 0;

        for(int i = 0; i + 4 < n; i++)
        {
            long long x = nums[i] + nums[i + 2] - nums[i + 4];

            // Number of previous triads having same value
            cnt += mp[x];

            // Remove previous triads which overlap with current triad
            if(i >= 2)
            {
                long long y = nums[i - 2] + nums[i] - nums[i + 2];

                if(y == x)
                {
                    cnt--;
                }
            }

            if(i >= 4)
            {
                long long y = nums[i - 4] + nums[i - 2] - nums[i];

                if(y == x)
                {
                    cnt--;
                }
            }

            mp[x]++;
        }

        cout << cnt << endl;
    }

    return 0;
}