#include<iostream>
using namespace std;
int marco(){

    
   int n;
   cin>>n;

   int arr[n];
   for(int i=0;i<n;i++){
    cin>>arr[i];
   }

   int cnt=0;




   if(arr[0]==0 && arr[n-1]==0){
    return 0;
   }




   else if(arr[0]==0 && arr[n-1]==1){
    for(int i=n-2;i>=1;i--){
        if(arr[i]==0){
            swap(arr[n-1],arr[i]);
            cnt++;
            break;
        }
    }
    if(cnt==0){
        return -1;
    }
    else{
      return cnt;
    }
   }




   else if(arr[0]==1 && arr[n-1]==0){
    for(int i=1;i<n-1;i++){
        if(arr[i]==0){
            swap(arr[i],arr[0]);
            cnt++;
            break;
        }
    }
     if(cnt==0){
        return -1;
    }
    else{
      return cnt;
    }
   }




   else if(arr[0]==1 && arr[n-1]==1){
       for(int i=1;i<n-1;i++){
        if(arr[i]==0){
            swap(arr[i],arr[0]);
            cnt++;
            break;
        }    
    }

       for(int i=n-2;i>=1;i--){
        if(arr[i]==0){
            swap(arr[n-1],arr[i]);
            cnt++;
            break;
        }
    }
if(arr[0]==0 && arr[n-1]==0){
     if(cnt==0){
        return -1;
    }
    else{
      return cnt;
    }
}

else{
    return -1;
}
}


}


int main()
{  
   int t;
   cin>>t;



   for(int i=0;i<t;i++){

   int ans=marco();
   cout<<ans;
   cout<<endl;

}

   return 0;
}