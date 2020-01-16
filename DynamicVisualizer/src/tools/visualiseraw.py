import os 
import numpy as np 
import matplotlib as mpl
import re
from config import config


from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation

class VisualiseRaw:
    stick_bones = [(1, 2), (1, 5), (5, 6), (6, 7), (2, 3), (3, 4)]
    frame_order = [2, 3, 4, 5, 6, 7, 8, 9]
    labels = ['ground','thorax', 'clavicula', 'scapula', 'humerus','clavicula', 'scapula', 'humerus']
    interval = 10 

    def __init__(self, path, exercise):
        self.path = path 
        self.exercise = exercise 
        self.spacing = 1.45
        self.current_trajectory = 0 
        self.isvalid = True

        if config.raw_visualization_enabled:
            if not os.path.exists(path): 
                self.isvalid = False  
                  
            self.unpack_values() 
            self.generate_timeline() 
            self.generate_color_palette() 
            if config.raw_visualization_autoplay:
                self.visualise()

    def visualise(self):

        #TODO: framecount in title -> in update

        if self.isvalid:                  
            self.fig = plt.figure(facecolor='w')
            self.raw_fig = plt.subplot2grid((3,4), (0,0), colspan=4, rowspan=2, projection='3d')            
            self.raw_fig.axis('on')


            self.subplots = [
            plt.subplot2grid((3,4), (2,0)),            
            plt.subplot2grid((3,4), (2,1)),
            plt.subplot2grid((3,4), (2,2)),
            plt.subplot2grid((3,4), (2,3))]
            
            
            self.subplotdata_r = [
                self.exercise.dataframe[["thorax_r_x_ext", "thorax_r_y_ax", "thorax_r_z_lat"]].reset_index(drop=True),
                self.exercise.dataframe[["clavicula_r_y_pro", "clavicula_r_z_ele", "clavicula_r_x_ax"]].reset_index(drop=True),
                self.exercise.dataframe[[ "scapula_r_y_pro", "scapula_r_z_lat", "scapula_r_x_tilt"]].reset_index(drop=True),
                self.exercise.dataframe[[ "humerus_r_y_plane", "humerus_r_z_ele", "humerus_r_y_ax"]].reset_index(drop=True)]

            self.subplotdata_l = [
                self.exercise.dataframe[["thorax_l_x_ext", "thorax_l_y_ax", "thorax_l_z_lat"]].reset_index(drop=True),
                self.exercise.dataframe[["clavicula_l_y_pro", "clavicula_l_z_ele", "clavicula_l_x_ax"]].reset_index(drop=True),
                self.exercise.dataframe[[ "scapula_l_y_pro", "scapula_l_z_lat", "scapula_l_x_tilt"]].reset_index(drop=True),
                self.exercise.dataframe[[ "humerus_l_y_plane", "humerus_l_z_ele", "humerus_l_y_ax"]].reset_index(drop=True)]

            self.fig.tight_layout()

            self.subplots[0].axes.set_title('Thorax Sensor 1')
            self.subplots[0].plot(self.subplotdata_r[0], c=self.colors[1])
            self.subplots[0].plot(self.subplotdata_l[0], c=self.colors[0])
            self.subplots[1].axes.set_title('Clavicula Sensor 2 & 5')
            self.subplots[1].plot(self.subplotdata_r[1], c=self.colors[2])
            self.subplots[1].plot(self.subplotdata_l[1], c=self.colors[5])
            self.subplots[2].axes.set_title('Scapula Sensor 3 & 6')
            self.subplots[2].plot(self.subplotdata_r[2], c=self.colors[3])
            self.subplots[2].plot(self.subplotdata_l[2], c=self.colors[6])
            self.subplots[3].axes.set_title('Humerus Sensor 4 & 7')
            self.subplots[3].plot(self.subplotdata_r[3], c=self.colors[4])
            self.subplots[3].plot(self.subplotdata_l[3], c=self.colors[7])

            # setting axes names
            for plot in self.subplots:
                plot.grid()
                plot.axes.set_xlabel('framecount')
                plot.axes.set_ylabel('Deg')
            
            #annotating individual lines
            for df_list in (self.subplotdata_r,self.subplotdata_l):
                for j, df in enumerate(df_list):
                    for index in range(3):
                        y = len(df.index)-1
                        xy = (y,df.iat[y,index])
                        annostr = re.findall("_\w+_(\w+_\w+)", (df.columns[index]))[0]
                        self.subplots[j].axes.annotate(annostr,xy)
            


            # for index, plot in enumerate(self.subplots):
            #     plot.plot(self.subplotdata_r[index], c=self.colors)

            self.raw_fig.set_zlim(min(self.zvalues) * self.spacing , max(self.zvalues) * self.spacing)
            self.raw_fig.set_ylim(min(self.yvalues) * self.spacing , max(self.yvalues) * self.spacing)
            self.raw_fig.set_xlim(min(self.xvalues) * self.spacing , max(self.xvalues) * self.spacing) 
               
            self.points = sum([self.raw_fig.plot([], [], [], 'o', c=c * 0.5, markersize=7.5) for c in self.colors], [])
            self.texts = [self.raw_fig.text(1, 1, 1, '-', 'y', c=c) for c in self.colors]
            self.lines = sum([self.raw_fig.plot([], [], [], '-', c='b', linewidth=0.75) for c in range(len(VisualiseRaw.stick_bones))], [])
            self.trajectory_points = [sum([self.raw_fig.plot([], [], [], 'o', c=c * 0.5, markersize=7.5) for c in self.colors], []) for i in range(8)] 
            self.elbow_labels = [self.raw_fig.text(1, 1, 1, '', 'y'), self.raw_fig.text(1, 1, 1, '', 'y')]

            #self.subpoints = sum([graph.plot([],[]) for graph in self.subplots], [])
            self.framelines =  sum([subplot.plot([],[]) for subplot in self.subplots],[])

            for index, point in enumerate(self.points):
                point.set_label("{i} - {label}".format(label=VisualiseRaw.labels[index], i=index))
            
            self.raw_fig.view_init(-180, -180) 
            self.raw_fig.legend()

            self.frame_label = self.raw_fig.text2D(0.005, 2, "Frame: -", transform=self.raw_fig.transAxes)
            #self.frame_label = self.ax.text2D(0.005, 1.95, "2D Text", transform=self.ax.transAxes)
            import matplotlib
            mpl.style.use('seaborn-talk')
            plt.style.context('dark_background')
            plt.suptitle("group: {g} - patient: {p} - exercise: {e}".format(e=self.exercise.exercisestype, g=self.exercise.patientgroup, p=self.exercise.patientid), fontsize=13, color='black', style='italic')
            
            #self.ax.text(3, 2, 0,  'unicode: Institut für Festkörperphysik')    
            # matplotlib.use('Agg')
            print('start generating gif')
            anim = animation.FuncAnimation(self.fig, self.animation_update_frame, init_func=self.animation_init, frames=self.framecount, interval=VisualiseRaw.interval, blit=True)
            print('saved!') 
            plt.show()

    def animation_init(self):
        # Initalising the data-set
        for point in self.points:
            point.set_data([], [])
            point.set_3d_properties([])

        for line in self.framelines:
            line.set_data([],[])

        
        return self.points

    def generate_info_label(self, index):
        column_table = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [15, 16, 17], [18, 19, 20], [21, 22, 23], [24, 25, 26]]
        columnames = self.exercise.df.columns

        label = ''
        for index, row in enumerate(column_table):
            text = '{name}:    x={x}   y={y}    z={z}\n'.format(name=columnames[index], x='', y='', z='')
            label = label + text
        return label 


    def animation_update_frame(self, frame_index):
        frame = self.frame_data[frame_index] 
        x, y, z, label= ([] for i in range(4)) 
 
        
        #self.frame_label._text = 'Frame: {f}'.format(f=frame_index)
        #print(self.generate_info_label(frame_index) )
        #self.frame_label._text = self.generate_info_label(frame_index) 
        
        #Creating datapoint for every bone for 2d graphs

        for index, enum in enumerate(zip(self.framelines, self.subplotdata_r)):
            #for every plot get x and y appended to list
            line, data = enum
            line.set_data(frame_index, list(range(-300,300)))
                
                 

        # Creating x y z array's in correct order
        for key in VisualiseRaw.frame_order: 
            coords = frame[key] 
            x.append(coords[1])
            y.append(coords[2])
            z.append(coords[3])
            label.append(key)


        
        # Updating locations of points and their labels
        for index, enum in enumerate(zip(self.points, self.texts)):
            point, text = enum  
            point.set_data(x[index], y[index])
            point.set_3d_properties(z[index]) 
            text._position3d = [x[index] * 1.10, y[index], z[index]]
            text._text = str(label[index] - 2)

        # Updating location of lines between points
        for index, line in enumerate(self.lines):
            start_index, end_index = VisualiseRaw.stick_bones[index]
            xdata = [x[start_index], x[end_index]]
            ydata = [y[start_index], y[end_index]]
            zdata = [z[start_index], z[end_index]]
            line.set_data(xdata, ydata)
            line.set_3d_properties(zdata)

        # Updating trajectory points
        # Last used point is updated with lastest coordinates 
        for index, trajectory_list in enumerate(self.trajectory_points): 
            trajectory_list[self.current_trajectory].set_data(x[index], y[index])
            trajectory_list[self.current_trajectory].set_3d_properties(z[index])
            trajectory_list[self.current_trajectory]._color = self.colors[index]
            trajectory_list[self.current_trajectory]._markersize = 6

            # Upon each new frame, decreasing size / color of each trajectory point
            for index, trajectory in enumerate(trajectory_list):
                if index != self.current_trajectory:
                    trajectory._color = trajectory._color * 0.85
                    trajectory._markersize = trajectory._markersize * 0.9
 
        # Update current_trajectory to last used trajectory point for next frame
        if self.current_trajectory == len(self.colors) - 1:
            self.current_trajectory = 0 
        else: 
            self.current_trajectory = self.current_trajectory + 1
        
        # Two labels with elbow angle from converted data 
        self.elbow_labels[0]._position3d =  [x[6] * 1.04, y[6], z[6]]
        self.elbow_labels[0]._text = str(int(self.exercise.df['ellebooghoek_r'].iloc[frame_index] % 360))
        self.elbow_labels[1]._position3d =  [x[3] * 1.04, y[3], z[3]]
        self.elbow_labels[1]._text = str(int(self.exercise.df['ellebooghoek_l'].iloc[frame_index] % 360))

        self.raw_fig.set_ylabel(frame_index, fontsize = 20)
        # Drawing all changes! 
        self.fig.canvas.draw()
        return self.points 

    def unpack_values(self):
        if self.isvalid:
            self.sensor_data = {}   

            with open(self.path) as reader:
                lines = reader.readlines()  
                # Only .dat files have sensor info on 5th row
                isdatfile = lines[5][0] in '23456789' 
                if isdatfile: 
                    sensor_count = int(len(lines) / 5)
                else:
                    sensor_count = int(len(lines) / 10)
                
                for line_index in range(sensor_count):
                    if isdatfile:
                        sensor_record = lines[line_index * 5].replace('\n','').replace(' ', '').split('\t') 
                    else: 
                        sensor_record = lines[line_index * 10].replace('\n', '').split('  ')[:-1]
                    np_sensor_data = np.asarray(sensor_record, dtype=np.float64) 
                    # Setting data into 
                    if np_sensor_data[0] not in self.sensor_data:
                        self.sensor_data[np_sensor_data[0]] = [] 
                    self.sensor_data[np_sensor_data[0]].append(np_sensor_data)

    def generate_timeline(self):
        # TODO: Finding biggest / smallest value  
        self.xvalues = []
        self.yvalues = []
        self.zvalues = []
        if self.isvalid:
            # Making a timeline for the sensors  
            self.framecount = len(self.sensor_data[2]) 
            self.frame_data = []
            # Looping through every frame
            for frame in range(self.framecount):
                # For each frame, store each sensor 
                frame_sensors = {}

                for key, value in self.sensor_data.items():
                    # adding every sensor for the frame
                    frame_sensors[key] = self.sensor_data[key][frame]
                    self.xvalues.append(self.sensor_data[key][frame][1])
                    self.yvalues.append(self.sensor_data[key][frame][2])
                    self.zvalues.append(self.sensor_data[key][frame][3])
                    
                self.frame_data.append(frame_sensors)
            
    def generate_color_palette(self):
        if self.isvalid:
            color_count = len(self.frame_data[0].keys())
            self.colors = plt.cm.jet(np.linspace(0, 1, color_count))
            


        

