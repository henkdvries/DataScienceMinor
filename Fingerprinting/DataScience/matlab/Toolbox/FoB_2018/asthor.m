function[T] =  asthor(IJ,PX,C7,T8)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                          %
% calculation of local coordinate system thorax.                           %
%                                                                          %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

yt = (IJ + C7)/2 - (T8 + PX)/2;  yt = yt/norm(yt);
xt = cross(yt,T8-PX);  xt = xt/norm(xt);
zt = cross(xt,yt);

T = [xt,yt,zt];
