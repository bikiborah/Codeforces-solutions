#include<bits/stdc++.h>
using namespace std;
int main()
{  

   int t;
   cin>>t;
   while(t--){
    int n,x;
    cin>>n>>x;
    int arr[n];
    for(int i = 0; i < n; i++){
        cin>>arr[i];
    }
    if(n == 0){
        cout<<x<<endl;
    }
    else{
        int Mx = 0;
        Mx = max(Mx,arr[0]);
        Mx = max(Mx,2*(x-arr[n-1]));

        for(int i = 1; i < n; i++){
            Mx = max(Mx,arr[i]-arr[i-1]);
        }

        cout<<Mx<<endl;


    }
   }
   return 0;
}