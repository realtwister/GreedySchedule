import sys;
from collections import OrderedDict;

def printSchedule(due, error=False):
	print();
	print('\\begin{tabular}{r|'+'c'*(len(due))+'}');
	D='Day&';
	Du='Due day&';
	for i in range(len(due)):
		if(error and i==len(due)-1):
			D+='\\textbf{\\textcolor{red}{'+str(i+1)+'}}&';
			Du+='\\textbf{\\textcolor{red}{'+str(due[i])+'}}&';
		else:
			D+=str(i+1)+'&';
			Du+=str(due[i])+'&';
	print(D[:-1]+'\\\\ \\hline');
	print(Du[:-1]+'\\\\');
	print('\\end{tabular}');
	print();

#Check if schedule is independent
def isIndependent(schedule):
	#set day to 1
	n=1;
	
	due=[];
	#For every "earliest deadline"
	for i in sorted(schedule[:]):
		#If the deadline is smaller than the day we are on now
		due.append(i);
		if n>i:
			#This is not independent
			printSchedule(due,True);
			print('\\verb|There exists no feasible schedule and we neglect the task.|');
			return False;
		#Go to next day
		n+=1;
	#the whole schedule is independent
	printSchedule(due);
	print('\\verb|There exists a feasible schedule and we add the task to J.|');
	return True;

#Read the data
f = open('problem2cdata','r');
T = f.readline()[:-1].split(' ');
D = [int(d) for d in f.readline()[:-1].split(' ')];
R = [int(r) for r in f.readline()[:-1].split(' ')];
f.close();

#Parse data
data = {T[i]:(D[i],R[i])  for i  in range(len(T))};

#Order data by revenue
data = OrderedDict(sorted(data.items(), key=lambda t: t[1][1]));
dataDue = OrderedDict(sorted(data.items(), key=lambda t: t[1][0], reverse=True));

print("We first of all sort the input on revenue to simplify the execution of the greedy algorithm");
T='Task&';
R='Revenue&';
for it in reversed(data):
	T+=it+'&';
	R+=str(data[it][1])+'&';
print();
print('\\begin{tabular}{r|'+'c'*(len(data))+'}');
print(T[:-1]+'\\\\ \\hline');
print(R[:-1]+'\\\\');
print('\\end{tabular}');
print();
#Set datastructures
J = [];
schedule = [];

print('Now we invoke the greedy algorithm as described from page 274 of \\book.');
print();
print('\\verb|Initialization...|\\\\');
print('\\verb|J={}|');
print();
#Start algo[
i=1;
while data:
	print('\\verb|Iteration '+str(i)+':|\\\\');
	i+=1;
	# Take highest item (Structure:(key,value))
	it=data.popitem();
	print('\\verb|Considering task '+it[0]+'...|');
	
	#append to due day to schedule
	schedule.append(it[1][0]);
	
	#check if schedule is Independent
	if(not isIndependent(schedule)):
		#not independent: delete the due day from schedule and from result
		del dataDue[it[0]];
		del schedule[-1];
	else:
		J.append(it[0]);
	print('\\\\ \\verb|J = {'+', '.join(J)+'}.|');
	print();

#Print result
print();
print('In conclusion, by ordering the due dates in ascending order, we find an optimal schedule:');

print();
print('\\begin{tabular}{r|'+'c'*(len(dataDue)+1)+'}');
D='Day&';
T='Task&';
Du='Due day&';
R='Revenue&';
total=0;
for i in range(len(dataDue)):
	D+=str(i+1)+'&';
	it=dataDue.popitem();
	T+=str(it[0])+'&';
	Du+=str(it[1][0])+'&';
	R+=str(it[1][1])+'&';
	total+=it[1][1];
print(D[:-1]+'&\\textbf{total}\\\\ \\hline');
print(T[:-1]+'\\\\');
print(Du[:-1]+'\\\\');
print(R[:-1]+'&\\textbf{'+str(total)+'}\\\\');
print('\\end{tabular}');
print();
