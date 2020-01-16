function[Error,AngH,ANGH]=Test_GHrotatie(AngH)
% testen van axiale rotatie dmv simulatie van GH hoeken ev vergelijken van 
% input en uitkomst 
% Testen van subroutine roteuler.m of roteulern.m
% Input
%   AngH: 1e rotatie y-as, 2e rotatie z-as, 3e rotatie y'-as [graden]
%   bijv [10,12,8
%          5,21,9]
%   default: 21 waarden waarbij y'=[-90:9:90]'
% Output
%   Error: input-output: AngH-ANGH
%   AngH:  hoeken humerus (input)
%   ANGH:  hoeken humerus (output)



% aanpassen
%addpath h:\matlab\toolbox\fob
path(path,'\\vf-reva-arch\reva-arch$\Matlab\toolbox\FoB_2018\');

if nargin==0
    % Input rotations
    %AngH=[zeros(21,1),zeros(21,1)+rand(21,1)*10,[-90:9:90]']
    %AngH=[rand(21,1)*10-5,rand(21,1)*10,[-90:9:90]'+rand(21,1)*10']
    AngH=[rand(21,1)*10-5,[-90:9:90]'+rand(21,1)*10,rand(21,1)*10']
end


RadH=AngH/180*pi % van graden naar radialen

n=size(AngH,1)
for i=1:n
    Rh{i}=roty(RadH(i,1))*rotz(RadH(i,2))*roty(RadH(i,3))
    ANGH(i,:)=roteuler(Rh{i},6)
end

plot(AngH(:,3),ANGH(:,3),'.'), figure(gcf)
Error=AngH-ANGH
    