import math
dict={}
ineq=[]
ineq_arr=[]
n=2
#Reading from the file
filename="C:\\Users\\HP\\Desktop\\a.txt"
#"C:\\Users\\HP\\Desktop\\a.txt" is the location of the testbench
fo=open(filename,"r")
dict['OUTPUT']=[]
dict['DFF']=[]
dict['ASSIGNMENT']=[]
dict['ASSIGNMENT']=['SUPER_INPUT','SUPER_OUTPUT']
dict['SUPER_INPUT']=['INPUT',0]
dict['SUPER_OUTPUT']=['OUTPUT',0]
line=fo.readline()
#Making nodes in dictionary
#edge_MatrixnewG contains the edge weights ogf G'
#edge_Matrix contains the edge weights ogf G
while(line):
    if ("INPUT" in line):
        dict[line[line.index('(')+1:line.index(')')]]=[]
        dict[line[line.index('(')+1:line.index(')')]].append('INPUT')
        dict[line[line.index('(')+1:line.index(')')]].append(0)
        n+=1
        dict['ASSIGNMENT'].append(line[line.index('(')+1:line.index(')')])
    elif ("OUTPUT" in line):
        dict['OUTPUT'].append(line[line.index('(')+1:line.index(')')])
    elif("DFF" in line):
        arr=[]
        arr.append(line[0:line.index(' ')])
        arr.append(line[line.index('(')+1:line.index(')')])
        dict['DFF'].append(arr)
    elif ("=" in line ):
        dict[line[0:line.index(' ')]]=[]
        dict[line[0:line.index(' ')]].append(line[line.index('=')+2:line.index('(')])
        if ("DFF" in line):
            dict[line[0:line.index(' ')]].append(0)
        else:
            dict[line[0:line.index(' ')]].append(1)
        n+=1    
        dict['ASSIGNMENT'].append(line[0:line.index(' ')])      
    line=fo.readline()
tmax=1
M=n*tmax
fo.close()
edge_MatrixnewG = [[float('inf') for x in range(n)] for y in range(n)]
edge_Matrix=[[float('inf') for x in range(n)] for y in range(n)]
fo=open(filename,"r")
for i in range (0,4):
    line=fo.readline()
