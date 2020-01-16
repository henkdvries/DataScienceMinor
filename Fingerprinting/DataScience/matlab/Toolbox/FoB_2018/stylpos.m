function [x]=stylpos(posR,stylfile)

% program to calculate the endpoint of the stylus
eval(['v = ' stylfile ';']);    % stylus length as calibrated
O = posR(1,:)';
R = posR(2:4,:)';
x = O + R*v;

