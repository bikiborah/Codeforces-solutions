#include <iostream>
using namespace std;

int main()
{
    int t;
    cin >> t;

    while(t--){
        int x;
        cin >> x;

        int y;
        cin >> y;

        int R;
        cin >> R;

        int target = R * R;
        bool check = false;

        for(int i = -R; i <= R; i++){
            for(int j = -R; j <= R; j++){

                int u = x + i;
                int v = y + j;

                int a = x - u;
                int b = y - v;

                int c = a * a + b * b;

                if(c == target){
                    cout << u << " " << v << endl;
                    check = true;
                    break;
                }
            }

            if(check == true){
                break;
            }
        }
    }

    return 0;
}