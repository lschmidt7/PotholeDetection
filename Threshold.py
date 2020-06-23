import statistics

class Threshold():

    def __init__(self):
        pass
    
    def transform(self,signal,media):
        for i in range(len(signal)):
            s = signal[i]
            if(s<=media):
                s=0
            signal[i] = s
        return signal

    def media(self,signal):
        med = 0
        i=0
        for s in signal:
            if(s>0):
                med+=s
                i+=1
        return med/i

    def threshold_mean(self,data):
        thresh_value = self.media(data)
        indexes = []
        i=0
        for d in data:
            if(d>thresh_value):
                indexes.append(i)
            i+=1
        return indexes
    
    def threshold_median(self,data):
        thresh_value = statistics.median(data)
        indexes = []
        i=0
        for d in data:
            if(d>thresh_value):
                indexes.append(i)
            i+=1
        return indexes

    def threshold_deviation(self,data):
        thresh_value = statistics.stdev(data)
        indexes = []
        i=0
        for d in data:
            if(d>thresh_value):
                indexes.append(i)
            i+=1
        return indexes