inv_count=line[2]
line=fo.readline()
str_gates=line
line=fo.readline()
while(line):
    if ("INPUT" in line):
        dict['SUPER_INPUT'].append(line[line.index('(')+1:line.index(')')])
        dict['SUPER_INPUT'].append((M*0-dict['SUPER_INPUT'][1]))
        edge_MatrixnewG[0][dict['ASSIGNMENT'].index(line[line.index('(')+1:line.index(')')])]=M*0-dict['SUPER_INPUT'][1]
        edge_Matrix[0][dict['ASSIGNMENT'].index(line[line.index('(')+1:line.index(')')])]=0
        #ineq.append([0,dict['ASSIGNMENT'].index(line[line.index('(')+1:line.index(')')]),0])
    elif ("NOT" in line):
        flag=-1
        for k in range(0,len(dict['DFF'])):
            if (line[line.index('(')+1:line.index(')')]==dict['DFF'][k][0]):
                flag=k
        if(flag==-1):
            dict[line[line.index('(')+1:line.index(')')]].append(line[0:line.index(' ')])
            dict[line[line.index('(')+1:line.index(')')]].append((M*0-dict[line[line.index('(')+1:line.index(')')]][1]))
            edge_MatrixnewG[dict['ASSIGNMENT'].index(line[line.index('(')+1:line.index(')')])][dict['ASSIGNMENT'].index(line[0:line.index(' ')])]=(M*0-dict[line[line.index('(')+1:line.index(')')]][1])
            edge_Matrix[dict['ASSIGNMENT'].index(line[line.index('(')+1:line.index(')')])][dict['ASSIGNMENT'].index(line[0:line.index(' ')])]=0
            #ineq.append([dict['ASSIGNMENT'].index(line[line.index('(')+1:line.index(')')]),dict['ASSIGNMENT'].index(line[0:line.index(' ')]),0])           
        elif(flag!=-1):
            count=1
            temp=dict['DFF'][flag][1]
            while (temp not in dict):
                count+=1
                for l in range(0,len(dict['DFF'])):
                    if(dict['DFF'][l][0]==temp):
                        break
                temp=dict['DFF'][l][1]
            dict[temp].append(line[0:line.index(' ')])
            dict[temp].append((M*1-dict[temp][1]))
            edge_MatrixnewG[dict['ASSIGNMENT'].index(temp)][dict['ASSIGNMENT'].index(line[0:line.index(' ')])]=(M*count-dict[temp][1])
            edge_Matrix[dict['ASSIGNMENT'].index(temp)][dict['ASSIGNMENT'].index(line[0:line.index(' ')])]=count
            #ineq.append([dict['ASSIGNMENT'].index(temp),dict['ASSIGNMENT'].index(line[0:line.index(' ')]),1])
    elif ("= OR" in line or "= AND" in line or "NOR" in line or "NAND" in line ):
        arr=[]
        temp=line[line.index('(')+1:line.index(')')]
        arr=temp.split(', ')
        for j in range(0,len(arr)):
            flag=-1
            for k in range(0,len(dict['DFF'])):
                if (arr[j]==dict['DFF'][k][0]):
                    flag=k
            if(flag==-1):
                dict[arr[j]].append(line[0:line.index(' ')])
                dict[arr[j]].append((M*0-dict[arr[j]][1]))
                edge_MatrixnewG[dict['ASSIGNMENT'].index(arr[j])][dict['ASSIGNMENT'].index(line[0:line.index(' ')])]=(M*0-dict[arr[j]][1])
                #ineq.append([dict['ASSIGNMENT'].index(arr[j]),dict['ASSIGNMENT'].index(line[0:line.index(' ')]),0])
            elif(flag!=-1):
                count=1
                temp=dict['DFF'][flag][1]
                while (temp not in dict):
                    count+=1
                    for l in range(0,len(dict['DFF'])):
                        if(dict['DFF'][l][0]==temp):
                            break
                    temp=dict['DFF'][l][1]
                dict[temp].append(line[0:line.index(' ')])
                dict[temp].append((M*1-dict[temp][1]))
                edge_MatrixnewG[dict['ASSIGNMENT'].index(temp)][dict['ASSIGNMENT'].index(line[0:line.index(' ')])]=(M*count-dict[temp][1])
                edge_Matrix[dict['ASSIGNMENT'].index(temp)][dict['ASSIGNMENT'].index(line[0:line.index(' ')])]=count
    line=fo.readline()  
fo.close()
for i in range(0,len(dict['OUTPUT'])):
    dict[dict['OUTPUT'][i]].append('SUPER_OUTPUT')
    dict[dict['OUTPUT'][i]].append((M*0-dict[dict['OUTPUT'][i]][1]))
    edge_MatrixnewG[dict['ASSIGNMENT'].index(dict['OUTPUT'][i])][1]=M*0-dict[dict['OUTPUT'][i]][1]
for i in range(0,n):
    edge_MatrixnewG[i][i]=0
#edge_MatrixnewG[1][0]=0
for i in range(0,n):
    edge_Matrix[i][i]=0
#edge_Matrix[1][0]=0


#for i in range(0,len(edge_MatrixnewG[0])):
    #print edge_MatrixnewG[i]
######################################################
#Now implementing all-pairs shortest paths   
matrix=edge_MatrixnewG
for k in range(0,n):
    temp_Matrix1=matrix
    temp_Matrix2 = [[float('inf') for x in range(n)] for y in range(n)]
    for i in range(0,n):
        for j in range(0,n):
            temp_Matrix2[i][j]=min(temp_Matrix1[i][j],(temp_Matrix1[i][k]+temp_Matrix1[k][j]))
    matrix=temp_Matrix2
#######################################################
#print 'shoretst path matrix & n is',n
#for i in range(0,len(matrix[0])):
    #print matrix[i]   
#print matrix

