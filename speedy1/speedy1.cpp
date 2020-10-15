#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <vector>
#include <stack>
#include <string.h>
#include <stdio.h>
#include <sstream>
#include <time.h>

using namespace std;

string its1(int a)
{
	stringstream ss;
	ss << a;
	return ss.str();
}

char *strtoglob1(string a)
{
	char *ret1=new char[a.length()+1];
	ret1[a.length()]=0;
	memcpy(ret1,&a[0],a.length());
	return ret1;
}

int sti1(string a)
{
	stringstream ss(a);
	int num1;
	ss >> num1;
	return num1;
}

int fileL1(string a)
{
	FILE *fp1 = NULL;
	fp1=fopen(a.c_str(),"rb");
	fseek(fp1,0,SEEK_END);
	int ret1 = ftell(fp1);
	fclose(fp1);
	return ret1;
}

vector<string> split1(string a,char b)
{
	vector<string> ret1;
	a+=b;
	int li1=0;
	for(int i=0;i<a.length();i++)
		if(a[i]==b)
		{
			ret1.push_back(a.substr(li1,i-li1));
			li1=i+1;
		}
	return ret1;
}

char *readfile1(string fname1)
{
	ifstream ffp1(fname1.c_str(),ifstream::binary);
	int l1=fileL1(fname1);
	char *ar1=new char[l1+1];
	ar1[l1]=0;
	ffp1.read(ar1,l1);
	ffp1.close();
	return ar1;
}

string replace1(string a,string b,string c)
{
	string ret1="";
	for(int i=0;i<=a.length()-b.length();i++)
	{
		for(int i1=0;i1<b.length();i1++)
			if(b[i1]!=a[i+i1])
				goto skp1;
		ret1+=c;
		i+=b.length()-1;
		continue;
		skp1:
		ret1+=a[i];
	}
	return ret1;
}

float mod1(float a,float b)
{
	return a-(float)((int)(a/b))*b;
}

struct liter1
{
	int cmd1=0;
	int* data1=0;
};

struct data1
{
	int type1;
	int *data1;
	data1(){}
	data1(int a,int *b):type1(a),data1(b){}
};

struct pair1
{
	int num1;
	string name1;
};

int iof1(string a,string *b,int c)
{
	for(int i=0;i<c;i++)
		if(a==b[i])
			return i;
	return -1;
}

vector<string> toargs1(string a)
{
	vector<string> ret1;
	string cr1="";
	int open1=0;
	bool instr1=false;
	for(int i=1;i<a.length()-1;i++)
	{
		char cc1=a[i];
		if(cc1=='{')
			open1++;
		else if(cc1=='}')
			open1--;
		else if(cc1=='\'')
			instr1=!instr1;
		else if(cc1==',' && open1==0)
		{
			ret1.push_back(cr1);
			cr1="";
			continue;
		}
		cr1+=cc1;
	}
	ret1.push_back(cr1);
	return ret1;
}

vector<pair1> funcs1;
vector<pair1> vars1;
vector< vector<string> > types1;

const int intfuncc1=40;
string intfunc1[]={"output","input",">","+","-","=","array","skip","strtoint","length","[g]","set","[s]","system","call","clone","push_back","s+","*","/","%","!=","&","|","^","!",">=","<","<=","remove","substr","inttostr","read","insert","indexof","rev-set","tochar","inttofloat","floattoint","random"};

short isnum1(string a)
{
	short ret1=0;
	for(int i=0;i<a.length();i++)
	{
		if(a[i]>='0' && a[i]<='9')
			ret1|=1;
		else if(a[i]=='-')
			ret1|=2;
		else if(a[i]=='.')
			ret1|=4;
		else
		{
			ret1=0;
			break;
		}
	}
	return ret1;
}

