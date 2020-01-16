function [gdata,blvecs] = rec2bl_FV(IMflnm,mov,GHest_flag,receiverorder,mm,stylfile)
% [gdata,blvecs] = rec2bl_acr(IM,mov,GHest_flag,receiverorder,mm(facultative),stylfile(facultative))
%
%  NB ALLE BEWERKINGEN IN GLOBALE ASSENSTELSEL VAN FLOCK OF BIRDS: 
%                   X:voorwaards; Y: zijwaards; Z: naar beneden.
%
%  INPUT
%  in IM the static trial (Initial Measurements) is stored,
%  with the position of bony landmarks w.r.t. the receiver.
%  order bony landmarks in the static trial:
%
%  PX:	Processus Xiphoideus, the most caudal point on the sternum
%  IJ: 	Incisura Jugularis, the most cranial point on the sternum
%  C7: 	Processus Spinosus of the 7th cervical vertebra
%  T8: 	Processus Spinosus of the 8th thoracic vertebra
%  right shoulder:
%  SC: 	The most ventral point at the sternoclavicular joint, about halfway the joint in vertical direction
%  PC: 	The most ventral point at the Processus Coracoideus
%  AC: 	The most dorsal point at the acromioclavicular joint (just in the small V-shape between clavicle and acromion)
%  AA: 	Angulus Acromialis: The most dorsolateral point at the scapular spine (a sharp corner point)
%  TS: 	Trigonum Spinae, a point at the medial border of the scapulae, in extension of the scapular spine
%  AI: 	Angulus Inferior, the most caudal point at the scapula
%  EL: 	Most caudal point at the lateral epicondyle of the humerus
%  EM: 	Most caudal point at the medial epicondyle of the humerus
%  SR:  Most caudal point at the Processus Styloideus Radialis
%  SU:  Most caudal point at the Processus Styloideus Ulnaris
%  left shoulder:
%  SC: 	The most ventral point at the sternoclavicular joint, about halfway the joint in vertical direction
%  PC: 	The most ventral point at the Processus Coracoideus
%  AC: 	The most dorsal point at the acromioclavicular joint (just in the small V-shape between clavicle and acromion)
%  AA: 	Angulus Acromialis: The most dorsolateral point at the scapular spine (a sharp corner point)
%  TS: 	Trigonum Spinae, a point at the medial border of the scapulae, in extension of the scapular spine
%  AI: 	Angulus Inferior, the most caudal point at the scapula
%  EL: 	Most caudal point at the lateral epicondyle of the humerus
%  EM: 	Most caudal point at the medial epicondyle of the humerus
%  SR:  Most caudal point at the Processus Styloideus Radialis
%  SU:  Most caudal point at the Processus Styloideus Ulnaris
%
%  mov: movement file required for estimation of GH rotation center
%       if mov = [], then use regression equation Meskers 
%
%  GHest_flag : method of GH centre estimation 
%  [0:only regression; 1:spherefit; (2:screwaxis not OK yet)]
% 
%  facultative input
%
%  Receiver order:
%  Receiver 2: Stylus
%  Receiver 3: Thorax 
%  Receiver 4: Scapula right (acromion) 
%  Receiver 5: Upper arm right
%  Receiver 6: Forearm right
%  Receiver 7: Scapula left (acromion) 
%  Receiver 8: Upper arm left
%  Receiver 9: Forearm left
%
%  mm: number of recorded repetitions per bony landmark           [default 5]
%
%  stylfile: file name with stylus definitions [default = 'h:\matlab\toolbox\fob\stylus_leidenkort.m']
%
%  OUTPUT
%  gdata:  local input vectors for palpfob of the bony landmarks with respect to the receiver
%  order (input for palpfob_acr):
%  tIJ tPX  tC7  tT8  tSCr   sPC_r  sAC_r  sAA_r  sTS_r  sAI_r  sGH_r   []  hEM_r  hEL_r uSR_r uSU_r
%                     tSCl   sPC_l  sAC_l  sAA_l  sTS_l  sAI_l  sGH_l   []  hEM_l  hEL_l uSR_l uSU_l
%  blvecs: local vectors of all bony landmarks with respect to the receiver
%  order:
%  tIJ tPX  tC7  tT8  tSCr sPC_r sAC_r  sAA_r  sTS_r  sAI_r  sGH_r hGH_r hEM_r  hEL_r uSR_r uSU_r
%                     tSCl sPC_l sAC_l  sAA_l  sTS_l  sAI_l  sGH_l hGH_l hEM_l  hEL_l uSR_l uSU_l
%  4 May 1999, Frans van der Helm
%  05/26/1999 Remco Rotteveel
%  27/04/2004 Jurriaan de Groot: 
%      Aanpassen voor opname met acromion sensoren en 2 zijdig meten

