  function [Rx]=rotx(th)
% vormen van een rotatiematrix voor rotaties rond de x-as
Rx(1,1)=1;
Rx(2,2)=cos(th);
Rx(2,3)=-sin(th);
Rx(3,2)= sin(th);
Rx(3,3)= cos(th);
