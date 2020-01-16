  function [Ry]=roty(th)
% vormen van een rotatiematrix voor rotaties rond de y-as
Ry(1,1)=cos(th);
Ry(1,3)=sin(th);
Ry(2,2)=1;
Ry(3,1)=-sin(th);
Ry(3,3)= cos(th);
