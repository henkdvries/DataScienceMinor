% Pass the path of patientgroup into orthoparser
function [patient_folders] = Process_Ortho_Group(patients_path)

patients_path = '/Users/developer/Documents/School/DataScience/Octave/FobVisData HHS 20191009/PersonalRecordings'
FoB_Toolbox = "/Users/developer/Documents/School/DataScience/Octave/Matlab/Toolbox/FoB_2018";
HHS_Toolbox = "/Users/developer/Documents/School/DataScience/master/matlab/Toolbox/HHS_Ortho";
Output_folder = "/Users/developer/Documents/School/DataScience/master/matlab/Output"

% Adding toolboxes to global path 
addpath(HHS_Toolbox,'-end');
addpath(FoB_Toolbox,'-end');

% ADDITIONAL FILENAMES SUBJECTS
filenames = ["IM", "AB1", "AB2", "AF1", "AF2", "EH1", "EH2", "EL1", "EL2", "RF1", "RF2"];


for file_id = 1:length(filenames)
    Init.Flnm{file_id}= string(filenames(file_id)); 
    fprintf("%d : %s\n", file_id, filenames(file_id));
end

% RECORDING/RECORDED STRUCTURES (Double Sided)
Init.Sensors{1}='Stylus';
Init.Sensors{2}='Thorax';
Init.Sensors{3}='Scapula (acromion) rechts';
Init.Sensors{4}='Humerus rechts';
Init.Sensors{5}='Radius-Ulna rechts';
Init.Sensors{6}='Scapula (acromion) links';
Init.Sensors{7}='Humerus links';
Init.Sensors{8}='Radius-Ulna links';

% ORDER OF PALPATED LANDMARKS (Double Sided)
Init.Landmarks{ 1}='PX: Processus Xiphoideus';
Init.Landmarks{ 2}='IJ: Incisura Jugularis';
Init.Landmarks{ 3}='C7: Processus Spinosus of the 7th cervical vertebra';
Init.Landmarks{ 4}='T8: Processus Spinosus of the 8th thoracic vertebra';
Init.Landmarks{ 5}='SCr: The most ventral point at the sternoclavicular joint, about halfway the joint in vertical direction';
Init.Landmarks{ 6}='PCr: The most ventral point at the Processus Coracoideus';
Init.Landmarks{ 7}='ACr: The most dorsal point at the acromioclavicular joint, just in the small V-shape between clavicle and acromion';
Init.Landmarks{ 8}='AAr: Angulus Acromialis: The most dorsolateral point at the scapular spine (a sharp corner point)';
Init.Landmarks{ 9}='TSr: Trigonum Spinae, a point at the medial border of the scapulae, in extension of the scapular spine';
Init.Landmarks{10}='AIr: Angulus Inferior, the most caudal point at the scapula';
Init.Landmarks{11}='ELr: Most caudal point at the lateral epicondyle of the humerus';
Init.Landmarks{12}='EMr: Most caudal point at the medial epicondyle of the humerus';
Init.Landmarks{13}='SRr: Most caudal point at the Processus Styloideus Radialis';
Init.Landmarks{14}='SUr: Most caudal point at the Processus Styloideus Ulnaris';
Init.Landmarks{15}='SCl: The most ventral point at the sternoclavicular joint, about halfway the joint in vertical direction';
Init.Landmarks{16}='PCl: The most ventral point at the Processus Coracoideus';
Init.Landmarks{17}='ACl: The most dorsal point at the acromioclavicular joint, just in the small V-shape between clavicle and acromion';
Init.Landmarks{18}='AAl: Angulus Acromialis: The most dorsolateral point at the scapular spine (a sharp corner point)';
Init.Landmarks{19}='TSl: Trigonum Spinae, a point at the medial border of the scapulae, in extension of the scapular spine';
Init.Landmarks{20}='AIl: Angulus Inferior, the most caudal point at the scapula';
Init.Landmarks{21}='ELl: Most caudal point at the lateral epicondyle of the humerus';
Init.Landmarks{22}='EMl: Most caudal point at the medial epicondyle of the humerus';
Init.Landmarks{23}='SRl: Most caudal point at the Processus Styloideus Radialis';
Init.Landmarks{24}='SUl: Most caudal point at the Processusf Styloideus Ulnaris';

% LandMarkOrder; which bony landmarks belong to the same bone
Init.LandMarkOrder{ 2}=[2 1 3 4 5 15];     % thorax
Init.LandMarkOrder{ 3}=[5 7];              % clavicle_r
Init.LandMarkOrder{ 4}=[6 7 8 9 10];       % scapula_r
Init.LandMarkOrder{ 5}=[11 12];            % humerus_r
Init.LandMarkOrder{ 6}=[13 14];            % ulna/radius_r
Init.LandMarkOrder{ 7}=[15 17];            % clavicle_l
Init.LandMarkOrder{ 8}=[16 17 18 19 20];   % scapula_l
Init.LandMarkOrder{ 9}=[21 22];            % humerus_l
Init.LandMarkOrder{10}=[23 24];            % ulna/radius_l