###########################################
#Now calculating W
W_matrix=[[0 for x in range(n)] for y in range(n)]
D_matrix=[[0 for x in range(n)] for y in range(n)]
for k in range(0,n):
    for j in range(0,n):
        if(k==j):
            W_matrix[k][j]=0
        else:
            W_matrix[k][j]=math.ceil(matrix[k][j]/M)
for k in range(0,n):
    for j in range(0,n):
        if(k==j):
            D_matrix[k][j]=dict[dict['ASSIGNMENT'][k]][1]
        else:
            D_matrix[k][j]=(M*W_matrix[k][j])-matrix[k][j]+dict[dict['ASSIGNMENT'][j]][1]     
for keys,values in dict.items():
    print(keys),
    print(' = '),
    print(values)
#print edge_Matrix            

#for i in range(0,len(matrix[0])):
    #print matrix[i]
#################################################            
#let the value of c be 0
c=1          
for i in range(0,n):
    for j in range(0,n):
        if(D_matrix[i][j]>c or edge_Matrix[i][j]!=float('inf')):
            if(dict['ASSIGNMENT'][i] not in ineq_arr):
                ineq_arr.append(dict['ASSIGNMENT'][i])
            if(dict['ASSIGNMENT'][j] not in ineq_arr):
                ineq_arr.append(dict['ASSIGNMENT'][j])
            if(D_matrix[i][j]>c and edge_Matrix[i][j]==float('inf')):
                ineq.append([ineq_arr.index(dict['ASSIGNMENT'][i]),ineq_arr.index(dict['ASSIGNMENT'][j]),(W_matrix[i][j]-1)])   
            if(D_matrix[i][j]<=c and edge_Matrix[i][j]!=float('inf')):
                ineq.append([ineq_arr.index(dict['ASSIGNMENT'][i]),ineq_arr.index(dict['ASSIGNMENT'][j]),edge_Matrix[i][j]])
            if(D_matrix[i][j]>c and edge_Matrix[i][j]!=float('inf')):
                ineq.append([ineq_arr.index(dict['ASSIGNMENT'][i]),ineq_arr.index(dict['ASSIGNMENT'][j]),min(edge_Matrix[i][j],(W_matrix[i][j]-1))])

ineq_arr.append('extra_node')
#ineq holds the inequalities
#N is the number of nodes in the new graph(constraint graph) made for solving inequalities including the extra node
#ineq_arr holds the nodes of the graph
#ineq_matrix holds the edge weights
N=len(ineq_arr)
ineq_matrix=[[float('inf') for x in range(N)] for y in range(N)]
for i in range(0,len(ineq)):
    ineq_matrix[ineq[i][1]][ineq[i][0]]=ineq[i][2]
for i in range(0,N-1):
    ineq_matrix[N-1][i]=0
#Now check whether negative weight cycles exist in this graph(constraint graph) or not.
#If no negative weight cycles then solution exists
    
#Now solving the inequalities
#Applying Bellman-Ford to find the shortest paths if no negative weight cycles exist.
#darray holds the shortest paths and hence darray holds the solution of the inequalities
darray=[float('inf') for x in range(N)]
darray[N-1]=0
flag=0

#BELLMAN-FORD
for i in range(0,N-1):
    for j in range(0,N):
        for k in range(0,N):
            if(ineq_matrix[j][k]!=float('inf')):
                if(darray[k]>darray[j]+ineq_matrix[j][k]):
                    darray[k]=darray[j]+ineq_matrix[j][k]
for j in range(0,N):
    for k in range(0,N):
        if(ineq_matrix[j][k]!=float('inf') and darray[k]>darray[j]+ineq_matrix[j][k]):
            flag=1
#for i in range(0,len(ineq_matrix[0])):
    #print ineq_matrix[i]
if(flag==1):
    print 'For the given value of c no solution exists'
if(flag==0):
    print 'Solution exists for given c'
############################################################################################################
#######Now applying retiming

#retimed_edge_weights contains new retimed edge weights
retimed_edge_weights=[[float('inf') for x in range(n)] for y in range(n)]
for i in range(0,n):
    for j in range(0,n):
        if(edge_Matrix[i][j]!=float('inf')):
            retimed_edge_weights[i][j]=edge_Matrix[i][j]+darray[ineq_arr.index(dict['ASSIGNMENT'][j])]-darray[ineq_arr.index(dict['ASSIGNMENT'][i])]


