function [f]=asfore(EM,EL,SR,SU)

% program to calculate the local coordinate system of the forearm

y = (EM+EL)/2 - (SR+SU)/2;
y = y/norm(y);
xh = SR - SU;
z = cross(xh,y);
z = z/norm(z);
x = cross(y,z);

f = [x y z];

