import glob
import os
from optparse import OptionParser
from time import perf_counter
from itertools import groupby

import numpy as np
import pandas as pd

# Display all row when printing a dataframe
pd.set_option('display.max_rows', None)

labels = ["thorax_r_x", "thorax_r_y", "thorax_r_z",
          "clavicula_r_x", "clavicula_r_y", "clavicula_r_z",
          "scapula_r_x", "scapula_r_y", "scapula_r_z",
          "humerus_r_x", "humerus_r_y", "humerus_r_z",
          "ellebooghoek_r_x", "ellebooghoek_r_y", "ellebooghoek_r_z",
          "thorax_l_x", "thorax_l_y", "thorax_l_z",
          "clavicula_l_x", "clavicula_l_y", "clavicula_l_z",
          "scapula_l_x", "scapula_l_y", "scapula_l_z",
          "humerus_l_x", "humerus_l_y", "humerus_l_z",
          "ellebooghoek_l_x", "ellebooghoek_l_y", "ellebooghoek_l_z"]


def line_equation(pt1, pt2):
    """
    Points (pt) are encoded as (x, y).
    Get the a & b of f(x) = ax + b.
    :param pt1: coordinates of the first point
    :param pt2: coordinates of the second point
    :return:
    """
    m = (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])
    c = (pt2[1] - (m * pt2[0]))
    return m, c


def convert_to_level(intensity):
    """
    :param intensity: number
    :return: 1 if the value is greater than between. -1 if the value is smaller than between. Otherwise 0.
    """
    between = 0.01

    if intensity > between:
        return 1
    elif intensity < -between:
        return -1
    else:
        return 0


def get_variation(data):
    """

    :param data: Dataframe
    :return: Dataframe with all variation chunks
    """
    df_level = pd.DataFrame()

    if display:
        print('Get variations, please wait...')

    for label in labels:
        # GET VARIATION WITH LINE EQUATION FOR EACH ELEMENT IN COLUMN
        df_level[label] = data[label].apply(convert_to_level)
        # FOR CHUNK_SIZE BETWEEN 3 AND 8
        if display:
            print('Get variations for {0}, please wait...'.format(label))
        for chunk_size in range(3, 9):
            # FOR EACH ELEMENT IN COLUMN
            for index, row in df_level[label].iteritems():
                if index > df_level[label].size - chunk_size:
                    continue
                # IF THE VALUES BETWEEN ARE THE SAMES
                if len(list(set(df_level[label][index + 1:index + chunk_size - 1].tolist()))) == 1:
                    start_value = df_level[label][index]
                    between_value = df_level[label][index + 1]
                    end_value = df_level[label][index + chunk_size - 1]
                    # IF THE START & END VALUES ARE THE SAME
                    if start_value == end_value:
                        # IF THE VALUE BETWEEN & START ARE DIFFERENT [0, 1, 0]
                        if start_value != between_value:
                            for index_btw in range(index, index + chunk_size):
                                df_level[label][index_btw] = end_value
                    # IF THE START & END ARE DIFFERENT
                    elif start_value != end_value:
                        # IF THE VALUE START & BETWEEN & END ARE DIFFERENT [0, -1, 1]
                        if start_value != between_value != end_value:
                            for index_btw in range(index, index + chunk_size):
                                df_level[label][index_btw] = end_value
    return df_level


def get_intensity(data):
    old_row = []
    new_values = []

    if display:
        print('Get intensity, please wait...')

    # FOR EACH ROW IN DF
    for index, row in data.iterrows():
        if index == 0:
            old_row = row
            continue
        extract_value = []
        # FOR EACH BONE IN ROW
        for bone_index in range(int(len(labels) / 3)):
            indexes = [bone_index * 3, (bone_index * 3) + 1, (bone_index * 3) + 2]
            linear_eq_x = line_equation((index - 1, old_row[labels[indexes[0]]]), (index, row[labels[indexes[0]]]))
            linear_eq_y = line_equation((index - 1, old_row[labels[indexes[1]]]), (index, row[labels[indexes[1]]]))
            linear_eq_z = line_equation((index - 1, old_row[labels[indexes[2]]]), (index, row[labels[indexes[2]]]))
            extract_value.append(linear_eq_x[0])
            extract_value.append(linear_eq_y[0])
            extract_value.append(linear_eq_z[0])
        new_values.append(extract_value)
        # Create a copy of this row for the next iteration
        old_row = row
    return new_values


