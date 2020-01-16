import pprint
import os 


class baseconfig:
    logging = False 
    basepath = os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], "data-clean/Category_{groupid}")
    pp = pprint.PrettyPrinter(indent=4)

    raw_visualization_enabled = False
    raw_visualization_autoplay = False
    show_visualization = False

    multithreading = False
    workers = 20 

class config(baseconfig):
    remove_idle_split_count = 3
    frames_counts = 5
    binsize = 10
    frame_generator_count = 5

    exercisegroups = ['AF', 'EL', 'AB', 'RF', 'EH']
    exercise_count = len(exercisegroups)

    columns = ["thorax_r_x_ext", "thorax_r_y_ax", "thorax_r_z_lat",
               "clavicula_r_y_pro", "clavicula_r_z_ele", "clavicula_r_x_ax",
               "scapula_r_y_pro", "scapula_r_z_lat", "scapula_r_x_tilt",
               "humerus_r_y_plane", "humerus_r_z_ele", "humerus_r_y_ax",
               "ellebooghoek_r",
               "thorax_l_x_ext", "thorax_l_y_ax", "thorax_l_z_lat",
               "clavicula_l_y_pro", "clavicula_l_z_ele", "clavicula_l_x_ax",
               "scapula_l_y_pro", "scapula_l_z_lat", "scapula_l_x_tilt",
               "humerus_l_y_plane", "humerus_l_z_ele", "humerus_l_y_ax",
               "ellebooghoek_l"]
