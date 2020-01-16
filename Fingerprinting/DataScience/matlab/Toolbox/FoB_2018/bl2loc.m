function [xloc]=bl2loc(xglob,posR);

% program to calculate the local vector xloc of the bony
% landmark xglob w.r.t. the receiver coordinate system.

O = posR(1,:)';
R = posR(2:4,:)';
xloc = R'*(xglob - O);