# Create 2D Array with pandas Series
def split_column(column):
    # 2D Array with chunks
    two_dimensional_array = []

    current_number = 0
    tmp_array = []

    for index, value in column.items():
        if index == 0:
            current_number = value
            tmp_array.append(value)
            continue

        if value == current_number:
            tmp_array.append(value)
        else:
            current_number = value
            two_dimensional_array.append(tmp_array)
            tmp_array = [value]

    two_dimensional_array.append(tmp_array)
    return two_dimensional_array


def get_schema(column):
    column_split = split_column(column)
    schema = []

    for index, variation in enumerate(column_split):
        if len(schema) == 0:
            schema.append(variation[0])
            continue

        if schema[-1] != variation[0]:
            schema.append(variation[0])
    return column_split, schema


def get_next_chunk(schema, chunks_size, current_index, number_of_frames, column):
    """
    Find the next schematics with almost the same size
    :param schema: CURRENT SCHEMA
    :param chunks_size:
    :param current_index:
    :param number_of_frames:
    :param column:
    :return: (SCHEMA OF THE NEXT CHUNK, START INDEX, END INDEX) IF A CHUNK IS FOUND OTHERWISE None
    """
    valid_chunks = []
    valid_schema = []
    # print(schema)
    for index, variation in enumerate(schema):
        # Skip the chunks before your chunk
        if current_index >= index:
            continue
        valid_schema.append(variation)
        valid_chunks.append(column[index])
        # print(len([item for sublist in column[index - len(valid_schema) + 1: index + 1] for item in sublist]))
        if len([item for sublist in column[index - len(valid_schema) + 1: index + 1] for item in sublist]) >= number_of_frames:
            # print(column[index - len(valid_schema) + 1: index + 1])
            return valid_schema, index - len(valid_schema) + 1, index + 1
        # return schema[index:index + chunks], index, index + chunks
    return valid_schema, len(schema) - len(valid_schema) - 1, len(schema) - 1


def normalize_array(smaller_array, bigger_array):
    number_of_values_to_add = len(bigger_array) - len(smaller_array)

    for value in range(number_of_values_to_add):
        step = number_of_values_to_add / len(smaller_array)
        array_index = int(step * value)

        if array_index >= len(smaller_array):
            array_index = len(smaller_array) - 1
        value_to_add = int((smaller_array[array_index] + smaller_array[array_index - 1]) / 2)
        smaller_array.insert(array_index, value_to_add)
    return smaller_array


def get_best(data, n=3):
    best_validation = []

    tmp_validation_chunk = data

    for index in range(n):
        minimum = None
        bone_name = None
        for bone in tmp_validation_chunk:
            if tmp_validation_chunk[bone] is None:
                continue
            if minimum is None:
                minimum = tmp_validation_chunk[bone]
                bone_name = bone
                continue
            if minimum['mean_difference'] > tmp_validation_chunk[bone]['mean_difference']:
                minimum = tmp_validation_chunk[bone]
                bone_name = bone
        if minimum is None:
            continue
        minimum['bone'] = bone_name
        best_validation.append(minimum)
        tmp_validation_chunk.pop(bone_name, None)
    test = list(map(lambda x: len(x['chunk']), best_validation))
    return test, best_validation


def normalize_schemas(data, bone, first_schema, second_schema):
    first_schema_array = data[bone][first_schema[0]:first_schema[1]].tolist()
    next_schema_array = data[bone][second_schema[0]:second_schema[1]].tolist()

    first_schema_size = len(first_schema_array)
    second_schema_size = len(next_schema_array)

    if first_schema_size > second_schema_size:
        next_schema_array = normalize_array(next_schema_array, first_schema_array)
    elif first_schema_size < second_schema_size:
        first_schema_array = normalize_array(first_schema_array, next_schema_array)

    if len(first_schema_array) != len(next_schema_array):
        print("WARNING!\n Arrays with different shapes: {0}, {1}\n".format(len(first_schema_array), len(next_schema_array)))
    return first_schema_array, next_schema_array