liter1 lfromstr1(string a,string b)
{
	liter1 ret1;
	ret1.cmd1=-1;
	int fnd1;
	int rev1=0;
	short numbr1=isnum1(a);
	if(a[0]=='@' || ((numbr1&5)==5))
	{
		ret1.cmd1=3;
		stringstream ss(a.substr(a[0]=='@' ? 1:0));
		float num1;
		ss >> num1;
		ret1.data1=*(int*)&num1;
	}
	else if(a[0]=='$' || (numbr1&1))
	{
		ret1.cmd1=2;
		stringstream ss(a.substr(a[0]=='$' ? 1:0));
		int num1;
		ss >> num1;
		ret1.data1=num1;
	}
	else if(a[0]=='\'')
	{
		ret1.cmd1=4;
		a=a.substr(1,a.length()-2);
		char *ar1=&a[0];
		char *ar2=malloc(a.length()+1);
		memcpy(ar2,ar1,a.length());
		ar2[a.length()]=0;
		ret1.data1=(int*)ar2;
	}
	else if(a[0]=='{')
	{
		vector<string> params1=toargs1(a);
		ret1.cmd1=5;
		vector<data1> *arr1=new vector<data1>(params1.size());
		ret1.data1=(int*)arr1;
		for(int i=0;i<params1.size();i++)
		{
			liter1 nl1=lfromstr1(params1[i],b);
			(*arr1)[i]=data1(nl1.cmd1,nl1.data1);
		}
	}
	else if(a=="true" || a=="false")
	{
		ret1.cmd1=8;
		int n1=a=="true" ? 1:0;
		ret1.data1=*(int*)&(n1);
	}
	else if(a[0]=='+' && a.length()>1)
	{
		for(int i=0;i<funcs1.size();i++)
			if(funcs1[i].name1==a.substr(1))
			{
				ret1.cmd1=10;
				ret1.data1=funcs1[i].num1;
				goto rt1;
			}
	}
	else for(int i=0;i<intfuncc1;i++)
	if(intfunc1[i]==a)
	{
		ret1.cmd1=1;
		ret1.data1=-i-1;
		goto rt1;
	}
	for(int i=0;i<funcs1.size();i++)
	if(funcs1[i].name1==a)
	{
		ret1.cmd1=1;
		ret1.data1=funcs1[i].num1;
		goto rt1;
	}
	for(int i=0;i<types1.size();i++)
	if(types1[i][1]==a)
	{
		ret1.cmd1=6;
		ret1.data1=types1[i].size()-2;
		goto rt1;
	}
	for(int i=0;i<vars1.size();i++)
	if(vars1[i].name1==b+"+"+a)
	{
		ret1.cmd1=0;
		ret1.data1=i;
		goto rt1;
	}
	for(int i=0;i<vars1.size();i++)
	if(vars1[i].name1=="+"+a)
	{
		ret1.cmd1=0;
		ret1.data1=i;
		goto rt1;
	}
	fnd1=a.find(".");
	if(fnd1!=-1)
	{
		if(a[0]=='-')
		{
			fnd1--;
			a=a.substr(1);
			rev1=1;
		}
	for(int i=0;i<types1.size();i++)
	if(types1[i][1]==a.substr(0,fnd1))
	{
		ret1.cmd1=9;
		bool f1=false;
		for(int i1=2;i1<types1[i].size();i1++)
			if(types1[i][i1]==a.substr(fnd1+1))
			{
				ret1.data1=i1-2;
				if(rev1)
					ret1.data1=0-(int)ret1.data1;
				f1=true;
				break;
			}
		if(!f1)
			ret1.cmd1=-1;
		goto rt1;
	}
	}
	rt1:
	return ret1;
}

int getend1(vector< vector<string> > a,int b,int c)
{
	int d1=c;
	for(int i=b;i>-1 && i<a.size();i+=c)
	{
		if(a[i][0]=="func" || a[i][0]=="loop" || a[i][0]=="if" || a[i][0]=="for")
			d1++;
		else if(a[i][0]=="end")
			d1--;
		if(d1==0)
			return i;
	}
	return -1;
}

