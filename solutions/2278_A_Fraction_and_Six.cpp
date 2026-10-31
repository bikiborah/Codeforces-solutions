
#include<bits/stdc++.h>
using namespace std;

void solve(int &n,int &m, string &p, string &q, unordered_map<char,int> &mpp){
    for(int i = 0; i < p.length(); i++){
        mpp[p[i]]++;
    }

    for(int i = 0; i < q.length(); i++){
        if(mpp.find(q[i]) != mpp.end() && mpp[q[i]] > 0){
            mpp[q[i]]--;

            if(mpp[q[i]] == 0){
                mpp.erase(q[i]);
            }
        }
        else{
            cout<<"NO"<<endl;
            return;
        }
    }

    if(mpp.size() == 3 &&
       mpp.find('s') != mpp.end() && mpp['s'] == 1 &&
       mpp.find('i') != mpp.end() && mpp['i'] == 1 &&
       mpp.find('x') != mpp.end() && mpp['x'] == 1){
        cout<<"YES"<<endl;
    }
    else{
        cout<<"NO"<<endl;
    }
}

int main()
{
    int t;
    cin>>t;

    while(t--){
        int n,m;
        cin>>n>>m;

        string p,q;
        cin>>p>>q;

        unordered_map<char,int> mpp;

        solve(n,m,p,q,mpp);
    }

    return 0;
}
