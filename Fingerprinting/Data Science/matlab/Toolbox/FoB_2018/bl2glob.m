function [xglob]=bl2glob(xloc,posR)

% program to calculate the global vector xglob of the bony
% landmark w.r.t. the receiver coordinate system, using xloc, the local
% vector of the bony landmark.

O = posR(1,:)';
R = posR(2:4,:)';
xglob = O + R*xloc;