vector< vector<liter1> > getcode1(vector< vector<string> > a)
{
	vector< vector<liter1> > ret1;
	string fname1="";
	for(int i=0;i<a.size();i++)
	{
		vector<string> cur1=a[i];
		if(cur1[0]=="func")
		{
			funcs1.push_back({i,cur1[1]});
			fname1=cur1[1];
			//vars1.push_back({vars1.size(),fname1+"+ret"});
			for(int i1=2;i1<cur1.size();i1++)
				vars1.push_back({vars1.size(),fname1+"+"+cur1[i1]});
		}
		else if(cur1[0]=="var")
			vars1.push_back({vars1.size(),fname1+"+"+cur1[1]});
		else if(cur1[0]=="type")
			types1.push_back(cur1);
	}
	/*for(int i=0;i<funcs1.size();i++)
		cout<<funcs1[i].num1<<" "<<funcs1[i].name1<<endl;
	for(int i=0;i<vars1.size();i++)
		cout<<vars1[i].num1<<" "<<vars1[i].name1<<endl;*/
	fname1="";
	stack<int> calls1;
	for(int i=0;i<a.size();i++)
	{
		vector<string> cur1=a[i];
		vector<liter1> new1;
		if(cur1[0]=="func" || cur1[0]=="loop" || cur1[0]=="if" || cur1[0]=="for")
		{
			if(cur1[0]=="func")
				fname1=cur1[1];
			calls1.push(i);
		}
		int cmd1;
		if(cur1[0]=="`" || cur1[0]=="var")
		{
			if(cur1[0]=="var")
				cur1.push_back("set");
			cmd1=3;
			new1.push_back(*(liter1*)&cmd1);
			for(int i1=1;i1<cur1.size();i1++)
				new1.push_back(lfromstr1(cur1[i1],fname1));
			ret1.push_back(new1);
		}
		else if(cur1[0]=="func")
		{
			cmd1=10;
			new1.push_back(*(liter1*)&cmd1);
			for(int i1=cur1.size()-1;i1>1;i1--)
				new1.push_back(lfromstr1(cur1[i1],fname1));
			ret1.push_back(new1);
		}
		else if(cur1[0]=="pop")
		{
			cmd1=10;
			new1.push_back(*(liter1*)&cmd1);
			for(int i1=1;i1<cur1.size();i1++)
				new1.push_back(lfromstr1(cur1[i1],fname1));
			ret1.push_back(new1);
		}
		else if(cur1[0]=="loop" || cur1[0]==":" || cur1[0]=="")
		{
			cmd1=-1;
			new1.push_back(*(liter1*)&cmd1);
			ret1.push_back(new1);
		}
		else if(cur1[0]=="goto")
		{
			cmd1=6;
			new1.push_back(*(liter1*)&cmd1);
			liter1 nl1;
			nl1.cmd1=7;
			for(int i1=0;i1<a.size();i1++)
				if(a[i1][0]==":" && a[i1][1]==cur1[1])
				{
					nl1.data1=i1;
					break;
				}
			new1.push_back(nl1);
			ret1.push_back(new1);
		}
		else if(cur1[0]=="while")
		{
			cmd1=1;
			new1.push_back(*(liter1*)&cmd1);
			liter1 nl1;
			nl1.cmd1=7;
			nl1.data1=(int)getend1(a,i,1)+1;
			new1.push_back(nl1);
			for(int i1=1;i1<cur1.size();i1++)
				new1.push_back(lfromstr1(cur1[i1],fname1));
			ret1.push_back(new1);
		}
		else if(cur1[0]=="for")
		{
			cmd1=13;
			new1.push_back(*(liter1*)&cmd1);
			liter1 nl1;
			nl1.cmd1=7;
			nl1.data1=(int)getend1(a,i+1,1)+1;
			new1.push_back(nl1);
			for(int i1=1;i1<4;i1++)
				new1.push_back(lfromstr1(cur1[i1],fname1));
			ret1.push_back(new1);
		}
		else if(cur1[0]=="end" || cur1[0]=="continue")
		{
			if(a[calls1.top()][0]=="if")
			{
				cmd1=-1;
				new1.push_back(*(liter1*)&cmd1);
			}
			else if(a[calls1.top()][0]=="func")
			{
				cmd1=12;
				new1.push_back(*(liter1*)&cmd1);
			}
			else if(a[calls1.top()][0]=="loop" || a[calls1.top()][0]=="for")
			{
				cmd1=6;
				new1.push_back(*(liter1*)&cmd1);
				liter1 nl1;
				nl1.cmd1=7;
				nl1.data1=(int)calls1.top();
				new1.push_back(nl1);
			}
			ret1.push_back(new1);
			if(cur1[0]=="end")
			{
				calls1.pop();
				if(calls1.size()==0)
					fname1="";
			}
		}
		else if(cur1[0]=="else" || cur1[0]=="break" || cur1[0]=="exit")
		{
			cmd1=6;
			new1.push_back(*(liter1*)&cmd1);
			liter1 nl1;
			nl1.cmd1=7;
			nl1.data1=(int)getend1(a,i,1)+(cur1[0]=="exit" ? 0:1);
			new1.push_back(nl1);
			ret1.push_back(new1);
			if(cur1[0]=="else")
				ret1[calls1.top()][1].data1=(int)ret1.size();
		}
		else if(cur1[0]=="push")
		{
			cmd1=9;
			new1.push_back(*(liter1*)&cmd1);
			for(int i1=1;i1<cur1.size();i1++)
				new1.push_back(lfromstr1(cur1[i1],fname1));
			ret1.push_back(new1);
		}
		else if(cur1[0]=="if")
		{
			cmd1=8;
			new1.push_back(*(liter1*)&cmd1);
			liter1 nl1;
			nl1.cmd1=7;
			nl1.data1=(int)42424242;
			new1.push_back(nl1);
			for(int i1=1;i1<cur1.size();i1++)
				new1.push_back(lfromstr1(cur1[i1],fname1));
			ret1.push_back(new1);
		}
		else if(cur1[0]=="type")
		{
			cmd1=4;
			new1.push_back(*(liter1*)&cmd1);
			liter1 nl1;
			nl1.cmd1=7;
			nl1.data1=(int)cur1.size()-2;
			new1.push_back(nl1);
			ret1.push_back(new1);
		}
		else
		{
			cmd1=-2;
			new1.push_back(*(liter1*)&cmd1);
			ret1.push_back(new1);
		}
	}
	return ret1;
}

string ltostr1(liter1 a)
{
	//string ret1="";
	//char *i1=new char[30];
	//itoa((int)a.data1,i1,10);
	return its1((int)a.data1);
	/*switch(a.cmd1)
	{
		case 1:
		if((int)a.data1<0)
			ret1+=intfunc1[-(int)a.data1-1];
		else
			ret1+=funcs1[(int)a.data1].name1;
		break;
	}
	return ret1;*/
}

