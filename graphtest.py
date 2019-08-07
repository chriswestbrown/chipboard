
def generateGraph(a, weight, bias):
    graphString = ""
    layer={}
    i=1
    while i <= len(a):
        layer[i-1] = list(range(sum(a[0:i])-a[i-1], sum(a[0:i])))
        i = i+1

    graphString=" "
    x = 0;
    while(x < len(layer)):
        if x==0:
            graphString += "( i function " + str(i) + " " +  " [ ] " + weight[y-1] + " ) "
        else:
            for y in layer[x]: #for each node
                graphString+= "( m function " + str(i) + " " + bias[x][y-max(layer[x-1]) - 1] + " " + str(layer[y-1]).replace(",", " ").replace("[", "[ ").replace("]", " ] ")
                for i in layer[x-1]: #for each input of the node
                    if x==1:
                        graphString += str(weight[x-1][i][y]) + " "
                    else:
                        graphString += str(weight[x-1][i-max(layer[x-2])-1][y]) + " "
                graphString+=" ) "
        x+=1
    print(graphString)
