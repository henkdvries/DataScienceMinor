function [H] =  ashum(GH,EM,EL)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% function [H] =  ashum(GH,EM,EL)                                          %
%                                                                          %
%  calculation of local coordinate system humerus                          %
%                                                                          %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

H_mid=(EM+EL)/2;
yh = (GH-H_mid) / norm(GH-H_mid);
zh =  cross(EL-EM,yh);
zh = zh/norm(zh);
xh = cross(yh,zh);    
H = [xh,yh,zh];
