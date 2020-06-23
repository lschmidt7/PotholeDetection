from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import model_from_json

class Network():

    def __init__(self):
        self.model = None
        self.compile_config = None

    def read_compile_config_file(self,filename):
        self.compile_config = {}
        with open(filename) as f:
            for line in f:
                (key, val) = line.split(':')
                self.compile_config[key] = val.strip()

    def load(self,path,compile_config_filename,c,p,o):
        self.read_compile_config_file(path+compile_config_filename)
        json_file = open(path+'model_c_'+str(c)+'_p_'+str(p)+'_o_'+str(o)+'.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        self.model.load_weights(path+'model_c_'+str(c)+'_p_'+str(p)+'_o_'+str(o)+'.h5')
        self.model.compile(loss=self.compile_config['loss'], optimizer=self.compile_config['optimizer'], metrics=[self.compile_config['metrics']])
    
    def predict(self,x):
        return self.model.predict(x)