from config import config
import csv
import os
import json 
from pprint import pprint
from itertools import chain, combinations
from tabulate import tabulate

class LoadMaster:

    CONFIG_FILE = 'config_final_normalize.json'
    

    def read_configs_from_file(self):
        data = {'configs':[]} 
        if not os.path.exists(ConfigCreator.CONFIG_FILE):
            exportfile = open(ConfigCreator.CONFIG_FILE, 'x')
            exportfile.close() 
            return data

        with open(ConfigCreator.CONFIG_FILE, 'r') as reader:
            data = json.load(reader)
        return data 

    def config_as_dict(self):
        dictionary = {}
        for key, value in config.__dict__.items(): 
            if not key.startswith('_'):
                dictionary[key] = value 
        return dictionary
    

class ConfigLoader(LoadMaster):
    

    def __init__(self, patient_groups, filename=LoadMaster.CONFIG_FILE):
        ConfigLoader.CONFIG_FILE = filename 
        LoadMaster.CONFIG_FILE = filename 
        self.counter = 1
        self.patient_groups = patient_groups

        self.configs = self.read_configs_from_file()['configs']
        print('Read [{count}] configs from file [{file}]'.format(count=len(self.configs), file=ConfigLoader.CONFIG_FILE))
        self.current_config = None
        self.column_of_interest = []
        self.table = []
        self.evaluations = []

    def next_config(self): 
        # Popping old one from the list, retreiving first value 

        # TODO: Op basis van wijzigingen tabel printen!!!! 
        if self.current_config:
            self.configs.pop(0) 
        if self.configs:
            self.current_config = self.configs[0] 
            for key, value in self.current_config.items():
                oldvalue = getattr(config, key)
                if oldvalue != value:
                    if key not in self.column_of_interest:
                        self.column_of_interest.append(key)


                    print('change detected: {key} has new value [{value}]'.format(key=key, value=value))
                    setattr(config, key, value) 
                     
        else:
            self.counter += 1
            return False
        
        self.counter += 1
        return True 
    
    def update_table(self, score):
        
        self.table.append([score, self.current_config])
        #self.print_table() 
        self.export_evaluation()
        with open('C:\\Users\\lennart\Desktop\\results\\{}\\config{}'.format(self.counter, self.counter),'w') as output:
            json.dump([score, self.current_config], output, indent= 4)
        return self.counter
    
    def clear_evaluation_result(self):
        if os.path.exists("eval_result.json"):
            with open("eval_result.json", "w+") as f:
                f.write(json.dumps([]))
        else:
            with open("eval_result.json", "w+") as f:
                f.write(json.dumps([]))

    def export_evaluation(self):
        with open("eval_result.json", "w") as f:
            f.write(json.dumps(self.table, indent= 2))        
            

    def print_table(self):
        if 'columns' in self.column_of_interest:
            self.column_of_interest.remove('columns')
        temp_table = []
        for record in self.table:
            score, config = record
            temp_table.append([score['Accuracy'],score['MCC'], score['LogLoss'],score['RMSE'],score['RMSLE'], *[config[key] for key in self.column_of_interest]])
        sorted_scores = list(sorted(temp_table, key=lambda x: x[0]))
        print(tabulate(sorted_scores, headers=['Accuracy', 'MCC', 'LogLoss', 'RSME', 'RMSLE',  *self.column_of_interest]))

    def update_exercises(self):
        for patientgroup in self.patient_groups:
            for patient in patientgroup.patients:
                for exercise in patient.exercises:
                    exercise.update_config()
        
    
