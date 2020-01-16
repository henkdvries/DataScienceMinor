function[C] =  asclav98(SC,AC)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                          %
% calculation local coordinate clavicula.                                  %
%                                                                          %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Y=[0 1 0]';      %  N.B. zc will be perpendicular to xc and GLOBAL Y-axis
                 %  true axial rotation will be estimated subsequently

xc = (AC-SC) / norm(AC-SC);
zc = cross(xc,Y); zc = zc / norm(zc);
yc = cross(zc,xc);
    
C  = [xc yc zc];