def find_chunks(data, data_intensity, data_variations):
    possible_chunks_per_bones = {}

    if display:
        print('Finding all possible chunks, please wait...')

    for label in labels:
        possible_chunks_per_bones[label] = []
        column_split, current_schema = get_schema(data_variations[label])

        # IF THE SCHEMA OF THE COLUMN IS TOO SMALL, THE COLUMN IS NOT USEFUL
        if len(current_schema) < 3 or len(get_indexes_change(data_variations[label].tolist())) < 4:
            possible_chunks_per_bones[label].append([])
            continue
        # FOR A CHUNK_SIZE BETWEEN 2 AND CURRENT_SCHEMA.LENGTH
        for number_of_chunks in range(2, len(current_schema)):
            # FOR EACH CHUNK OF CHUNK_SIZE LENGTH IN CURRENT_SCHEMA
            for index, variation in enumerate(current_schema):
                # SKIP LASTS CHUNKS
                if index > len(current_schema) - number_of_chunks:
                    continue
                current_chunks = column_split[index:index + number_of_chunks]

                current_chunk_start = len([item for sublist in column_split[0:index] for item in sublist])
                current_chunk_end = len([item for sublist in column_split[0:index + number_of_chunks] for item in sublist])
                possible_chunks = [{
                    'start': current_chunk_start,
                    'end': current_chunk_end,
                    'integral': np.trapz(tmp_df[label][current_chunk_start:current_chunk_end].tolist()),
                    'schema': current_schema[index:index + number_of_chunks],
                    'number_of_frames': current_chunk_end - current_chunk_start
                }]
                number_of_frames = current_chunk_end - current_chunk_start

                for secondary_index in range(index, len(current_schema) - number_of_chunks):
                    next_possible_chunk = get_next_chunk(current_schema, number_of_chunks, secondary_index, number_of_frames, column_split)
                    # IF THERE ARE NO NEXT POSSIBLE CHUNK, SKIP IT
                    if next_possible_chunk is None:
                        continue

                    next_chunk_start = len(
                        [item for sublist in column_split[0:next_possible_chunk[1]] for item in sublist])
                    next_chunk_end = len(
                        [item for sublist in column_split[0:next_possible_chunk[2]] for item in sublist])

                    # IF THE NEXT CHUNK START BEFORE THE END OF THE CURRENT CHUNK, SKIP IT
                    # if next_chunk_start < current_chunk_end:
                    #     continue

                    current_chunk_array, next_chunk_array = normalize_schemas(data, label, (current_chunk_start, current_chunk_end), (next_chunk_start, next_chunk_end))

                    # current_chunk_array = data[label][current_chunk_start:current_chunk_end].tolist()
                    # next_chunk_array = data[label][next_chunk_start:next_chunk_end].tolist()

                    current_chunk_integral = np.trapz(current_chunk_array)
                    next_chunk_integral = np.trapz(next_chunk_array)

                    if possible_chunks[-1]['end'] <= next_chunk_start and possible_chunks[0]['schema'][0] == next_possible_chunk[0][0] and possible_chunks[0]['schema'][-1] == next_possible_chunk[0][-1]:
                        possible_chunks.append({
                            'start': next_chunk_start,
                            'end': next_chunk_end,
                            'integral': next_chunk_integral,
                            'schema': next_possible_chunk[0],
                            'number_of_frames': next_chunk_end - next_chunk_start
                        })

                # tmp_possible_chunk = []
                #
                # for secondary_index, possible_chunk in enumerate(possible_chunks):
                #     if secondary_index == 0:
                #         tmp_possible_chunk.append(possible_chunk)
                #         continue

                if len(possible_chunks) > 1:
                    possible_chunks_per_bones[label].append(possible_chunks)

    validation_chunk = {}

    for bone in possible_chunks_per_bones:
        valid_chunk = None

        # print('For {0}:'.format(bone))
        for possible_chunk in possible_chunks_per_bones[bone]:
            if len(possible_chunk) == 0:
                continue
            number_of_frames = 0
            integrals = []
            integrals_difference = []

            for chunk in possible_chunk:
                number_of_frames += chunk['number_of_frames']
                integrals.append(chunk['integral'])
                # print(chunk)

            for chunk in possible_chunk:
                integrals_difference.append(abs(chunk['integral'] - np.mean(integrals)))
            # print(integrals_difference)
            percentage_of_usage = number_of_frames / len(data[bone])
            mean_difference = abs(np.mean(integrals) - possible_chunk[0]['integral'])
            # print("Percentage of usage: {0}\nMean difference: {1}\nMedian: {2}\nMean: {3}".format(percentage_of_usage, mean_difference, np.median(integrals), np.mean(integrals)))
            # print("Integrals mean difference: {0}".format(np.mean(integrals_difference) / len(possible_chunk)))
            # print("Percentage of usage * Mean difference: {0}".format((percentage_of_usage / len(possible_chunk)) * (10 / mean_difference)))
            # print('\n')
            if valid_chunk is None:
                valid_chunk = {
                    'chunk': possible_chunk,
                    'percentage_of_usage': percentage_of_usage,
                    'mean_difference': mean_difference
                }
            elif valid_chunk['percentage_of_usage'] <= percentage_of_usage:
                valid_chunk = {
                    'chunk': possible_chunk,
                    'percentage_of_usage': percentage_of_usage,
                    'mean_difference': mean_difference
                }
        validation_chunk[bone] = valid_chunk
        # print('\n\n')

    number_of_best_chunks = 15

    test, best_validation = get_best(validation_chunk, number_of_best_chunks)
    if len(best_validation) < number_of_best_chunks:
        if options.display:
            print("{0} contain only 1 time exercise".format(filename))
    else:
        if options.display:
            print(best_validation)
            print("{0} contains multiple exercise".format(filename))
        file_with_multiple_exercises.append((filename, list(set(test)), [(i, len(list(c))) for i, c in groupby(sorted(test))], len(test)))
    # IF THE BEST CHUNKS HAVE THE NUMBER OF CHUNKS
    # if len(list(set(test))) == 1:
    #     print('yes')
    # else:
    #     print('Different chunk number')

    for best_value in best_validation:
        best_value_separators = []

        for chunk in best_value['chunk']:
            best_value_separators.append(chunk['start'])
            best_value_separators.append(chunk['end'])

        lift = ''
        if options.lift:
            lift = ' --lift ' + str(options.lift)
        # print(best_value)
        if options.graph:
            os.system("python MultipleExercisesVisualisation.py -f " + filename + " -s " + ','.join(str(x) for x in best_value_separators) + ' -b ' + best_value['bone'] + lift)

    # for bone in validation_chunk:
    #     print('\n\nFor {0}'.format(bone))
    #     if validation_chunk[bone] is None:
    #         print('NOTHING')
    #         continue
    #     for chunk in validation_chunk[bone]['chunk']:
    #         print(chunk)
    #     print('Percentage of usage: {0}.\nMean Difference: {1}.'.format(validation_chunk[bone]['percentage_of_usage'], validation_chunk[bone]['mean_difference']))

    # if display:
    #     for bone in possible_chunks_per_bones:
    #         print("For {0}:\n".format(bone))
    #         if bone != 'thorax_r_x':
    #             continue
    #         for possible_chunk in possible_chunks_per_bones[bone]:
    #             number_of_frames = 0
    #             integrals = []
    #
    #             for chunk in possible_chunk:
    #                 print(chunk)
    #                 number_of_frames += chunk['number_of_frames']
    #                 integrals.append(chunk['integral'])
    #             print('Number of frames / {0} length: {1}%'.format(bone, round((number_of_frames / len(data[bone])) * 100, 2)))
    #             print('Mean: {0}.\nMean - First schema: {1}'.format(np.mean(integrals), np.mean(integrals) - possible_chunk[0]['integral']))
    #             print('\n\n')
    return possible_chunks_per_bones


