function [DATA] = makebl_FV(pdata,blvectors,side,receiverorder,nr_receivers); 

%  program to calculate the position of bony landmarks w.r.t. the Global
%  Flock-of-Bird coordinate system from the receiver position and orientation
%  data (pdata) and the local vectors of the bony landmarks
% 
%  input:
%  pdata: 26 x 3 (receiver 1 to 5, first row position, next three rows rotation matrix
%
%  blvectors: 3 x 15 (local vectors of bony landmarks,
%                     order
%               tIJ tPX  tC7  tT8  tSC  sPC  sAC  sAA  sTS  sAI  sGH  hEM  hEL uSR uSU
%
%  output:
%  DATA 15 x 3 file with global positions of bony landmarks
%
% 05/27/1999 Remco Rotteveel
% 05/10/2004 Jurriaan de Groot
%   GH gedefinieerd in scapula ipv humerus
%   blvectors uitgebreid met Proc. Coracoideus
%   DATA uitgebreid met Proc. Coracoideus
% 15/02/2010 Aangepast voor FoBVis
%   Volgorde IJ-PX omgedraaid
%   GH in invoer aan einde van blvector!

%path(path,'H:\matlab\toolbox\FoB');

stylus = receiverorder(1) - 1;
thorax = receiverorder(2) - 1;
scapula = receiverorder(3) - 1;
humerus = receiverorder(4) - 1;
if (nr_receivers == 5)
   forearmpresent = 1;
   forearm = receiverorder(5) - 1;
else
   forearmpresent = 0;
end

%blvectors,pause
tIJ = blvectors(:,2); 
tPX = blvectors(:,1);
tC7 = blvectors(:,3);
tT8 = blvectors(:,4);
tSC = blvectors(:,5);
sPC = blvectors(:,6);
sAC = blvectors(:,7);
sAA = blvectors(:,8);
sTS = blvectors(:,9);
sAI = blvectors(:,10);
sGH = blvectors(:,11); %ipv 11
hEM = blvectors(:,12); %ipv 12
hEL = blvectors(:,13); %ipv 13
% sGH = blvectors(:,25); %ipv 11
% hEM = blvectors(:,11); %ipv 12
% hEL = blvectors(:,12); %ipv 13
if (forearmpresent)
   uSR = blvectors(:,14); %ipv 14
   uSU = blvectors(:,15); %ipv 15
end

if side == 'l'
    tSC = blvectors(:,16); %ipv 16
    sPC = blvectors(:,17); %ipv 17
    sAC = blvectors(:,18); %ipv 18
    sAA = blvectors(:,19); %ipv 19
    sTS = blvectors(:,20); %ipv 20
    sAI = blvectors(:,21); %ipv 21
    sGH = blvectors(:,22); %ipv 22
    hEM = blvectors(:,23); %ipv 23
    hEL = blvectors(:,24); %ipv 24
    if (forearmpresent)
        uSR = blvectors(:,25); %ipv 25
        uSU = blvectors(:,26); %ipv 26
    end
end

%tIJ, nr = thorax, pdata((nr-1)*4+1:(nr-1)*4+4,:), whos,pause
nr = thorax;         gIJ = bl2glob(tIJ,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = thorax;         gPX = bl2glob(tPX,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = thorax;         gC7 = bl2glob(tC7,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = thorax;         gT8 = bl2glob(tT8,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = thorax;         gSC = bl2glob(tSC,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = scapula;        gAC = bl2glob(sAC,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = scapula;        gAA = bl2glob(sAA,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = scapula;        gTS = bl2glob(sTS,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = scapula;        gAI = bl2glob(sAI,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = scapula;        gGH = bl2glob(sGH,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = humerus;        gEM = bl2glob(hEM,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = humerus;        gEL = bl2glob(hEL,pdata((nr-1)*4+1:(nr-1)*4+4,:));
if (forearmpresent)
   nr = forearm; gSR = bl2glob(uSR,pdata((nr-1)*4+1:(nr-1)*4+4,:));
   nr = forearm; gSU = bl2glob(uSU,pdata((nr-1)*4+1:(nr-1)*4+4,:));
end

if (forearmpresent)
   DATA = [gIJ gPX gC7 gT8 gSC gAC gAA gTS gAI gGH gEM gEL gSR gSU]';
else
   DATA = [gIJ gPX gC7 gT8 gSC gAC gAA gTS gAI gGH gEM gEL]';
end

if (side == 'l')					% negate all x-coordinates (second column in FoB coordinate system!) 
   DATA(:,2) = -DATA(:,2);	    	% to convert left side to right side (the delft shoulder model
end									% only handles right shoulders)
