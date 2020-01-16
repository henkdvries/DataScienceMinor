function blvecgh = rec2bl_gh(IM,loc1,loc2,loc3,receiverorder,mm,stylfile)

%  in IM the static trial (Initial Measurements) is stored,
%  with the position of bony landmarks w.r.t. the receiver.
%  order bony landmarks in the static trial:
%
%  PX:	Processus Xiphoideus, the most caudal point on the sternum
%  IJ: 	Incisura Jugularis, the most cranial point on the sternum
%  SC: 	The most ventral point at the sternoclavicular joint, about halfway the joint in vertical direction
%  PC: 	The most ventral point at the Processus Coracoideus
%  AC: 	The most dorsal point at the acromioclavicular joint (just in the small V-shape between clavicle and acromion)
%  AA: 	Angulus Acromialis: The most dorsolateral point at the scapular spine (a sharp corner point)
%  TS: 	Trigonum Spinae, a point at the medial border of the scapulae, in extension of the scapular spine
%  AI: 	Angulus Inferior, the most caudal point at the scapula
%  C7: 	Processus Spinosus of the 7th cervical vertebra
%  T8: 	Processus Spinosus of the 8th thoracic vertebra
%  EL: 	Most caudal point at the lateral epicondyle of the humerus
%  EM: 	Most caudal point at the medial epicondyle of the humerus
%  SR:   Most caudal point at the Processus Styloideus Radialis
%  SU:   Most caudal point at the Processus Styloideus Ulnaris
%
%  tIJ tPX  tC7  tT8  tSC  sAC  sAA  sTS  sAI  hGH hEM  hEL uSR uSU

%qu = setstr(39);

data = IM;
nset = 4*length(receiverorder);

stylus = receiverorder(1) - 1;
thorax = receiverorder(2) - 1;
scapulolocator = receiverorder(3) - 1;
humerus = receiverorder(4) - 1;

bl = 1;
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; PX = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=humerus;nr=(m-1)*nset+(rec-1)*4; hPXm(1:3,m-(bl-1)*mm) = bl2loc(PX,data(nr+1:nr+4,2:4));
end
hPX = mean(hPXm')';

bl = 2;
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; IJ = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=humerus;nr=(m-1)*nset+(rec-1)*4; hIJm(1:3,m-(bl-1)*mm) = bl2loc(IJ,data(nr+1:nr+4,2:4));
end
hIJ = mean(hIJm')';

bl = 3;
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; SC = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=humerus;nr=(m-1)*nset+(rec-1)*4; hSCm(1:3,m-(bl-1)*mm) = bl2loc(SC,data(nr+1:nr+4,2:4));
end
hSC = mean(hSCm')';

bl = 4;
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; PC = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=humerus;nr=(m-1)*nset+(rec-1)*4; hPCm(1:3,m-(bl-1)*mm) = bl2loc(PC,data(nr+1:nr+4,2:4));
end
hPC = mean(hPCm')';

bl = 5;
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; AC = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=humerus;nr=(m-1)*nset+(rec-1)*4; hACm(1:3,m-(bl-1)*mm)= bl2loc(AC,data(nr+1:nr+4,2:4));
end
hAC = mean(hACm')';

bl = 6;
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; AA = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=humerus;nr=(m-1)*nset+(rec-1)*4; hAAm(1:3,m-(bl-1)*mm) = bl2loc(AA,data(nr+1:nr+4,2:4));
end
hAA = mean(hAAm')';

bl = 7;
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; TS = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=humerus;nr=(m-1)*nset+(rec-1)*4; hTSm(1:3,m-(bl-1)*mm) = bl2loc(TS,data(nr+1:nr+4,2:4));
end
hTS = mean(hTSm')';

bl = 8;
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; AI = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=humerus;nr=(m-1)*nset+(rec-1)*4; hAIm(1:3,m-(bl-1)*mm) = bl2loc(AI,data(nr+1:nr+4,2:4));
end
hAI = mean(hAIm')';

bl = 9;
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; C7 = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=humerus;nr=(m-1)*nset+(rec-1)*4; hC7m(1:3,m-(bl-1)*mm) = bl2loc(C7,data(nr+1:nr+4,2:4));
end
hC7 = mean(hC7m')';

bl = 10;
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; T8 = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=humerus;nr=(m-1)*nset+(rec-1)*4; hT8m(1:3,m-(bl-1)*mm) = bl2loc(T8,data(nr+1:nr+4,2:4));
end
hT8 = mean(hT8m')';

bl = 11;
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; EL = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=humerus;nr=(m-1)*nset+(rec-1)*4; hELm(1:3,m-(bl-1)*mm) = bl2loc(EL,data(nr+1:nr+4,2:4));
end
hEL = mean(hELm')';

bl = 12;
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; EM = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=humerus;nr=(m-1)*nset+(rec-1)*4; hEMm(1:3,m-(bl-1)*mm) = bl2loc(EM,data(nr+1:nr+4,2:4));
end
hEM = mean(hEMm')';

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% estimation of local vector hGH with respect to humerus receiver
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

hGH=ghestnew(hPC*10,hAC*10,hAA*10,hTS*10,hAI*10);  % new version, by measurements Carel
hGH = hGH/10;                                      % regression is in millimeters!

blvecgh = [hIJ hPX hC7 hT8 hSC hAC hAA hTS hAI hGH hEM hEL];
