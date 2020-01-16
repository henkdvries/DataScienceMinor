import pprint
import os 
from models.models import Models 


class baseconfig:
    logging = False 
    basepath = os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], "data-clean/Category_{groupid}")
    pp = pprint.PrettyPrinter(indent=4)

    raw_visualization_enabled = False
    raw_visualization_autoplay = False
    show_visualization = False

    model = Models.LOGISTIC_REGRESSION
    multithreading = False
    workers = 20 
    differentiation = False

    columns_backup = ["thorax_r_x_ext", "thorax_r_y_ax", "thorax_r_z_lat",
                      "clavicula_r_y_pro", "clavicula_r_z_ele", "clavicula_r_x_ax",
                      "scapula_r_y_pro", "scapula_r_z_lat", "scapula_r_x_tilt",
                      "humerus_r_y_plane", "humerus_r_z_ele", "humerus_r_y_ax",
                      "ellebooghoek_r",
                      "thorax_l_x_ext", "thorax_l_y_ax", "thorax_l_z_lat",
                      "clavicula_l_y_pro", "clavicula_l_z_ele", "clavicula_l_x_ax",
                      "scapula_l_y_pro", "scapula_l_z_lat", "scapula_l_x_tilt",
                      "humerus_l_y_plane", "humerus_l_z_ele", "humerus_l_y_ax",
                      "ellebooghoek_l"]


class config(baseconfig):
    remove_idle = False
    resample_exercise = False 
    frame_generator = False 
    occupied_space = False 
    default = False 

    normalise = True

    remove_idle_split_count = 3
    frames_counts = 5
    binsize = 10
    frame_generator_count = 5

    exercisegroups = ['AF', 'EL', 'AB', 'RF', 'EH']
    exercise_count = len(exercisegroups)

    validation_split = 20
    shuffle_train = False
    batch_size = 0
 
    test_patients = {
        "1": [1, 5, 18, 20, 27, 11, 8, 12],
        "2": [2, 3, 5, 19, 23, 29, 8, 9, 10, 11, 12, 13],
        "3": [1, 5, 18, 20, 27, 10, 11, 12, 13],
        "4": [1, 5, 18, 20, 27]
    } 

    # For better printing! 
    column_index = -1
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