string compilerror1(vector< vector<liter1> > code1)
{
	string ret1="";
	for(int i=0;i<code1.size();i++)
	{
		if(*(int*)&code1[i][0]==-2)
		{
			ret1=its1(i+1)+";unsupported command";
			break;
		}
		for(int i1=1;i1<code1[i].size();i1++)
			if(code1[i][i1].cmd1==-1)
			{
				
				ret1=its1(i+1)+":"+its1(i1+1)+";unsupported argument";
				goto stp1;
			}
	}
	stp1:
	return ret1;
}

struct stckpair1
{
	int line1;
	int arg1;
	stckpair1(){}
	stckpair1(int a,int b):line1(a),arg1(b){}
};

data1 str2d1(string a)
{
	return data1(4,(int*)a.c_str());
}

stack<stckpair1> rets1;
stack<data1> stck1;
data1 *glob1;

void intfuncs1(int a)
{
	switch(a)
	{
		case 12: //set
		{
			data1 from1=stck1.top();
			stck1.pop();
			data1 to1=stck1.top();
			stck1.pop();
			if(from1.type1==0)
				from1=*(data1*)from1.data1;
			*(data1*)to1.data1=from1;
			break;
		}
		case 1: //output
		{
			data1 out1=stck1.top();
			stck1.pop();
			if(out1.type1==0)
				out1=*(data1*)out1.data1;
			switch(out1.type1)
			{
				case 2: cout<<(int)out1.data1<<endl; break;
				case 3: cout<<*(float*)&out1.data1<<endl; break;
				case 4: cout<<(char*)out1.data1<<endl; break;
				case 8: cout<<((char)out1.data1==0 ? "false":"true")<<endl; break;
				default:
					cout<<"*unprintable_type*"<<endl;
			}
			break;
		}
		case 2: //input
		{
			string s1;
			cin>>s1;
			stck1.push(data1(4,(int*)(&s1[0])));
			break;
		}
		case 3: //>
		{
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			if(op1.type1>op2.type1)
			{
				data1 t1=op1;
				op1=op2;
				op2=t1;
			}
			if(op1.type1==2 && op2.type1==2)
				stck1.push(data1(8,(int*)((int)op1.data1>(int)op2.data1)));
			else if(op1.type1==3 && op2.type1==3)
				stck1.push(data1(8,(int*)(*(float*)&op1.data1>*(float*)&op2.data1)));
			else if(op1.type1==2 && op2.type1==3)
				stck1.push(data1(8,(int*)((int)op1.data1>*(float*)&op2.data1)));
			break;
		}
		case 4: //+
		{
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			if(op1.type1>op2.type1)
			{
				data1 t1=op1;
				op1=op2;
				op2=t1;
			}
			if(op1.type1==2 && op2.type1==2)
				stck1.push(data1(2,(int*)((int)op1.data1+(int)op2.data1)));
			else if(op1.type1==3 && op2.type1==3)
			{
				float cf1=(*(float*)&op1.data1+*(float*)&op2.data1);
				stck1.push(data1(3,*(int*)&cf1));
			}
			else if(op1.type1==2 && op2.type1==3)
			{
				float cf1=((int)op1.data1+*(float*)&op2.data1);
				stck1.push(data1(3,*(int*)&cf1));
			}
			break;
		}
		case 5: //-
		{
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			if(op1.type1>op2.type1)
			{
				data1 t1=op1;
				op1=op2;
				op2=t1;
			}
			if(op1.type1==2 && op2.type1==2)
				stck1.push(data1(2,(int*)((int)op1.data1-(int)op2.data1)));
			else if(op1.type1==3 && op2.type1==3)
			{
				float cf1=(*(float*)&op1.data1-*(float*)&op2.data1);
				stck1.push(data1(3,*(int*)&cf1));
			}
			else if(op1.type1==2 && op2.type1==3)
			{
				float cf1=((int)op1.data1-*(float*)&op2.data1);
				stck1.push(data1(3,*(int*)&cf1));
			}
			break;
		}
		case 6: //=
		{
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			if(op1.type1>op2.type1)
			{
				data1 t1=op1;
				op1=op2;
				op2=t1;
			}
			if(op1.type1==2 && op2.type1==2)
				stck1.push(data1(8,(int*)((int)op1.data1==(int)op2.data1)));
			else if(op1.type1==3 && op2.type1==3)
				stck1.push(data1(8,(int*)(*(float*)&op1.data1==*(float*)&op2.data1)));
			else if(op1.type1==2 && op2.type1==3)
				stck1.push(data1(8,(int*)((int)op1.data1==*(float*)&op2.data1)));
			else if(op1.type1==4 && op2.type1==4)
			{
				string s1=string((char*)op1.data1);
				string s2=string((char*)op2.data1);
				stck1.push(data1(8,(int*)(s1.compare(s2)==0 ? 1:0)));
			}
			break;
		}
		case 7: //array
		{
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			vector<data1> *arr1=new vector<data1>((int)op1.data1);
			stck1.push(data1(5,(int*)arr1));
			break;
		}
		case 8: //skip
		{
			stck1.pop();
			break;
		}
		case 9: //strtoint
		{
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			string s1=(char*)op1.data1;
			stck1.push(data1(2,sti1(s1)));
			break;
		}
		case 10: //length
		{
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			if(op1.type1==4)
				stck1.push(data1(2,string((char*)op1.data1).length()));
			else if(op1.type1==5)
				stck1.push(data1(2,(*(vector<data1>*)op1.data1).size()));
			break;
		}
		case 11: //[g]
		{
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			if(op1.type1==5)
				stck1.push((*(vector<data1>*)op1.data1)[(int)op2.data1]);
			else
			{
				string ar1=(char*)op1.data1;
				char cc1=ar1.substr((int)op2.data1,1)[0];
				char *s1=calloc(2,1);
				s1[0]=cc1;
				stck1.push(data1(4,(int*)s1));
			}
			break;
		}
		case 13: //[s]
		{
			data1 op3=stck1.top();
			stck1.pop();
			if(op3.type1==0) op3=*(data1*)op3.data1;
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			if(op1.type1==5)
				(*(vector<data1>*)op1.data1)[(int)op2.data1]=op3;
			else
			{
				char *ar1=(char*)op1.data1;
				ar1[(int)op2.data1]=(char)op3.data1;
			}
			break;
		}
		case 14: //system
		{
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			string s1=(char*)op1.data1;
			system(s1.c_str());
			break;
		}
		case 16: //clone
		{
			data1 old1=stck1.top();
			stck1.pop();
			if(old1.type1==0) old1=*(data1*)old1.data1;
			if(old1.type1==4)
			{
				data1 nw1=*(data1*)malloc(sizeof(data1));
				nw1.type1=4;
				string s1=string((char*)old1.data1);
				char *n1=new char[s1.length()+1];
				n1[s1.length()]=0;
				memcpy(n1,&s1[0],s1.length());
				nw1.data1=(int*)n1;
				stck1.push(nw1);
				break;
			}
			if(old1.type1!=5)
			{
				data1 nw1=*(data1*)malloc(sizeof(data1));
				nw1.type1=old1.type1;
				nw1.data1=old1.data1;
				stck1.push(nw1);
				break;
			}
			vector<data1> arr0=*(vector<data1>*)old1.data1;
			vector<data1> *arr1=new vector<data1>(arr0.size());
			data1 new1=data1(5,(int*)arr1);
			for(int i=0;i<(*arr1).size();i++)
				(*arr1)[i]=arr0[i];
			stck1.push(new1);
			break;
		}
		case 17: //push_back
		{
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			(*(vector<data1>*)op1.data1).push_back(op2);
			break;
		}
		case 18: //s+
		{
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			char *cf1=strtoglob1(((string)(char*)op1.data1)+((string)(char*)op2.data1));
			stck1.push(data1(4,(int*)cf1));
			break;
		}
		case 19: //*
		{
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			if(op1.type1>op2.type1)
			{
				data1 t1=op1;
				op1=op2;
				op2=t1;
			}
			if(op1.type1==2 && op2.type1==2)
				stck1.push(data1(2,(int*)((int)op1.data1 * (int)op2.data1)));
			else if(op1.type1==3 && op2.type1==3)
			{
				float cf1=(*(float*)&op1.data1 * *(float*)&op2.data1);
				stck1.push(data1(3,*(int*)&cf1));
			}
			else if(op1.type1==2 && op2.type1==3)
			{
				float cf1=((int)op1.data1 * *(float*)&op2.data1);
				stck1.push(data1(3,*(int*)&cf1));
			}
			break;
		}
		case 20: ///
		{
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			if(op1.type1>op2.type1)
			{
				data1 t1=op1;
				op1=op2;
				op2=t1;
			}
			if(op1.type1==2 && op2.type1==2)
				stck1.push(data1(2,(int*)((int)op1.data1 / (int)op2.data1)));
			else if(op1.type1==3 && op2.type1==3)
			{
				float cf1=(*(float*)&op1.data1 / *(float*)&op2.data1);
				stck1.push(data1(3,*(int*)&cf1));
			}
			else if(op1.type1==2 && op2.type1==3)
			{
				float cf1=((int)op1.data1 / *(float*)&op2.data1);
				stck1.push(data1(3,*(int*)&cf1));
			}
			break;
		}
		case 21: //%
		{
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			if(op1.type1>op2.type1)
			{
				data1 t1=op1;
				op1=op2;
				op2=t1;
			}
			if(op1.type1==2 && op2.type1==2)
				stck1.push(data1(2,(int*)((int)op1.data1%(int)op2.data1)));
			else if(op1.type1==3 && op2.type1==3)
			{
				float cf1=mod1(*(float*)&op1.data1,*(float*)&op2.data1);
				stck1.push(data1(3,*(int*)&cf1));
			}
			else if(op1.type1==2 && op2.type1==3)
			{
				float cf1=mod1((int)op1.data1,*(float*)&op2.data1);
				stck1.push(data1(3,*(int*)&cf1));
			}
			break;
		}
		case 22: //!=
		{
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			if(op1.type1>op2.type1)
			{
				data1 t1=op1;
				op1=op2;
				op2=t1;
			}
			if(op1.type1==2 && op2.type1==2)
				stck1.push(data1(8,(int*)((int)op1.data1!=(int)op2.data1)));
			else if(op1.type1==3 && op2.type1==3)
				stck1.push(data1(8,(int*)(*(float*)&op1.data1!=*(float*)&op2.data1)));
			else if(op1.type1==2 && op2.type1==3)
				stck1.push(data1(8,(int*)((int)op1.data1!=*(float*)&op2.data1)));
			else if(op1.type1==4 && op2.type1==4)
			{
				string s1=string((char*)op1.data1);
				string s2=string((char*)op2.data1);
				stck1.push(data1(8,(int*)(s1.compare(s2)!=0 ? 1:0)));
			}
			break;
		}
		case 23: //&
		{
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			stck1.push(data1(2,(int*)((int)op1.data1 & (int)op2.data1)));
			break;
		}
		case 24: //|
		{
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			stck1.push(data1(2,(int*)((int)op1.data1 | (int)op2.data1)));
			break;
		}
		case 25: //^
		{
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			stck1.push(data1(2,(int*)((int)op1.data1 ^ (int)op2.data1)));
			break;
		}
		case 26: //!
		{
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			stck1.push(data1(2,(int*)(~(int)op1.data1)));
			break;
		}
		case 27: //>=
		{
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			if(op1.type1>op2.type1)
			{
				data1 t1=op1;
				op1=op2;
				op2=t1;
			}
			if(op1.type1==2 && op2.type1==2)
				stck1.push(data1(8,(int*)((int)op1.data1>=(int)op2.data1)));
			else if(op1.type1==3 && op2.type1==3)
				stck1.push(data1(8,(int*)(*(float*)&op1.data1>=*(float*)&op2.data1)));
			else if(op1.type1==2 && op2.type1==3)
				stck1.push(data1(8,(int*)((int)op1.data1>=*(float*)&op2.data1)));
			break;
		}
		case 28: //<
		{
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			if(op1.type1>op2.type1)
			{
				data1 t1=op1;
				op1=op2;
				op2=t1;
			}
			if(op1.type1==2 && op2.type1==2)
				stck1.push(data1(8,(int*)((int)op1.data1<(int)op2.data1)));
			else if(op1.type1==3 && op2.type1==3)
				stck1.push(data1(8,(int*)(*(float*)&op1.data1<*(float*)&op2.data1)));
			else if(op1.type1==2 && op2.type1==3)
				stck1.push(data1(8,(int*)((int)op1.data1<*(float*)&op2.data1)));
			break;
		}
		case 29: //<=
		{
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			if(op1.type1>op2.type1)
			{
				data1 t1=op1;
				op1=op2;
				op2=t1;
			}
			if(op1.type1==2 && op2.type1==2)
				stck1.push(data1(8,(int*)((int)op1.data1<=(int)op2.data1)));
			else if(op1.type1==3 && op2.type1==3)
				stck1.push(data1(8,(int*)(*(float*)&op1.data1<=*(float*)&op2.data1)));
			else if(op1.type1==2 && op2.type1==3)
				stck1.push(data1(8,(int*)((int)op1.data1<=*(float*)&op2.data1)));
			break;
		}
		case 30: //remove
		{
			data1 op3=stck1.top();
			stck1.pop();
			if(op3.type1==0) op3=*(data1*)op3.data1;
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			vector<data1> *vct1=((vector<data1>*)op1.data1);
			(*vct1).erase((*vct1).begin()+(int)op2.data1,(*vct1).begin()+(int)op3.data1);
			break;
		}
		case 31: //substr
		{
			data1 op3=stck1.top();
			stck1.pop();
			if(op3.type1==0) op3=*(data1*)op3.data1;
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			string ar1=(char*)op1.data1;
			char *str1=calloc(op3.data1+1,1);
			char *s1=ar1.substr((int)op2.data1,(int)op3.data1).c_str();
			memcpy(str1,s1,(int)op3.data1+1);
			stck1.push(data1(4,(int*)s1));
			break;
		}
		case 32: //inttostr
		{
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			int s1=(int)op1.data1;
			stck1.push(data1(4,(int*)its1(s1).c_str()));
			break;
		}
		case 33: //read
		{
			stck1.top()=*(data1*)stck1.top().data1;
			break;
		}
		case 34: //insert
		{
			data1 op3=stck1.top();
			stck1.pop();
			if(op3.type1==0) op3=*(data1*)op3.data1;
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			vector<data1> vct1=(*(vector<data1>*)op1.data1);
			vct1.insert(vct1.begin()+(int)op3.data1,op2);
			break;
		}
		case 35: //indexof
		{
			data1 op2=stck1.top();
			stck1.pop();
			if(op2.type1==0) op2=*(data1*)op2.data1;
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
				stck1.push(data1(2,string((char*)op1.data1).find(string((char*)op2.data1))));
			break;
		}
		case 36: //rev-set
		{
			data1 to1=stck1.top();
			stck1.pop();
			data1 from1=stck1.top();
			stck1.pop();
			if(from1.type1==0)
				from1=*(data1*)from1.data1;
			*(data1*)to1.data1=from1;
			break;
		}
		case 37: //tochar
		{
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			string ar1=(char*)op1.data1;
			stck1.push(data1(2,(int)(ar1[0])));
		}
		case 38: //inttofloat
		{
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			float r1=(float)((int)op1.data1);
			stck1.push(data1(3,*(int*)&r1));
			break;
		}
		case 39: //floattoint
		{
			data1 op1=stck1.top();
			stck1.pop();
			if(op1.type1==0) op1=*(data1*)op1.data1;
			float r1=*(float*)&op1.data1;
			stck1.push(data1(2,(int*)(int)r1));
			break;
		}
		case 40: //random
		{
			stck1.push(data1(2,rand()));
			break;
		}
	}
}

