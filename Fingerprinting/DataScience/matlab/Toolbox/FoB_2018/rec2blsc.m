function [output,hGH, sGH] = rec2blsc(IM,loc1,loc2,loc3,mov1,mov2,mov3,oftochmaarniet,receiverorder,mm,stylfile)

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
%  Receiver 2: Stylus
%  Receiver 3: Thorax 
%  Receiver 4: Scapulolocator
%  Receiver 5: Upper arm
%  Receiver 6: Forearm
%
%  In loc1, loc2, loc3 the position of the bony landmarks AA, TS, AI
%  with respect to the scapulalocator is recorded.
%
%  output: file with local vectors of the bony landmarks with
%          respect to the receiver
%  order:
%
%  tIJ tPX  tC7  tT8  tSC  sAC  sAA  sTS  sAI  hGH hEM  hEL uSR uSU
% 
%  4 May 1999, Frans van der Helm
%  05/26/1999 Remco Rotteveel
%  23 Oct 2008 Jurriaan de Groot (additional check on estimation of AC and thus GH)

qu = setstr(39);

data = IM;
nset = 4*length(receiverorder);

stylus = receiverorder(1) - 1;
thorax = receiverorder(2) - 1;
scapulolocator = receiverorder(3) - 1;
humerus = receiverorder(4) - 1;
if (length(receiverorder) == 5)
   forearmpresent = 1;
   forearm = receiverorder(5) - 1;
else
   forearmpresent = 0;
end

bl = 1;
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; PX = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=thorax;nr=(m-1)*nset+(rec-1)*4; tPXm(1:3,m-(bl-1)*mm) = bl2loc(PX,data(nr+1:nr+4,2:4));
end
tPX = mean(tPXm')';

bl = 2;
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; IJ = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=thorax;nr=(m-1)*nset+(rec-1)*4; tIJm(1:3,m-(bl-1)*mm) = bl2loc(IJ,data(nr+1:nr+4,2:4));
end
tIJ = mean(tIJm')';

bl = 3;
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; SC = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=thorax;nr=(m-1)*nset+(rec-1)*4; tSCm(1:3,m-(bl-1)*mm) = bl2loc(SC,data(nr+1:nr+4,2:4));
end
tSC = mean(tSCm')';

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
   rec=thorax;nr=(m-1)*nset+(rec-1)*4; tC7m(1:3,m-(bl-1)*mm) = bl2loc(C7,data(nr+1:nr+4,2:4));
end
tC7 = mean(tC7m')';

bl = 10;
for m=(bl-1)*mm+1:(bl-1)*mm+mm
   rec=stylus;nr=(m-1)*nset+(rec-1)*4; T8 = stylpos(data(nr+1:nr+4,2:4),stylfile);
   rec=thorax;nr=(m-1)*nset+(rec-1)*4; tT8m(1:3,m-(bl-1)*mm) = bl2loc(T8,data(nr+1:nr+4,2:4));
end
tT8 = mean(tT8m')';

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

if (forearmpresent)
   bl = 13;
   %bl = 14; %metingen michiel
   for m=(bl-1)*mm+1:(bl-1)*mm+mm
      rec=stylus;nr=(m-1)*nset+(rec-1)*4; SR = stylpos(data(nr+1:nr+4,2:4),stylfile);
      rec=forearm;nr=(m-1)*nset+(rec-1)*4; uSRm(1:3,m-(bl-1)*mm) = bl2loc(SR,data(nr+1:nr+4,2:4));
   end
   uSR = mean(uSRm')';
   
   bl = 14;
   %bl = 13; %metingen michiel
   for m=(bl-1)*mm+1:(bl-1)*mm+mm
      rec=stylus;nr=(m-1)*nset+(rec-1)*4; SU = stylpos(data(nr+1:nr+4,2:4),stylfile);
      rec=forearm;nr=(m-1)*nset+(rec-1)*4; uSUm(1:3,m-(bl-1)*mm) = bl2loc(SU,data(nr+1:nr+4,2:4));
   end
   uSU = mean(uSUm')';
end

[tIJ, tPX, tC7, tT8, tSC, hPC, hAC, hAA, hTS, hAI, hEL, hEM]
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% estimation of local vectors sAA, sTS and sAI from scapulolocator
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

nrec = length(receiverorder);
[nd,md]=size(loc1);
select=[];
for i=scapulolocator:nrec:nd/nrec
   select = [select;((i-1)*4+1:(i-1)*4+4)'];
end
loc1 = loc1(select,:);    % only receiver 2 (scapulolocator)

[nd,md]=size(loc2);
select=[];
for i=scapulolocator:nrec:nd/nrec
   select = [select;((i-1)*4+1:(i-1)*4+4)'];
end
loc2 = loc2(select,:);    % only receiver 2 (scapulolocator)

[nd,md]=size(loc3);
select=[];
for i=scapulolocator:nrec:nd/nrec
   select = [select;((i-1)*4+1:(i-1)*4+4)'];
end
loc3 = loc3(select,:);     % only receiver 2 (scapulolocator)

[sAA,sTS,sAI]=scaploc(loc1,loc2,loc3);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% estimation of sAC from scapular bony landmarks in the humerus receiver
% system and the scapular receiver system:
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 

[R,v,a,e]= veldpaus([hAA'; hTS' ;hAI'],[sAA'; sTS'; sAI']);
R = real(R);
[sAC]=veldrot(R,v,a,hAC'); sAC = sAC';

%CHECK ACCURACY of AC ESTIMATE
S_est=veldrot(R,v,a,[hAC';hAA'; hTS' ;hAI']);
sAC_est=S_est(1,:)';
sAA_est=S_est(2,:)';
sTS_est=S_est(3,:)';
sAI_est=S_est(4,:)';

N1=[norm(hAA-hTS);norm(hAA-hAI);norm(hTS-hAI)];
N2=[norm(sAA_est-sTS_est);norm(sAA_est-sAI_est);norm(sTS_est-sAI_est)];

E=sqrt([(sAA_est-sAA);(sTS_est-sTS);(sAI_est-sAI)]'*[(sAA_est-sAA);(sTS_est-sTS);(sAI_est-sAI)])
%E=sqrt((N2-N1)'*(N2-N1))
if E>=5, 
    msgbox('WARNING: Estimated scapulaframe differs from recorded scapula frame: sAC and sGH are not reliably estimated!','ERROR: ','warn')
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% estimation of local vector hGH with respect to humerus receiver
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if (oftochmaarniet)
   hGHregr = ghestnew(hPC*10,hAC*10,hAA*10,hTS*10,hAI*10);  	% new version, by measurements Carel
   hGH = hGHregr/10                                            % regression is in millimeters!
else
   hGHregr = ghestnew(hPC*10,hAC*10,hAA*10,hTS*10,hAI*10);  	% new version, by measurements Carel
   hGHregr = hGHregr/10                                        % regression is in millimeters!
   blvecgh = [tIJ tPX tC7 tT8 tSC hAC hAA hTS hAI hGHregr hEM hEL];
   [hGH, sGH] = ghestscrewsc(blvecgh,mov1,mov2,mov3,receiverorder,mm,stylfile,sAA,sTS,sAI,sAC)
end

if (length(receiverorder) == 5)
   output = [tIJ tPX tC7 tT8 tSC sAC sAA sTS sAI hGH hEM hEL uSR uSU];
else
   output = [tIJ tPX tC7 tT8 tSC sAC sAA sTS sAI hGH hEM hEL];
end