def get_indexes_change(data):
    """
    Get an array with all indexes where the values change in the data array
    :param data: one dimensional array
    :return: array with all indexes where the values changes
    """
    separators_array = []

    for index, value in enumerate(data):
        if index == 0:
            continue
        if value != data[index - 1]:
            separators_array.append(index)
    if display:
        print('Separators are {0} and contains {1} values'.format(separators_array, len(separators_array)))
    return separators_array


def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


# Script entry point
if __name__ == '__main__':
    # Init OptionParser
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="use data inside the file.",
                      metavar="PATH_1,PATH_2")
    parser.add_option("-l", "--lift", dest="lift",
                      help="lift the data before process it.",
                      metavar="3")
    parser.add_option("-d", "--directory", dest="directory",
                      help="process all the files inside this directory.",
                      metavar="DIRECTORY_PATH")
    parser.add_option("-g", dest="graph", action="store_true",
                      help="Display graph with separator")
    parser.add_option("-v", dest="display", action="store_true",
                      help="Verbose mode")

    # Parse args
    (options, args) = parser.parse_args()

    display = options.display

    if not (options.filename or options.directory):
        raise ValueError('Please specify a file or a directory.')

    file_with_multiple_exercises = []

    filenames = []
    if options.filename:
        filenames.append(options.filename.split(','))
    if options.directory:
        directories = options.directory.split(',')

        for directory in directories:
            files = [f for f in glob.glob(directory + "/**/*.csv", recursive=True)]
            filenames.append(files)
    if options.lift:
        options.lift = int(options.lift)

    filenames = [item for sublist in filenames for item in sublist]
    if display:
        print('Files to process: {0}'.format(filenames))

    for file_index, filename in enumerate(filenames):
        if display:
            print('The file {0} is being processed. [{1}/{2}]'.format(filename, file_index + 1, len(filenames)))
        t1_start = perf_counter()
        df = pd.read_csv(filename, header=None)

        # Set columns name
        df = df.rename(columns={index: k for index, k in enumerate(labels)})

        tmp_df = df
        if options.lift:
            tmp_df = pd.DataFrame()

            if options.display:
                print('Lift data, please wait...')

            lift = options.lift if len(df.index) >= options.lift else len(df.index) - 1
            for bone in df:
                tmp_df[bone] = moving_average(np.array(df[bone]), lift)
        df_intensity = pd.DataFrame(data=get_intensity(tmp_df), columns=labels)
        df_variations = pd.DataFrame(data=get_variation(df_intensity), columns=labels)

        if options.graph:
            for label in labels:
                tmp_s = get_indexes_change(df_variations[label].tolist())
                lift = ''
                if options.lift:
                    lift = ' --lift ' + str(options.lift)
                # print('Visualization of separators for {0}'.format(label))
                # os.system("python VisualizeExercise.py -f " + filename + lift + ' -s ' + ','.join(str(x) for x in tmp_s))

        chunks = find_chunks(tmp_df, df_intensity, df_variations)

        separators = get_indexes_change(df_variations['thorax_r_x'].tolist())

        t1_stop = perf_counter()
        if options.display:
            print('Elapsed time: {0} seconds'.format(int(t1_stop - t1_start)))
        if options.graph:
            if len(separators) > 0:
                lift = ''
                if options.lift:
                    lift = ' --lift ' + str(options.lift)
                os.system("python VisualizeExercise.py -f " + filename + " -s " + ','.join(str(x) for x in separators) + lift)
            else:
                print("Can't find separators for {0}".format(filename))
    if len(filenames) == 0:
        exit()
    print("Here the files with multiple exercises ({0} file(s) => {1}%):".format(len(file_with_multiple_exercises), round((len(file_with_multiple_exercises) / len(filenames)) * 100), 2))
    for file, chunks, times, length in file_with_multiple_exercises:
        chance_str = ''
        for time in times:
            if length > 0:
                chance_str += '(' + str(time[0]) + ': ' + str(round(time[1] / length, 2)) + '%) '
        print("File: {0}\t\tPossible times: {1}\t\tPercentage per times: {2}".format(file, chunks, chance_str))