% PARAMETERS
Init.CalFile = convertStringsToChars(fullfile(FoB_Toolbox, 'leiden_pols.m'))   % calibration file                                NB LOCAL ENVIRINMENT
Init.StylusFile = 'stylus_leidenkort';                  % applied stylus                                  NB LOCAL APPLIED STYLUS
Init.N_init = 5;                                        % number of repetitions during initialisation
Init.ReceiverOrder=[2,3,4,5,6,7,8,9];                   % ReceiverOrder

% Finding all patients folders
patient_folders = iterfolder(patients_path);
fprintf("Found %d folders\n", length(patient_folders));

% For each patient (folder)
for patient_index  = 1:length(patient_folders)
    patient_folder = patient_folders(patient_index);
    [pathstr,patient_id,ext] = fileparts(string(patient_folder(1)));
    
    fprintf("Processing patient: %s\n", patient_id);
    
    patient_output   = fullfile(Output_folder, patient_id);
    patient_output_m = fullfile(patient_output, 'm');
   
    Sessionnr = 1;
    Snr = 1;
    pp = 1; % str2num(patient_id);


    % Creating patient folder if not present 
    if ~exist(patient_output)
        fprintf("Creating folder: %s\n", patient_output);
        mkdir(patient_output);
    end
    if ~exist(patient_output_m)
        fprintf("Creating folder: %s\n", patient_output_m);
        mkdir(patient_output_m);
    end
    
    % We do not use session and patient numbers in memory
    % We write the results directly into a folder
     
    
    % CALIBRATION 
    % disp('calibration')
    for k=1: size(Init.Flnm,2)
        sbj_nr =[num2str(pp)];
        flnm=[Init.Flnm{k}(1,:)];
         
        datfile = convertStringsToChars(fullfile(patient_folder,strcat(Init.Flnm{k}(1,:),'.txt')));
        mfile   = convertStringsToChars(fullfile(patient_output_m,strcat(Init.Flnm{k}(1,:),'.m')));
        vrmlfile= convertStringsToChars(fullfile(patient_output, strcat(Init.Flnm{k}(1,:),'.wrl')));
        fprintf("datfile: %s\n", datfile);
        if exist(datfile)==2
            add_flag=0;      % Flag to add dummy sensor data to *IM.m
            if k==1
                add_flag=1;
            end
              
            FoB(pp).datfile{Snr,k}=datfile
            FoB(pp).mfile{Snr,k}=mfile 
            FoB(pp).vrml{Snr,k}=vrmlfile;

            % disp(['start calibration : ',mfile])
            if exist(mfile)==0
                dat2m_FV(datfile,Init.CalFile,mfile,add_flag);
            end 
        end
    end

    %_____________________________________________
    % CALCULATION OF 3D POSITION OF BONY LANDMARKS
    %   1. RELATIVE TO TRANSMITTOR (GDATA)
    %   2. RELATIVE TO LOCAL RECEIVERS (BLVECS)
    
    tlr=0;
    %disp(['Calculate (relative) position of bony landmarks'])
    receiverorder=Init.ReceiverOrder;
    sbj_nr=[num2str(pp)];
    %disp(['pp=',num2str(pp),',  Snr=',num2str(Snr)])  %%%%%%%%%%%%% CHECK MOV en telling %%%%%%%%%%%%%%%%%%
    %disp(FoB(pp).mfile{Snr,1}); %(1,:))
    IM  = FoB(pp).mfile{Snr,1};
    MOV = [];  %FoB(pp,Snr).mfile{2}, pause(.5)
    GHest_flag=0;  % regression method only
    
    [gdata,blvecs] = rec2bl_FV(IM,MOV,GHest_flag,receiverorder,Init.N_init,Init.StylusFile);
    FoB(pp).gdata{Snr}=gdata;
    FoB(pp).blvecs{Snr}=blvecs;
    %_______________________________________________________________________
    % CALCULATION OF MOTIONS
    % CALIBRATION
    
    %disp('Berekenen van gewrichtsrotations')
    %%%for pp=PP % subject number
    receiverorder=Init.ReceiverOrder;
    nr_receivers=size(receiverorder,2);
    fprintf("Processing patient: %s | Files: ", patient_id); 
    %%%k=size(FoB(pp).mfile,2),pause
    for k=2:size(FoB(pp).mfile,2);
        %mfile = FoB(pp).mfile{k};
        %disp(['Snr=',num2str(Snr),', k=',num2str(k),',  ',FoB(pp).mfile{Snr,k}]); %,pause(1)
        %exist(FoB(pp).mfile{k})
        if exist(FoB(pp).mfile{Snr,k},'file')
             
            run(FoB(pp).mfile{Snr,k}) %%%, whos, pause
            [gANGLES,jANGLES,modelinputr,modelinputl,alldata] = palpfob_FV(Data,FoB(pp).blvecs{Snr},receiverorder,nr_receivers,FoB(pp).vrml{Snr,k});
            dlmwrite(fullfile(patient_output, strcat(Init.Flnm{k}(1,:),'.csv')), gANGLES, 'precision', '%i');
            fprintf("%s\t",strcat(Init.Flnm{k}(1,:),'.csv'));
             
        end
        %disp('end PalpFob')
    end
    fprintf("\n");

fprintf("Done!\n")

end