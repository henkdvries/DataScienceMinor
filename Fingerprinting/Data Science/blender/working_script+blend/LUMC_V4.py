import bpy
import math

import pandas as pd 
import numpy as np
import os

def read_dataframe_from_file(filename):
    # Checking if file exists
    if os.path.exists(filename):

        # Reading file content with Pandas to a DataFrame
        # Generating column names from 0 - 29
        dataframe = pd.read_csv(filename, names=list(range(30)))

        # Renaming column names to bodypart, thanks to previous group for the names <3
        dataframe = dataframe.rename(columns={0: "thorax_r_x_ext", 1: "thorax_r_y_ax", 2: "thorax_r_z_lat"})
        dataframe = dataframe.rename(columns={3: "clavicula_r_y_pro", 4: "clavicula_r_z_ele", 5: "clavicula_r_x_ax"})
        dataframe = dataframe.rename(columns={6: "scapula_r_y_pro", 7: "scapula_r_z_lat", 8: "scapula_r_x_tilt"})
        dataframe = dataframe.rename(columns={9: "humerus_r_y_plane", 10: "humerus_r_z_ele", 11: "humerus_r_y_ax"})
        dataframe = dataframe.rename(columns={12: "ellebooghoek_r"})
        dataframe = dataframe.rename(columns={15: "thorax_l_x_ext", 16: "thorax_l_y_ax", 17: "thorax_l_z_lat"})
        dataframe = dataframe.rename(columns={18: "clavicula_l_y_pro", 19: "clavicula_l_z_ele", 20: "clavicula_l_x_ax"})
        dataframe = dataframe.rename(columns={21: "scapula_l_y_pro", 22: "scapula_l_z_lat", 23: "scapula_l_x_tilt"})
        dataframe = dataframe.rename(columns={24: "humerus_l_y_plane", 25: "humerus_l_z_ele", 26: "humerus_l_y_ax"})
        dataframe = dataframe.rename(columns={27: "ellebooghoek_l"})
        return dataframe
    else: 
        raise FileNotFoundError("CSV Niet gevonden")

def get_dataframe_from_bodypart(dataframe, bodypart, side=None):
    bodyparts = []
    
    # Extending the bodypart with the side ("thorax" -> "thorax_l")
    if side:
        bodypart = bodypart + '_' + side

    # Looping through available DataFrame columns 
    for columname in dataframe.columns.values: 
        # Compairing column name with requested bodypart
        if bodypart in str(columname):
            # Adding it to a list for pandas to filter
            bodyparts.append(columname)
    
    # Extracting the correct DataFrame columns to df_bodypart
    df_bodypart = dataframe[bodyparts]
    return df_bodypart


rotation_mode = 'XYZ' #don't cahnge!!
col = list() #dont'change!!

# all variables are cahged here:
#_________________________________________________________________________________________________________

grouping = 'oef' #choose you grouping type('cat','pat','meting','oef')
y = 0 #start
x = 0 #start
directory = 'D:\\Hochschule\\5_Semester\\Orthoeyes\\Data\\test-data\\'


