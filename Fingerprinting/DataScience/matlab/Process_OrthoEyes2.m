function[FoB,Init]=Process_OrthoEyes2(PP,Sessionnr,Init,FoB)
% [FoB,Init]=Process_proprio(PP,Sessionnr,Init,FoB) (origin: ProcessFOBVIS)
% Process the the raw data obtained with FOBVIS
%
% INPUT
%   PP  :   Subject number
%   Init:   Initialization data [struct]
%   FoB :   Previous results [struct] (optional)
%
% OUTPOUT
%   FoB :   Updated Results [struct]
%   Init:   Updated Initialization data [struct]
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% ADJUST
% DataLocation
DL=['/Users/developer/Documents/School/DataScience/Octave/Matlab/Data'] 
%DL=['\\vf-reva-arch\reva-arch$\2. PROJECTEN - Niet WMO-plichtig\Ortho Eyes\L:\2. PROJECTEN - Niet WMO-plichtig\Ortho Eyes\DATA_OrthoEyes_JURRIAAN\Category_1\']
%DL=['\\vf-reva-arch\reva-arch$\2. PROJECTEN - Niet WMO-plichtig\Ortho Eyes\FobVisData-HHS 20181010\data']
%DL=['\\vf-reva-arch\reva-arch$\2. PROJECTEN - Niet WMO-plichtig\Ortho Eyes\FobVisData-HHS 20181010\data']
%DL=['\\vf-reva-arch\reva-arch$\2. PROJECTEN - Niet WMO-plichtig\Ortho Eyes\FobVisData-HHS 20181010\data']

% Patient data
FoB( 1).Side='r'; % pat01
Sessionnr=1;

% ADDITIONAL FILENAMES SUBJECTS
Init.Flnm{ 1}='IM';    % initial measurement
% Init.Flnm{ 2}='MOV';   % movement
Init.Flnm{ 2}='AB1';   % abduction pre
Init.Flnm{ 3}='AB2';   % abduction pre
Init.Flnm{ 4}='AF1';   % anteflexion pre
Init.Flnm{ 5}='AF2';   % anteflexion pre
Init.Flnm{ 6}='ENDOEXOAF901';   % endo-exo high pre
Init.Flnm{ 7}='ENDOEXOAF902';   % endo-exo high pre
Init.Flnm{ 8}='ENDOEXOAB901';   % endo-exo high pre
Init.Flnm{ 9}='ENDOEXOAB902';   % endo-exo high pre
Init.Flnm{10}='RF1';   % retroflexion
Init.Flnm{11}='RF2';   % retroflexion pre
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% File INITIALIZATION
path(path,'/Users/developer/Documents/School/DataScience/Octave/Matlab/Toolbox/FoB_2018');
disp([path]);
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
%Init.CalFile = 'leiden_pols.m';
Init.CalFile = '/Users/developer/Documents/School/DataScience/Octave/Matlab/Toolbox/FoB_2018/leiden_pols.m'  % calibration file                                NB LOCAL ENVIRINMENT
Init.StylusFile = 'stylus_leidenkort';           % applied stylus                                  NB LOCAL APPLIED STYLUS
Init.N_init = 5;                                 % number of repetitions during initialisation
Init.ReceiverOrder=[2,3,4,5,6,7,8,9];            % ReceiverOrder

%path(path,'toolbox');             % path for FoBVis toolbox

%Data locations
Ddataruw =[DL,'/dataruw/'];
Ddatacali=[DL,'/datacali/'];
Dvrml    =[DL,'/data/vrml/'];
Dmatlab  =[DL,'/matlab/'];


for pp=1
    PP=pp;
    Init.Flag{PP,Sessionnr}=1;
    for Snr=Sessionnr
        % Define state of data processing
        if nargin==2
            Init.Flag{PP,Sessionnr}=1;
        end
        if size(FoB)<pp;
            Init.Flag{PP,Sessionnr}=1;
        end
        
        [r,c]=size(Init.Flag{PP,Snr});
        
        if (r<pp)
            Init.Flag{PP,Sessionnr}=1;
        end
        
        % CALIBRATION
        Init.Flag{PP,Sessionnr}=1;
        if    Init.Flag{PP,Sessionnr}==0 | Init.Flag{PP,Sessionnr}==1                        % if initialisation is 0 or 1 start calibration
            clc,disp('calibration')
            for k=1:size(Init.Flnm,2)
                sbj_nr=[num2str(pp)];
                flnm=[Init.Flnm{k}(1,:)];
                disp([sbj_nr,' : ',flnm]);
                datfile =[Ddataruw,Init.Flnm{k}(1,:),'.txt'];
                mfile   =[Ddatacali,Init.Flnm{k}(1,:),'.m'];
                disp(mfile);
                vrmlfile=[Dvrml,Init.Flnm{k}(1,:),'.wrl'];
                if exist(datfile)==2
                    add_flag=0;      % Flag to add dummy sensor data to *IM.m
                    if k==1
                        add_flag=1;
                    end
                    disp(datfile)
                    FoB(pp).datfile{Snr,k}=datfile
                    FoB(pp).mfile{Snr,k}=mfile
                    FoB(pp).vrml{Snr,k}=vrmlfile;
                    disp(['start calibration : ',mfile])
                    if exist(mfile)==0
                        dat2m_FV(datfile,Init.CalFile,mfile,add_flag);
                    end
                    disp(['stop calibration : ',mfile])
                end
            end
        end
        Init.Flag{PP,Sessionnr}=2
        save OrthoEyes2019.mat FoB Init
        
        disp('PASS 2')
        %FoB.Flag(PP)=2
        %_____________________________________________
        % CALCULATION OF 3D POSITION OF BONY LANDMARKS
        %   1. RELATIVE TO TRANSMITTOR (GDATA)
        %   2. RELATIVE TO LOCAL RECEIVERS (BLVECS)
        if  Init.Flag{PP,Sessionnr}==2
            tlr=0;
            disp(['Calculate (relative) position of bony landmarks'])
            receiverorder=Init.ReceiverOrder;
            sbj_nr=[num2str(pp)];
            disp(['pp=',num2str(pp),',  Snr=',num2str(Snr)])  %%%%%%%%%%%%% CHECK MOV en telling %%%%%%%%%%%%%%%%%%
            disp(FoB(pp).mfile{Snr,1}); %(1,:))
            IM  = FoB(pp).mfile{Snr,1};
            MOV = [];  %FoB(pp,Snr).mfile{2}, pause(.5)
            GHest_flag=0;  % regression method only
            
            [gdata,blvecs] = rec2bl_FV(IM,MOV,GHest_flag,receiverorder,Init.N_init,Init.StylusFile);
            FoB(pp).gdata{Snr}=gdata;
            FoB(pp).blvecs{Snr}=blvecs;
        end
        Init.Flag{PP,Sessionnr}=3;
        save OrthoEyes2019.mat FoB Init
        
        %_______________________________________________________________________
        % CALCULATION OF MOTIONS
        % CALIBRATION
        if Init.Flag{PP,Sessionnr}==3
            disp('Berekenen van gewrichtsrotations')
            %%%for pp=PP % subject number
            receiverorder=Init.ReceiverOrder;
            nr_receivers=size(receiverorder,2);
            %%%k=size(FoB(pp).mfile,2),pause
            for k=2:size(FoB(pp).mfile,2);
                %mfile = FoB(pp).mfile{k};
                disp(['Snr=',num2str(Snr),', k=',num2str(k),',  ',FoB(pp).mfile{Snr,k}]); %,pause(1)
                %exist(FoB(pp).mfile{k})
                if exist(FoB(pp).mfile{Snr,k},'file')
                    disp([FoB(pp).mfile{Snr,k},'file', 'exists'])
                    run(FoB(pp).mfile{Snr,k}) %%%, whos, pause
                    [gANGLES,jANGLES,modelinputr,modelinputl,alldata] = palpfob_FV(Data,FoB(pp).blvecs{Snr},receiverorder,nr_receivers,FoB(pp).vrml{Snr,k});
                    FoB(pp).gANGLES{Snr,k}=gANGLES;
                    FoB(pp).jANGLES{Snr,k}=jANGLES;
                    FoB(pp).modelinputr{Snr,k}=modelinputr;
                    FoB(pp).modelinputl{Snr,k}=modelinputl;
                    FoB(pp).AllData{Snr,k}=alldata;
                end
                disp('end PalpFob')
            end
        end
        Init.Flag{PP,Sessionnr}=4;
        save OrthoEyes2019.mat FoB Init
    end
end
end

