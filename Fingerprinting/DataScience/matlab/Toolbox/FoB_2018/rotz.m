  function [Rz]=rotz(th)
% vormen van een rotatiematrix voor rotaties rond de z-as
Rz(1,1)=cos(th);
Rz(1,2)=-sin(th);
Rz(2,1)= sin(th);
Rz(2,2)= cos(th);
Rz(3,3)=1;