#_________________________________________________________________________________________________________
for filename in os.listdir(directory):
    if filename.endswith(".csv"): 
        df = read_dataframe_from_file(directory+ filename)

        # Extracting some bodyparts to visualise
        df_thorax_r = get_dataframe_from_bodypart(df, 'thorax', 'r')
        df_thorax_l = get_dataframe_from_bodypart(df, 'thorax', 'l')
        df_clavicula_r = get_dataframe_from_bodypart(df, 'clavicula', 'r')
        df_clavicula_l = get_dataframe_from_bodypart(df, 'clavicula', 'l')
        df_scapula_r = get_dataframe_from_bodypart(df, 'scapula', 'r')
        df_scapula_l = get_dataframe_from_bodypart(df, 'scapula', 'l')
        df_humerus_r = get_dataframe_from_bodypart(df, 'humerus', 'r')
        df_humerus_l = get_dataframe_from_bodypart(df, 'humerus', 'l')
        df_ellebooghoek_r = get_dataframe_from_bodypart(df, 'ellebooghoek', 'r')
        df_ellebooghoek_l = get_dataframe_from_bodypart(df, 'ellebooghoek', 'l')


        print(df_ellebooghoek_r)
        ###### Blender relevant code following

        # search for armature in scene and name it ob
        ob = bpy.data.objects['Armature']
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.mode_set(mode='POSE')
        list_bones = list(ob.pose.bones)


        thorax_r = ob.pose.bones['thorax_r']
        thorax_l = ob.pose.bones['thorax_l']

        clavicula_r = ob.pose.bones['clavicula_r']
        clavicula_l = ob.pose.bones['clavicula_l']
        
        scapula_r = ob.pose.bones['scapula_r']
        scapula_l = ob.pose.bones['scapula_l']
        
        humerus_r = ob.pose.bones['humerus_r']
        humerus_l = ob.pose.bones['humerus_l']

        underarm_r = ob.pose.bones['underarm_r']
        underarm_l = ob.pose.bones['underarm_l']


        # Clear all set keyframes to avoid errors
        # Make sure input order is (X,Y,Z)
        for bone in list_bones :
            ob.animation_data_clear()
            bone.rotation_mode = rotation_mode
    
        print(list_bones)
        
        for key in range(int(int(df_thorax_r.size) / 3)):


            #saving the orientation for every bone in Numpy Array
            thorax_r_euler = np.array([(math.radians((df_thorax_r.loc[key,'thorax_r_x_ext']))), (math.radians((df_thorax_r.loc[key,'thorax_r_y_ax']))), (math.radians((df_thorax_r.loc[key,'thorax_r_z_lat'])))])
            thorax_l_euler = np.array([(math.radians((df_thorax_l.loc[key,'thorax_l_x_ext']))), (math.radians((df_thorax_l.loc[key,'thorax_l_y_ax']))), (math.radians((df_thorax_l.loc[key,'thorax_l_z_lat'])))])
    
            clavicula_r_euler = np.array([(math.radians((df_clavicula_r.loc[key,'clavicula_r_z_ele']))), (math.radians((df_clavicula_r.loc[key,'clavicula_r_x_ax']))), (math.radians((df_clavicula_r.loc[key,'clavicula_r_y_pro'])))])
            clavicula_l_euler = np.array([(math.radians((df_clavicula_l.loc[key,'clavicula_l_z_ele']))), (math.radians((df_clavicula_l.loc[key,'clavicula_l_x_ax']))), (math.radians((df_clavicula_l.loc[key,'clavicula_l_y_pro'])))])
    
            scapula_r_euler = np.array([(math.radians((df_scapula_r.loc[key,'scapula_r_z_lat']))), (math.radians((df_scapula_r.loc[key,'scapula_r_x_tilt']))), (math.radians((df_scapula_r.loc[key,'scapula_r_y_pro'])))])
            scapula_l_euler = np.array([(math.radians((df_scapula_l.loc[key,'scapula_l_z_lat']))), (math.radians((df_scapula_l.loc[key,'scapula_l_x_tilt']))), (math.radians((df_scapula_l.loc[key,'scapula_l_y_pro'])))])
    
            humerus_r_euler = np.array([(math.radians((df_humerus_r.loc[key,'humerus_r_y_ax']))), (math.radians((df_humerus_r.loc[key, 'humerus_r_y_plane']))), (math.radians((df_humerus_r.loc[key, 'humerus_r_z_ele'])))])
            humerus_l_euler = np.array([(math.radians((df_humerus_l.loc[key,'humerus_l_y_ax']))), (math.radians((df_humerus_l.loc[key, 'humerus_l_y_plane']))), (math.radians((df_humerus_l.loc[key, 'humerus_l_z_ele'])))])
    
    
            #Setting the rotation using radians.
            thorax_r.rotation_euler =  (thorax_r_euler[0], thorax_r_euler[1], thorax_r_euler[2]) 
            thorax_l.rotation_euler =  (thorax_l_euler[0], thorax_l_euler[1], thorax_l_euler[2]) #*np.array([-1,-1,-1])
    
            clavicula_r.rotation_euler =  (clavicula_r_euler[0], clavicula_r_euler[1], clavicula_r_euler[2]) *np.array([-1,1,1])
            clavicula_l.rotation_euler =  (clavicula_l_euler[0], clavicula_l_euler[1], clavicula_l_euler[2]) *np.array([1,-1,1])
    
            scapula_r.rotation_euler = (scapula_r_euler[0], scapula_r_euler[1], scapula_r_euler[2]) *np.array([-1,1,1])
            scapula_l.rotation_euler = (scapula_l_euler[0], scapula_l_euler[1], scapula_l_euler[2]) *np.array([1,-1,1])
    
            humerus_r.rotation_euler = (humerus_r_euler[0], humerus_r_euler[1], humerus_r_euler[2]) *np.array([-1,1,1])
            humerus_l.rotation_euler = (humerus_l_euler[0], humerus_l_euler[1], humerus_l_euler[2]) *np.array([1,-1,1])
    
            underarm_r.rotation_euler = (0,0,math.cos(math.radians((df_ellebooghoek_r.loc[key,'ellebooghoek_r'])))-humerus_r_euler[0]) * np.array([1,1,1])
            underarm_l.rotation_euler = (0,0,math.cos(math.radians((df_ellebooghoek_l.loc[key,'ellebooghoek_l'])))-humerus_l_euler[0])* np.array([1,1,-1])

            for bone in list_bones:
                #insert a keyframe
                bone.keyframe_insert(data_path="rotation_euler" ,frame= key)
                # Back to objectmode
                bpy.ops.object.mode_set(mode='OBJECT')
    
        #setting the animation length to length of one given dataframe
        if bpy.data.scenes[0].frame_end <= int(int(df_thorax_r.size) / 3) - 1:
            bpy.data.scenes[0].frame_end = int(int(df_thorax_r.size) / 3) - 1


                
        print(filename[:-4])
        ob_dub = ob.copy()   
        bpy.data.collections['Result'].objects.link(ob_dub)
        ob_dub.name = filename[:-4] 
        #bpy.data.collections['Result'].objects.link(ob_dub)
        bpy.ops.object.mode_set(mode='OBJECT')
        
    else:
        continue


for obj in bpy.data.collections['Result'].objects:
    if grouping == 'cat':
        name = "_".join(obj.name.split("_", 3)[:1])
    if grouping == 'pat':
        name = "_".join(obj.name.split("_", 3)[1:2])
    if grouping == 'meting':
        name = "_".join(obj.name.split("_", 3)[2:3])
    if grouping == 'oef':
        name = "_".join(obj.name.split("_", 3)[3:4])
    if name not in col:
        newCol = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(newCol)
        col.append(name)
    print(name)
    bpy.data.collections[name].objects.link(obj)
    bpy.data.collections['Result'].objects.unlink(obj)    


for key in col:
    for obj in bpy.data.collections[key].objects:
        obj.location = (y,x,0)
        x += 5
    x = 0
    y += 5
print(x)


