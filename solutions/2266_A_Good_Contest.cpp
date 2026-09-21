#include<iostream>
using namespace std;
int main()
{
    int t;
    cin>>t;
    for(int i=0;i<t;i++){
      int n;
      cin>>n;

      int Max=0;

      int arr[3];
      for(int i=0;i<3;i++){
        cin>>arr[i];
        int x=n-arr[i];
        Max=max(x,Max);

      }
      cout<<Max;
      cout<<endl;
    }
   return 0;
}