
import os
import shutil

folderpath = '/Users/developer/Documents/School/DataScience/Octave/FobVisData HHS 20191009/Category_4'
outputpath = '/Users/developer/Documents/School/DataScience/Octave/FobVisData HHS 20191009/Catagory_4_fixed'

for patientid in os.listdir(folderpath):
    patientfolder = os.path.join(folderpath, patientid)
    outputfolder = os.path.join(outputpath, patientid)
    moutputfolder = os.path.join(outputfolder, 'm')

    if not os.path.isdir(outputfolder):
        os.mkdir(outputfolder)
    if not os.path.isdir(moutputfolder):
        os.mkdir(moutputfolder)

    if os.path.isdir(patientfolder):
        datafolder = os.path.join(patientfolder, 'dataruw')
        for filename in os.listdir(datafolder):

            patientfile = os.path.join(datafolder, filename)
            filebase = os.path.basename(patientfile)
            filename, extention = os.path.splitext(filebase)

            if filename.lower().endswith("im"):
                shutil.copyfile(os.path.join(datafolder, filebase),
                                os.path.join(outputfolder, 'IM.txt'))

                print(patientid, newpath)
            else:
                newpath = os.path.join(
                    outputfolder, filename[-3:].upper() + '.txt')

                shutil.copyfile(os.path.join(datafolder, filebase),
                                newpath)
                print(newpath)

        datafolder = os.path.join(patientfolder, 'DataCali')
        for filename in os.listdir(datafolder):

            patientfile = os.path.join(datafolder, filename)
            filebase = os.path.basename(patientfile)
            filename, extention = os.path.splitext(filebase)

            if filename.lower().endswith("im"):
                shutil.copyfile(os.path.join(datafolder, filebase),
                                os.path.join(moutputfolder, 'IM.m'))

                # os.rename(os.path.join(patientfolder, filebase),
                #           os.path.join(outputfolder, 'IM.txt'))
                newpath = os.path.join(patientfolder, 'IM.m')
                print(patientid, newpath)
            else:
                newpath = os.path.join(
                    moutputfolder, filename[-3:] + extention)
                shutil.copyfile(os.path.join(datafolder, filebase),
                                newpath)
                print(newpath)

                # Check for IM files
                #

                # if filename == 'IM1':
                #     print('found')
                #     os.rename(os.path.join(patientfolder, filebase),
                #               os.path.join(patientfolder, 'IM.txt'))
                # if extention == '.txt':
                #     if len(filename) == 2:
                #         print(os.path.join(patientfolder, filename + "1" + extention))
                #         os.rename(os.path.join(patientfolder, filebase),
                #                   os.path.join(patientfolder, filename + "1" + extention))
                #         # print(patientfolder, filename, extention)
