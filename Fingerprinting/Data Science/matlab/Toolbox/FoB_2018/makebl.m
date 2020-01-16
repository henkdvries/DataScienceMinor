function [DATA] = makebl(pdata,blvectors,side,receiverorder); 

%  program to calculate the position of bony landmarks w.r.t. the Global
%  Flock-of-Bird coordinate system from the receiver position and orientation
%  data (pdata) and the local vectors of the bony landmarks
% 
%  input:
%  pdata: 20 x 3 (receiver 1 to 5, first row position, next three rows rotation matrix
%
%  blvectors: 3 x 14 (local vectors of bony landmarks,
%                     order
%               tIJ tPX  tC7  tT8  tSC  sAC  sAA  sTS  sAI  hGH  hEM  hEL uSR uSU
%
%  output:
%  DATA 14 x 3 file with global positions of bony landmarks
%
% 05/27/1999 Remco Rotteveel

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

tIJ = blvectors(:,1);
tPX = blvectors(:,2);
tC7 = blvectors(:,3);
tT8 = blvectors(:,4);
tSC = blvectors(:,5);
sAC = blvectors(:,6);
sAA = blvectors(:,7);
sTS = blvectors(:,8);
sAI = blvectors(:,9);
hGH = blvectors(:,10);
hEM = blvectors(:,11);
hEL = blvectors(:,12);
if (forearmpresent)
   uSR = blvectors(:,13);
   uSU = blvectors(:,14);
end

nr = thorax; gIJ = bl2glob(tIJ,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = thorax; gPX = bl2glob(tPX,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = thorax; gC7 = bl2glob(tC7,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = thorax; gT8 = bl2glob(tT8,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = thorax; gSC = bl2glob(tSC,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = scapulolocator; gAC = bl2glob(sAC,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = scapulolocator; gAA = bl2glob(sAA,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = scapulolocator; gTS = bl2glob(sTS,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = scapulolocator; gAI = bl2glob(sAI,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = humerus; gGH = bl2glob(hGH,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = humerus; gEM = bl2glob(hEM,pdata((nr-1)*4+1:(nr-1)*4+4,:));
nr = humerus; gEL = bl2glob(hEL,pdata((nr-1)*4+1:(nr-1)*4+4,:));
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
   DATA(:,2) = -DATA(:,2);		% to convert left side to right side (the delft shoulder model
end									% only handles right shoulders)