void runvm1(vector< vector<liter1> > code1,vector<string> args)
{
	srand(time(0));
	int entryp1=-1;
	int varc1=0;
	for(int i=0;i<code1.size();i++)
	{
		int ct1=code1[i][0].cmd1;
		if(entryp1==-1 && ct1==10)
			entryp1=i;
		if(ct1==3)
			for(int i1=1;i1<code1[i].size();i1++)
				if(code1[i][i1].cmd1==0)
					varc1=max(varc1,(int)code1[i][i1].data1+1);
	}
	glob1=new data1[varc1];
	rets1.push(stckpair1(0,0));
	vector<data1> argv1;
	for(int i=0;i<args.size();i++)
		argv1.push_back(str2d1(args[i]));
	stck1.push(data1(5,(int*)&argv1));
	// ret cont
	while(rets1.size())
	{
		stckpair1 work1=rets1.top();
		bool nextinst1=true;
		vector<liter1> cr1=code1[work1.line1];
		int lc1=(int)cr1[0].cmd1;
		// lang command
		switch(lc1)
		{
			case 1: //while
			case 3: //set
			case 8: //if
			{
				int fr1=(work1.arg1==0 ? (lc1==3 ? 1:2):work1.arg1);
				for(int i=fr1;i<cr1.size();i++)
				{
					liter1 clit1=cr1[i];
					// argument proc
					switch(clit1.cmd1)
					{
						case 0: //var
						{
							stck1.push(data1(0,(int*)&glob1[(int)clit1.data1]));
							break;
						}
						case 2: //int
						case 3: //float
						case 8: //bool
						case 10: //function as argument
						case 5: //array
						{
							stck1.push(data1(clit1.cmd1,clit1.data1));
							break;
						}
						case 4: //string
						{
							char *old1=(char*)clit1.data1;
							int l1=((string)old1).length();
							char *new1=malloc(l1+1);
							memcpy(new1,old1,l1);
							new1[l1]=0;
							stck1.push(data1(4,(int*)new1));
							break;
						}
						case 9: //array offset
						{
							//cout<<stck1.top().type1<<endl;
							//if(stck1.top().type1==0)
								//stck1.top()=*(data1*)stck1.top().data1;
							//cout<<stck1.top().data1<<" "<<(int)clit1.data1<<endl;
							stck1.top()=*(data1*)stck1.top().data1;
							//stck1.top()=((data1*)stck1.top().data1)[(int)clit1.data1];
							//cout<<stck1.top().type1<<endl;
							stck1.top().data1+=((int)clit1.data1)*sizeof(data1);
							break;
						}
						case 6: //record
						{
							data1 *rar1=malloc((int)clit1.data1*sizeof(data1));
							//for(int i3=0;i3<(int)clit1.data1;i3++)
								//rar1[i3].type1=2;
							stck1.push(data1(6,(int*)rar1));
							break;
						}
						case 1: //function
						{
							int fnc1=(int)clit1.data1;
							if(fnc1==-15) //callback
							{
								nextinst1=false;
								rets1.top().arg1=i+1;
								data1 out1=stck1.top();
								stck1.pop();
								if(out1.type1==0)
									out1=*(data1*)out1.data1;
								work1.line1=(int)out1.data1;
								rets1.push(work1);
								goto nextiter1;
							}
							else if(fnc1<0)
								intfuncs1(-fnc1);
							else
							{
								nextinst1=false;
								rets1.top().arg1=i+1;
								work1.line1=(int)clit1.data1;
								rets1.push(work1);
								goto nextiter1;
							}
							break;
						}
					}
				}
				if(lc1!=3 && (int)stck1.top().data1==0)
				{
					nextinst1=false;
					work1.line1=(int)cr1[1].data1;
					rets1.top()=work1;
					stck1.pop();
				}
				break;
			}
			case 6: //jump
				nextinst1=false;
				work1.line1=(int)cr1[1].data1;
				rets1.top()=work1;
				break;
			case 12: //func exit
				nextinst1=false;
				rets1.pop();
				break;
			case 9: //push
			{
				for(int i=1;i<cr1.size();i++)
				{
					data1 cpy1=glob1[(int)cr1[i].data1];
					stck1.push(cpy1);
				}
				break;
			}
			case 10: //pop
			{
				for(int i=1;i<cr1.size();i++)
				{
					data1 cdt1=stck1.top();
					while(cdt1.type1==0) cdt1=*(data1*)cdt1.data1;
					glob1[(int)cr1[i].data1]=cdt1;
					stck1.pop();
				}
				break;
			}
			case 13: //for
			{
				data1 *var1=&(glob1[(int)cr1[2].data1]);
				data1 var2=glob1[(int)cr1[3].data1];
				if(var2.type1==0) var2=*(data1*)var2.data1;
				int step1=cr1[4].data1;
				int cr2=(int)((*var1).data1);
				cr2+=step1;
				((*var1).data1)=(int*)cr2;
				if((step1>0 && (*var1).data1>var2.data1) || (step1<0 && (*var1).data1<var2.data1))
				{
					nextinst1=false;
					work1.line1=(int)cr1[1].data1;
					rets1.top()=work1;
				}
				break;
			}
		}
		nextiter1:
		if(nextinst1)
		{
			work1.line1++;
			work1.arg1=0;
			rets1.top()=work1;
		}
	}
}