%GHest_flag = 1 % 0: only regression; 1: spherefit; 2: screwaxis
%if isempty(mov)
%    flag_screw_axis=0;
%else
%    flag_screw_axis=1;
%end

if nargin == 5
    receiverorder_right=[2,3,4,5,6];
    receiverorder_left =[2,3,7,8,9];    
%    stylfile=['h:\matlab\toolbox\fob\stylus_leidenkort.m'];
elseif nargin == 4
%    stylfile=['h:\matlab\toolbox\fob\stylus_leidenkort.m'];
    receiverorder_right=[2,3,4,5,6];
    receiverorder_left =[2,3,7,8,9];    
    mm=5;
elseif nargin == 3
    receiverorder=[2,3,4,5,6,7,8,9];
    receiverorder_right=[2,3,4,5,6];
    receiverorder_left=[2,3,7,8,9];    
 %   stylfile=['h:\matlab\toolbox\fob\stylus_leidenkort.m'];
    mm=5;
elseif nargin == 2
    receiverorder=[2,3,4,5,6,7,8,9];
    receiverorder_right=[2,3,4,5,6];
    receiverorder_left =[2,3,7,8,9];    
 %   stylfile=['h:\matlab\toolbox\fob\stylus_leidenkort.m'];
    mm=5;
    GHest_flag = 0;
end

if isempty(mov)
    GHest_flag = 0;
end

[caldir,calname] = fileparts(IMflnm)
run([caldir,'/IM.m']);
whos
data=Data;

%whos
nset = 4*length(receiverorder);

stylus   = receiverorder(1) - 1;
thorax   = receiverorder(2) - 1;
scapular = receiverorder(3) - 1;
humerusr = receiverorder(4) - 1;
forearmr = receiverorder(5) - 1;
scapulal = receiverorder(6) - 1;
humerusl = receiverorder(7) - 1;
forearml = receiverorder(8) - 1;

bl = 2; disp('Processus Xiphoideus')  
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus; 
   nr=(m-1)*nset+(rec-1)*4;   
   PX = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=thorax; nr=(m-1)*nset+(rec-1)*4; tPXm(1:3,m-(bl-1)*mm) = bl2loc(PX,data(nr+1:nr+4,2:4));
