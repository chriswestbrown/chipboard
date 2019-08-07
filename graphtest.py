
def generateGraph(a):
    graphString = ""
    layer={}
    i=1
    while i <= len(a):
        layer[i-1] = list(range(sum(a[0:i])-a[i-1], sum(a[0:i])))
        i = i+1

    y=0
    while y<len(layer):
        for i in layer[y]:
            if y==0:
                graphString += ("(i:function:" + str(i) + ":" +  str(y) + ":" + str(i) + ":[])")
            else:
                graphString += ("(m:function:" + str(i) + ":" + str(y) + ":" + str(i-layer[y-1][-1]-1) + ":" + str(layer[y-1]) + ")")
        y+=1

    print(graphString)