inline void settop1(int *a,int b)
{
	//stack<int> st1;
	//for(int i=1;i<=100;i++)
	//st1.push(i);
	//cout<<st1.top()<<endl; - 100
	//settop1((int*)&st1,42);
	//cout<<st1.top()<<endl; - 42
	*((int*)*(a+4)+((*(a+12)-*(a+4))>>2)-1)=b;
}

int main(int argc, char *argv[])
{
	/*vector<liter1> cmds1;
	glob1=new data1[10];
	string s1="hello";
	int car1[]={-1,-1,0,1,2,5,2,10,1,-4,1,-12};
	for(int i=0;i<sizeof(car1)/4;i+=2)
	{
		liter1 nl1;
		nl1.cmd1=car1[i];
		nl1.data1=(int)car1[i+1];
		cmds1.push_back(nl1);
	}
	stack<data1> rt1=chain1(cmds1);
	while(rt1.size())
	{
		//string ns1=(char*)(rt1.top().data1);
				//cout<<ns1<<endl;
		cout<<rt1.top().type1<<" "<<(int)rt1.top().data1<<endl;
		rt1.pop();
	}
	system("pause");*/
	if(argc==1)
	{
		cout<<"no input file"<<endl;
		return 2;
	}
	char *ar1=readfile1(string(argv[1]));
	if(string(ar1).length()==3)
	{
		cout<<"empty file"<<endl;
		//system("pause");
		return 2;
	}
	vector<string> strs1=split1(replace1(ar1,"\r",""),'\n');
	for(int i=strs1.size()-1;i>=0;i--)
	{
		string cs1=strs1[i];
		while(cs1.length()>0 && (cs1[0]==' ' || cs1[0]=='\t'))
			cs1=cs1.substr(1);
		if(cs1.length()==0 || cs1[0]=='#')
			strs1[i]="";
			//strs1.erase(strs1.begin()+i);
	}
	vector< vector<string> > sar1;
	for(int i=0;i<strs1.size();i++)
	{
		string cs1=strs1[i]+' ';
		vector<string> vec1;
		string as1="";
		bool instr1=false;
		for(int i1=0;i1<cs1.length();i1++)
		{
			if(cs1[i1]=='\'')
				instr1=!instr1;
			if(cs1[i1]==' ' && !instr1)
			{
				vec1.push_back(as1);
				as1="";
			}
			else
				as1+=cs1[i1];
		}
		sar1.push_back(vec1);
	}
	vector< vector<liter1> > code1=getcode1(sar1);
	/*for(int i=0;i<code1.size();i++)
	{
		cout<<*(int*)&code1[i][0];
		for(int i1=1;i1<code1[i].size();i1++)
			cout<<" "<<code1[i][i1].cmd1<<","<<ltostr1(code1[i][i1]);
		cout<<endl;
	}
	cout<<"----------"<<endl;*/
	vector<string> arg1;
	for(int i=2;i<argc;i++)
		arg1.push_back(argv[i]);
	string error1=compilerror1(code1);
	if(error1!="")
	{
		cerr<<error1<<endl;
		return 1;
	}
	runvm1(code1,arg1);
	exit1:
	//system("pause");
	return 0;
}