class ConfigCreator(LoadMaster):
    
    def __init__(self):
        self.reset_config() 
        self.new_configs = self.read_configs_from_file() 
         

    def append_config(self):
        self.new_configs['configs'].append(self.config_as_dict())

    def model_evaluation(self):
        framecount = [5, 10, 15, 20]
        framecount_resample = [20, 50, 100, 150]

        self.reset_config() 
        config.remove_idle = True

        for frame in framecount:
            config.frames_counts = frame
            self.append_config()
        
        self.reset_config() 
        config.resample_exercise = True
        for frame in framecount_resample:
            config.frames_counts = frame
            self.append_config()

        self.reset_config() 
        config.frame_generator = True 
        for frame in framecount:
            config.frames_counts = frame
            self.append_config()

        self.reset_config()
        config.occupied_space = True 

        spacesize = [10, 36, 120, 360]
        for space in spacesize:
            config.binsize = space
            self.append_config()

        self.reset_config() 
        self.export_configs()


    def export_configs(self):  
        configs = self.new_configs
        print('Writing [{count}] configs to {file}'.format(count=len(configs['configs']), file=ConfigCreator.CONFIG_FILE))
        with open(ConfigCreator.CONFIG_FILE, 'w') as writer:
            writer.write(json.dumps(configs))

    def powerset(self, iterable):
        s = list(iterable)  # allows duplicate elements
        return chain.from_iterable(combinations(s, r) for r in range(len(s)+1)) 
        
    def test_generator(self):
        exercisegroups = ['AF', 'EL', 'AB', 'RF', 'EH']
        exercise_combinations = list(self.powerset(exercisegroups))

        for conbination in exercise_combinations[1:]:
            config.exercisegroups = conbination
            config.exercise_count = len(conbination)
            self.append_config()

        self.export_configs(self.new_configs)

    def reset_config(self):
        config.remove_idle = False
        config.resample_exercise = False 
        config.frame_generator = False 
        config.occupied_space = False 
        config.default = False 

        config.remove_idle_split_count = 3
        config.frames_counts = 5
        config.exercisegroups = ['AF', 'EL', 'AB', 'RF', 'EH']
        config.exercise_count = 5

        config.columns = config.columns_backup
        config.column_index = -1

    def resample_exercises(self):
        self.reset_config() 

        config.resample_exercise = True
        remove_idle = [True, False]
        framecount = [5, 10, 25, 100, 200] 
        normalize = [True, False] 

        for normal in normalize:
            for col in range(2):
                for idle in remove_idle:
                    for f in framecount:
                        config.frames_counts = f 
                        config.remove_idle = idle 
                        config.columns = self.column_combinations(col)
                        config.column_index = col
                        config.normalise = normal
                        self.append_config()  

    def create_default_config(self):
        self.reset_config()
        self.append_config()

        self.export_configs()

    def generate_more_frames(self):
        config.resample_exercise = False
        config.frame_generator = True 
        config.occupied_space = False 

        remove_idle = [True, False]
        frame_count = [5, 10, 15] 
        frame_generator_count = [3, 5, 7]

        columns = range(2)
        normalize = [True, False] 

        for normal in normalize:
            for gen in frame_generator_count:
                for idle in remove_idle:
                    for frame in frame_count: 
                        for col in columns:
                            config.remove_idle = idle
                            config.frames_counts = frame 
                            config.columns = self.column_combinations(col)
                            config.column_index = col
                            config.normalise = normal
                            config.frame_generator_count = gen
                            self.append_config()

    def occupied_space(self):
        config.remove_idle = False
        config.resample_exercise = False 
        config.frame_generator = False 
        config.occupied_space = True 
        config.default = False 

        binsize = [5, 10, 25, 36, 72, 152, 3]
        columns = range(2) 

        for bins in binsize:
            for col in columns:
                config.binsize = bins 
                config.column_index = col
                self.append_config()

    def remove_idle(self):
        config.remove_idle = False
        config.resample_exercise = False 
        config.frame_generator = False 
        config.occupied_space = False 
        config.default = False 

        frame_count = [5, 15, 25]
        split_count = [3, 5]
        columns = range(2) 
        config.resample_exercise = False
        normalize = [True, False] 

        for normal in normalize:
            for frame in frame_count:
                for split in split_count:
                    for col in columns:
                        config.frames_counts = frame
                        config.remove_idle_split_count = split 
                        config.columns = self.column_combinations(col)
                        config.column_index = col
                        config.normalise = normal
                        self.append_config()
        config.resample_exercise = True
        for normal in normalize:
            for frame in frame_count:
                for split in split_count:
                    for col in columns:
                        config.frames_counts = frame
                        config.remove_idle_split_count = split 
                        config.columns = self.column_combinations(col)
                        config.column_index = col
                        config.normalise = normal
                        self.append_config()

    def orignal_five_frames(self):
        config.remove_idle = False
        config.resample_exercise = False 
        config.frame_generator = False 
        config.occupied_space = False 
        config.default = True
        
        frame_count = [5, 15, 25] 
        remove_idle = [True, False]
        columns = range(2)
        normalize = [True, False] 

        for normal in normalize:
            for idle in remove_idle:
                for frame in frame_count: 
                    for col in columns:
                        config.remove_idle = idle
                        config.frames_counts = frame 
                        config.columns = self.column_combinations(col)
                        config.column_index = col
                        config.normalise = normal
                        self.append_config()



    def create_configurations(self):
        self.generate_more_frames() 
        # self.occupied_space() 
        self.remove_idle() 
        self.orignal_five_frames() 
        self.resample_exercises() 

        self.export_configs()

    def column_combinations(self, index):  
        column_combinations = [ 
            # (('thorax_r_x_ext', 'thorax_r_y_ax', 'thorax_r_z_lat'), ('humerus_r_y_plane', 'humerus_r_z_ele', 'humerus_r_y_ax'), ('humerus_l_y_plane', 'humerus_l_z_ele', 'humerus_l_y_ax')),
            #                     (('scapula_r_y_pro', 'scapula_r_z_lat', 'scapula_r_x_tilt'), ('humerus_r_y_plane', 'humerus_r_z_ele', 'humerus_r_y_ax'), ('clavicula_l_y_pro', 'clavicula_l_z_ele', 'clavicula_l_x_ax')),
            #                     (('humerus_r_y_plane', 'humerus_r_z_ele', 'humerus_r_y_ax'), ('thorax_l_x_ext', 'thorax_l_y_ax', 'thorax_l_z_lat'), ('humerus_l_y_plane', 'humerus_l_z_ele', 'humerus_l_y_ax')),
            #                     (('thorax_r_x_ext', 'thorax_r_y_ax', 'thorax_r_z_lat'), ('scapula_r_y_pro', 'scapula_r_z_lat', 'scapula_r_x_tilt'), ('humerus_r_y_plane', 'humerus_r_z_ele', 'humerus_r_y_ax'), ('clavicula_l_y_pro', 'clavicula_l_z_ele', 'clavicula_l_x_ax')),
            #                     (('thorax_r_x_ext', 'thorax_r_y_ax', 'thorax_r_z_lat'), ('humerus_r_y_plane', 'humerus_r_z_ele', 'humerus_r_y_ax'), ('thorax_l_x_ext', 'thorax_l_y_ax', 'thorax_l_z_lat'), ('humerus_l_y_plane', 'humerus_l_z_ele', 'humerus_l_y_ax')),
            #                     (('scapula_r_y_pro', 'scapula_r_z_lat', 'scapula_r_x_tilt'), ('humerus_r_y_plane', 'humerus_r_z_ele', 'humerus_r_y_ax'), ('thorax_l_x_ext', 'thorax_l_y_ax', 'thorax_l_z_lat'), ('clavicula_l_y_pro', 'clavicula_l_z_ele', 'clavicula_l_x_ax')),
            #                     (('thorax_r_x_ext', 'thorax_r_y_ax', 'thorax_r_z_lat'), ('scapula_r_y_pro', 'scapula_r_z_lat', 'scapula_r_x_tilt'), ('humerus_r_y_plane', 'humerus_r_z_ele', 'humerus_r_y_ax'), ('thorax_l_x_ext', 'thorax_l_y_ax', 'thorax_l_z_lat'), ('clavicula_l_y_pro', 'clavicula_l_z_ele', 'clavicula_l_x_ax')),
            #                     (('thorax_r_x_ext', 'thorax_r_y_ax', 'thorax_r_z_lat'), ('scapula_r_y_pro', 'scapula_r_z_lat', 'scapula_r_x_tilt'), ('humerus_r_y_plane', 'humerus_r_z_ele', 'humerus_r_y_ax'), ('scapula_l_y_pro', 'scapula_l_z_lat', 'scapula_l_x_tilt'), ('humerus_l_y_plane', 'humerus_l_z_ele', 'humerus_l_y_ax')),
            #                     (('scapula_r_y_pro', 'scapula_r_z_lat', 'scapula_r_x_tilt'), ('humerus_r_y_plane', 'humerus_r_z_ele', 'humerus_r_y_ax'), ('thorax_l_x_ext', 'thorax_l_y_ax', 'thorax_l_z_lat'), ('scapula_l_y_pro', 'scapula_l_z_lat', 'scapula_l_x_tilt'), ('humerus_l_y_plane', 'humerus_l_z_ele', 'humerus_l_y_ax')),
            #                     (('clavicula_r_y_pro', 'clavicula_r_z_ele', 'clavicula_r_x_ax'), ('scapula_r_y_pro', 'scapula_r_z_lat', 'scapula_r_x_tilt'), ('humerus_r_y_plane', 'humerus_r_z_ele', 'humerus_r_y_ax'), ('clavicula_l_y_pro', 'clavicula_l_z_ele', 'clavicula_l_x_ax'), ('scapula_l_y_pro', 'scapula_l_z_lat', 'scapula_l_x_tilt'), ('humerus_l_y_plane', 'humerus_l_z_ele', 'humerus_l_y_ax')),
            #                     (('thorax_r_x_ext', 'thorax_r_y_ax', 'thorax_r_z_lat'), ('clavicula_r_y_pro', 'clavicula_r_z_ele', 'clavicula_r_x_ax'), ('scapula_r_y_pro', 'scapula_r_z_lat', 'scapula_r_x_tilt'), ('humerus_r_y_plane', 'humerus_r_z_ele', 'humerus_r_y_ax'), ('clavicula_l_y_pro', 'clavicula_l_z_ele', 'clavicula_l_x_ax'), ('scapula_l_y_pro', 'scapula_l_z_lat', 'scapula_l_x_tilt'), ('humerus_l_y_plane', 'humerus_l_z_ele', 'humerus_l_y_ax')),
                                (('clavicula_r_y_pro', 'clavicula_r_z_ele', 'clavicula_r_x_ax'), ('scapula_r_y_pro', 'scapula_r_z_lat', 'scapula_r_x_tilt'), ('humerus_r_y_plane', 'humerus_r_z_ele', 'humerus_r_y_ax'), ('thorax_l_x_ext', 'thorax_l_y_ax', 'thorax_l_z_lat'), ('clavicula_l_y_pro', 'clavicula_l_z_ele', 'clavicula_l_x_ax'), ('scapula_l_y_pro', 'scapula_l_z_lat', 'scapula_l_x_tilt'), ('humerus_l_y_plane', 'humerus_l_z_ele', 'humerus_l_y_ax')),
                                (('thorax_r_x_ext', 'thorax_r_y_ax', 'thorax_r_z_lat'), ('clavicula_r_y_pro', 'clavicula_r_z_ele', 'clavicula_r_x_ax'), ('scapula_r_y_pro', 'scapula_r_z_lat', 'scapula_r_x_tilt'), ('humerus_r_y_plane', 'humerus_r_z_ele', 'humerus_r_y_ax'), ('thorax_l_x_ext', 'thorax_l_y_ax', 'thorax_l_z_lat'), ('clavicula_l_y_pro', 'clavicula_l_z_ele', 'clavicula_l_x_ax'), ('scapula_l_y_pro', 'scapula_l_z_lat', 'scapula_l_x_tilt'), ('humerus_l_y_plane', 'humerus_l_z_ele', 'humerus_l_y_ax'))]
        
        columns = []
        for column in column_combinations[index]:
            for col in column:
                columns.append(col)
        return columns
        #return [columnset for columnset in column_combinations[index]]
        


# Abductin is above 20 