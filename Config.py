from pickle import dump,load
from os.path import exists

class Config():

    def __init__(self):
        self.list_configurations = []
        self.video_names = []
        self.path = "data/results/"
        self.index = 0

    def add(self,alg,haralick_feature,sizew,sizeh,threads,threshold,hog_orientation,hog_cell_size,hog_block_size,resize_image):
        conf = [alg,haralick_feature,sizew,sizeh,threads,threshold,hog_orientation,hog_cell_size,hog_block_size,resize_image]
        if(not self.hasConf(conf)):
            self.list_configurations.append(conf)
        else:
            print("Configuracao ja existe")
            input()

    def hasConf(self,conf):
        for x in self.list_configurations:
            if(x==conf):
                return True
        return False

    def listConfigs(self):
        for c,v in zip(self.list_configurations,self.video_names):
            print(v)
            print("Haralick Feature: {}".format(c[0]))
            print("width: {}".format(c[1]))
            print("height: {}".format(c[2]))
            print("Threads: {}".format(c[3]))
            print("Threshold: {}".format(c[4]))
            print("Orientarions: {}".format(c[5]))
            print("Pixeis: {}".format(c[6]))
            print("Block: {}".format(c[7]))
            print("Resize: {}".format(c[8]))
            print("\n")

    def load(self):
        filename = self.path+"config-file.conf"
        if(exists(self.path+"config-file.conf")):
            config_file = open(filename,'rb')
            configs = load(config_file)
            self.list_configurations = configs[0]
            self.video_names = configs[1]
            self.index = len(self.video_names)
            config_file.close()

    def save(self):
        configs = (self.list_configurations,self.video_names)
        config_file = open(self.path+"config-file.conf",'wb')
        dump(configs,config_file)
        config_file.close()
