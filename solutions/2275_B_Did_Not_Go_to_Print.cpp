#include <iostream>
#include <stack>
#include <vector>
using namespace std;

int main()
{
    int t;
    cin >> t;

    while(t--)
    {
        int n;
        cin >> n;

        string s;
        cin >> s;

        stack<int> st;

        vector<int> printed(n + 1, 0);

        for(int i = 0; i < n; i++)
        {
            if(s[i] == '1')
            {
                st.push(i + 1);
            }

            else if(s[i] == '2')
            {
                if(st.empty())
                {
                    printed[i + 1] = 1;
                }
                else
                {
                    int doc = st.top();
                    st.pop();

                    printed[doc] = 1;
                }
            }

            else if(s[i] == '3')
            {
                printed[i + 1] = 1;
            }
        }

        vector<int> notPrint;

        for(int i = 1; i <= n; i++)
        {
            if(printed[i] == 0)
            {
                notPrint.push_back(i);
            }
        }

        cout << notPrint.size() << endl;

        for(int i = 0; i < notPrint.size(); i++)
        {
            cout << notPrint[i] << " ";
        }

        cout << endl;
    }

    return 0;
}