end
tPX = mean(tPXm')';

bl = 1; % Incisura Jugularis
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; IJ = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=thorax;nr=(m-1)*nset+(rec-1)*4; tIJm(1:3,m-(bl-1)*mm) = bl2loc(IJ,data(nr+1:nr+4,2:4));
end
tIJ = mean(tIJm')';

bl = 3; % Cervicaal 7
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; C7 = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=thorax;nr=(m-1)*nset+(rec-1)*4; tC7m(1:3,m-(bl-1)*mm) = bl2loc(C7,data(nr+1:nr+4,2:4));
end
tC7 = mean(tC7m')';

bl = 4; %Thoracaal 8
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; T8 = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=thorax;nr=(m-1)*nset+(rec-1)*4; tT8m(1:3,m-(bl-1)*mm) = bl2loc(T8,data(nr+1:nr+4,2:4));
end
tT8 = mean(tT8m')';

bl = 5; %SternoClaviculair joint (right)
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; SCr = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=thorax;nr=(m-1)*nset+(rec-1)*4; tSCmr(1:3,m-(bl-1)*mm) = bl2loc(SCr,data(nr+1:nr+4,2:4));
end
tSCr = mean(tSCmr')';

bl = 6; %Processus Coracoideus (right) in scapular coordinate system
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; PCr = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=scapular;nr=(m-1)*nset+(rec-1)*4; sPCmr(1:3,m-(bl-1)*mm) = bl2loc(PCr,data(nr+1:nr+4,2:4));
end
sPCr = mean(sPCmr')';

bl = 7; %AcromioClavicular joint (right) in scapular coordinate system
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; ACr = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=scapular;nr=(m-1)*nset+(rec-1)*4; sACmr(1:3,m-(bl-1)*mm)= bl2loc(ACr,data(nr+1:nr+4,2:4));
end
sACr = mean(sACmr')';

bl = 8; %Angulus Acromialis (right) in scapular coordinate system
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; AAr = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=scapular;nr=(m-1)*nset+(rec-1)*4; sAAmr(1:3,m-(bl-1)*mm) = bl2loc(AAr,data(nr+1:nr+4,2:4));
end
sAAr = mean(sAAmr')';

bl = 9; %Trigonum Spinae (right) in scapular coordinate system
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; TSr = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=scapular;nr=(m-1)*nset+(rec-1)*4; sTSmr(1:3,m-(bl-1)*mm) = bl2loc(TSr,data(nr+1:nr+4,2:4));
end
sTSr = mean(sTSmr')';

bl = 10; %Angulus Inferior (right) in humerus coordinate system
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; AIr = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=scapular;nr=(m-1)*nset+(rec-1)*4; sAImr(1:3,m-(bl-1)*mm) = bl2loc(AIr,data(nr+1:nr+4,2:4));
end
sAIr = mean(sAImr')';

bl = 11; %Epicondylus Lateralis (right)
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; ELr = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=humerusr;nr=(m-1)*nset+(rec-1)*4; hELmr(1:3,m-(bl-1)*mm) = bl2loc(ELr,data(nr+1:nr+4,2:4));
end
hELr = mean(hELmr')';

bl = 12; %Epicodylus Medialis (right)
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; EMr = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=humerusr;nr=(m-1)*nset+(rec-1)*4; hEMmr(1:3,m-(bl-1)*mm) = bl2loc(EMr,data(nr+1:nr+4,2:4));
end
hEMr = mean(hEMmr')';

bl = 13; %Processus Styloideus Radialis (right)
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; SRr = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=forearmr;nr=(m-1)*nset+(rec-1)*4; uSRmr(1:3,m-(bl-1)*mm) = bl2loc(SRr,data(nr+1:nr+4,2:4));
end
uSRr = mean(uSRmr')';
   
bl = 14; %Processus Styloideus Ulnaris (right)
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; SUr = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=forearmr;nr=(m-1)*nset+(rec-1)*4; uSUmr(1:3,m-(bl-1)*mm) = bl2loc(SUr,data(nr+1:nr+4,2:4));
end
uSUr = mean(uSUmr')';


bl = 15; %SternoClaviculair joint (left)
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; SCl = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=thorax;nr=(m-1)*nset+(rec-1)*4; tSCml(1:3,m-(bl-1)*mm) = bl2loc(SCl,data(nr+1:nr+4,2:4));
end
tSCl = mean(tSCml')';

bl = 16; %Processus Corracoideus (left) in scapular coordinate system
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; PCl = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=scapulal;nr=(m-1)*nset+(rec-1)*4; sPCml(1:3,m-(bl-1)*mm) = bl2loc(PCl,data(nr+1:nr+4,2:4));
end
sPCl = mean(sPCml')';

bl = 17; %AcromioClavicular joint (left) in scapular coordinate system
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; ACl = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=scapulal;nr=(m-1)*nset+(rec-1)*4; sACml(1:3,m-(bl-1)*mm)= bl2loc(ACl,data(nr+1:nr+4,2:4));
end
sACl = mean(sACml')';

bl = 18; %Angulus Acromialis (left) in scapular coordinate system
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; AAl = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=scapulal;nr=(m-1)*nset+(rec-1)*4; sAAml(1:3,m-(bl-1)*mm) = bl2loc(AAl,data(nr+1:nr+4,2:4));
end
sAAl = mean(sAAml')';

bl = 19; %Trigonum Spinae (left) in scapular coordinate system
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; TSl = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=scapulal;nr=(m-1)*nset+(rec-1)*4; sTSml(1:3,m-(bl-1)*mm) = bl2loc(TSl,data(nr+1:nr+4,2:4));
end
sTSl = mean(sTSml')';

bl = 20; %Angulus Inferior (left) in scapula coordinate system
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; AIl = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=scapulal;nr=(m-1)*nset+(rec-1)*4; sAIml(1:3,m-(bl-1)*mm) = bl2loc(AIl,data(nr+1:nr+4,2:4));
end
sAIl = mean(sAIml')';

bl = 21; %Epicondylus Lateralis (left)
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; ELl = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=humerusl;nr=(m-1)*nset+(rec-1)*4; hELml(1:3,m-(bl-1)*mm) = bl2loc(ELl,data(nr+1:nr+4,2:4));
end
hELl = mean(hELml')';

bl = 22; %Epicodylus Medialis (left)
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; EMl = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=humerusl;nr=(m-1)*nset+(rec-1)*4; hEMml(1:3,m-(bl-1)*mm) = bl2loc(EMl,data(nr+1:nr+4,2:4));
end
hEMl = mean(hEMml')';

bl = 23; %Processus Styloideus Radialis (left)
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; SRl = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=forearml;nr=(m-1)*nset+(rec-1)*4; uSRml(1:3,m-(bl-1)*mm) = bl2loc(SRl,data(nr+1:nr+4,2:4));
end
uSRl = mean(uSRml')';
   
bl = 24; %Processus Styloideus Ulnaris (left)
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; SUl = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=forearml;nr=(m-1)*nset+(rec-1)*4; uSUml(1:3,m-(bl-1)*mm) = bl2loc(SUl,data(nr+1:nr+4,2:4));
end
uSUl = mean(uSUml')';


% right GH
sGHregr = ghestnew(sPCr*10,sACr*10,sAAr*10,sTSr*10,sAIr*10);  	 % new version, by measurements Carel
sGHregr = sGHregr/10;                                            % regression is in millimeters!
sGHr = sGHregr;
hGHr = [];

% left GH
% first mirror data
pc=sPCl; pc(2,:)=-pc(2,:);
ac=sACl; ac(2,:)=-ac(2,:);
aa=sAAl; aa(2,:)=-aa(2,:);
ts=sTSl; ts(2,:)=-ts(2,:);
ai=sAIl; ai(2,:)=-ai(2,:);
disp('GH regression estimation')
gh = ghestnew(pc*10,ac*10,aa*10,ts*10,ai*10);  	 % new version, by measurements Carel
gh = gh/10;
gh(2,:)=-gh(2,:);
sGHl = gh;
hGHl = [];


if GHest_flag==1;
    % calculation of GH by means of sphere estimation
    disp('GH sphere estimation')    
    [sGHr,hGHr,sEr,hEr] = ghestsphere_acr(mov,receiverorder_right(1:4),8);
    [sGHl,hGHl,sEl,hEl] = ghestsphere_acr(mov,receiverorder_left(1:4),8);
    
elseif GHest_flag==2;
    
    % calculation of GH by means of screw axes
    
    disp('GH screw axis estimation')    
    %position of GH relative to humerus and scapula sensors
    [sGHr,hGHr] = ghestscrew_acr(mov,receiverorder_right(1:4),8);
    [sGHl,hGHl] = ghestscrew_acr(mov,receiverorder_left( 1:4),8);
end

gdata  = [IJ  PX  C7  T8   SCr  PCr  ACr  AAr  TSr  AIr  sGHr       EMr  ELr  SRr  SUr  SCl  PCl  ACl  AAl  TSl  AIl  sGHl       EMl  ELl  SRl  SUl];
blvecs = [tIJ tPX tC7 tT8 tSCr sPCr sACr sAAr sTSr sAIr sGHr hGHr hEMr hELr uSRr uSUr tSCl sPCl sACl sAAl sTSl sAIl sGHl hGHl hEMl hELl uSRl uSUl];
