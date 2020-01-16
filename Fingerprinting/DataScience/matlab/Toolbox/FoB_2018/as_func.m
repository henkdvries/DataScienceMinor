function [as] = as_func(gdata)

%  function[as]=as_func(gdata)
%    bepalen van lokale positiematrices
%    gdata  = 14 x 3_matrix met botcoordinaten
%    as = [3,15]_matrix met positie matrices
%
% 05/27/1999 Remco Rotteveel

if (size(gdata,1) == 14)
   forearmpresent = 1;
else
   forearmpresent = 0;
end

IJ = gdata(1,:)';
PX = gdata(2,:)';
C7 = gdata(3,:)';
T8 = gdata(4,:)';
SC = gdata(5,:)';
AC = gdata(6,:)';
AA = gdata(7,:)';
TS = gdata(8,:)';
AI = gdata(9,:)'; 
GH = gdata(10,:)';
EM = gdata(11,:)';
EL = gdata(12,:)';
if (forearmpresent)
   SR = gdata(13,:)';
   SU = gdata(14,:)';
end

t=asthor(IJ,PX,C7,T8);          %disp('check T : '),[shoek(t(:,1),t(:,2)),shoek(t(:,2),t(:,3)),shoek(t(:,1),t(:,3))]
c=asclav98(SC,AC);              %disp('check C : '),[shoek(c(:,1),c(:,2)),shoek(c(:,2),c(:,3)),shoek(c(:,1),c(:,3))]
s=asscap(AA,TS,AI);             %disp('check S : '),[shoek(s(:,1),s(:,2)),shoek(s(:,2),s(:,3)),shoek(s(:,1),s(:,3))]
h=ashum(GH,EM,EL);              %disp('check H : '),[shoek(h(:,1),h(:,2)),shoek(h(:,2),h(:,3)),shoek(h(:,1),h(:,3))]
if(forearmpresent)
   f=asfore(EM,EL,SR,SU);       %disp('check F : '),[shoek(f(:,1),f(:,2)),shoek(f(:,2),f(:,3)),shoek(f(:,1),f(:,3))]
end
                              
if (forearmpresent)
   as=[t,c,s,h,f];
else
   as=[t,c,s,h];
end
