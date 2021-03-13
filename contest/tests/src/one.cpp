#include <iostream>
using namespace std;

int main(){
    int a, b;
    cin >> a >> b;
    if(a + b != 2){
        cout << a+b << endl;
    }else{
        cout << "Ooops!" << endl;
    }
    return 0;
}