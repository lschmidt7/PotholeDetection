import pickle

class Box():

    def __init__(self):
        self.box = [0,0,0,0]

    def update(self,xi,yi,xf,yf):
        if(xf<xi):
            self.box[0] = xf
            self.box[2] = xi-xf
        else:
            self.box[0] = xi
            self.box[2] = xf-xi
        if(yf<yi):
            self.box[1] = yf
            self.box[3] = yi-yf
        else:
            self.box[1] = yi
            self.box[3] = yf-yi
            
    def normalize(self):
        b = self.box
        self.box = [b[0],b[1],b[0]+b[2],b[1]+b[3]]
        return self.box

    def inside(self,x,y):
        if(x>self.box[0] and x<self.box[0]+self.box[2] and y>self.box[1] and y<self.box[1]+self.box[3]):
            return True
        return False

class Boxes():

    def __init__(self,n):
        self.boxes = []
        for x in range(n):
            self.boxes.append([])

    def add(self,i,box):
        self.boxes[i].append(box)

    def get(self,i):
        return self.boxes[i]

    def remove(self,i,x,y):
        index = 0
        index_remove = -1
        for b in self.boxes[i]:
            if(b.inside(x,y)):
                index_remove = index
            index+=1
        if(index_remove!=-1):
            del self.boxes[i][index_remove]     

    def save(self,filename):
        f = open(filename,'wb')
        pickle.dump(self.boxes,f,protocol=2)
        f.close()
    
    def load(self,filename):
        f = open(filename,'rb')
        self.boxes = pickle.load(f)
        f.close()
    
    def clearFrame(self,i):
        self.boxes[i] = []
    
    def clearAll(self):
        i=0
        for x in self.boxes:
            self.boxes[i] = []
            i+=1