#for i in range(0,len(retimed_edge_weights[0])):
    #print retimed_edge_weights[i]
###########################################################################################################            
visited=[0 for x in range(n)]
ct=0
p=0
#####function to compute maximum computation time
def path(s,d):
    global p
    global visited
    global ct
    visited[s]=1
    ct+=dict[dict['ASSIGNMENT'][s]][1]
    if (s==d):
        if(ct>p):
            p=ct
        ct=0    
    else:
        for i in range (0,n):
            if (visited[i] == 0 and edge_Matrix[s][i]!=float('inf')):
                path(i,d)
    visited[s]=0
#####  
'''
maxp=0

for j in range(0,len(dict['DFF'])):
    if(dict['DFF'][j][1] in dict):
        for k in range(0,len(dict['DFF'])):
            if(dict['DFF'][k][1] in dict and k!=j):
                ct=0
                p=0
                path(dict['ASSIGNMENT'].index('SUPER_INPUT'),dict['ASSIGNMENT'].index(dict['DFF'][j][1]))
                print 'p is ',p
                if(p>maxp):
                    maxp=p
        ct=0
        p=0
        path(dict['ASSIGNMENT'].index('SUPER_INPUT'),dict['ASSIGNMENT'].index(dict['DFF'][j][1]))
        print 'p is ',p
        if(p>maxp):
            maxp=p
        ct=0
        p=0
        path(dict['ASSIGNMENT'].index(dict['DFF'][j][1]),dict['ASSIGNMENT'].index('SUPER_OUTPUT'))
        print 'p is ',p
        if(p>maxp):
            maxp=p


#print maxp
'''
####Writing in another file
filename="C:\\Users\\HP\\Desktop\\b.txt"
fo=open(filename,"w")
a=(len(dict['SUPER_INPUT'])-2)/2
b=len(dict['OUTPUT'])
fo.write ('# ')
fo.write(str((len(dict['SUPER_INPUT'])-2)/2))
fo.write(" inputs\n# ")
fo.write(str(len(dict['OUTPUT'])))
fo.write(' outputs\n# ')
#fo.write('dffs')
fo.write(' D-type flipflops\n# ')
fo.write(str(inv_count))
fo.write(' inverters\n')
fo.write(str_gates)
fo.write('\n')
for i in range(2,len(dict['SUPER_INPUT']),2):
    fo.write('INPUT(')
    fo.write(str(dict['SUPER_INPUT'][i]))
    fo.write(')\n')
fo.write('\n')
for i in range(0,len(dict['OUTPUT'])):
    fo.write('OUTPUT(')
    fo.write(str(dict['OUTPUT'][i]))
    fo.write(')\n')
fo.write('\n')

dff_remove=[]
dff_add=[]
newdffcount=0
for i in range(0,n):
    for i in range(0,n):
        if(retimed_edge_weights[i][j]<edge_Matrix[i][j]):
            temp=edge_Matrix[i][j]-retimed_edge_weights[i][j]
            a=dict['ASSIGNMENT'][i]
            for k in range(0,temp):
                for l in range(0,len(dict['DFF'])):
                    if(a==dict['DFF'][l][1]):
                        dff_remove.append(dict['DFF'][l][0])
                        a=dict['DFF'][l][0]
                        break
        elif(retimed_edge_weights[i][j]>edge_Matrix[i][j]):
            temp=retimed_edge_weights[i][j]-edge_Matrix[i][j]
            a=dict['ASSIGNMENT'][i]
            for k in range(0,temp):
                dff_name='new_dff'+str(newdffcount)
                newdffcount+=1
                dff_add.append([dff_name,a])
                a=dff_name
            for l in range(0,len(dict['DFF'])):
                if(dict['ASSIGNMENT'][i]==dict['DFF'][l][1]):
                    dff_remove.append(dict['DFF'][l][0])
                    dff_add.append([dict['DFF'][l][0],a])
                    break
fo.close()




    
    
