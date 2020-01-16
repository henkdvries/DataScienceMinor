function [sGH, hGH, sE, hE] = ghestsphere_acr(mov,receiverorder,nr_receivers)
% [sGH, hGH, sE, hE] = ghestsphere_acr(mov,receiverorder,nr_receivers)
% Sphere fitting procedure in the local coordinate systems of the scapula and humerus receivers
% 
% INPUT
%   mov:            movement file matrix
%   receiverorder:  order of receivers [stylus,thorax,scapula,humerus]
%                   e.g. right arm: [2,3,4,5], left arm: [2,3,7,8]
%   nr_receivers:   total number of receivers used during measurement
%
% OUTPUT
%   hGH: location of humerus GH rotation point (in humerus receiver)
%   sGH: location of scapular GH rotation point (in scapula receiver)
%   sE : Error GH rotation point (in scapula receiver)
%   hE : Error GH rotation point (in humerus receiver)

check_flag=0;
data = [mov];
nset = 4*nr_receivers;

scapula = receiverorder(3) - 1;
humerus = receiverorder(4) - 1;

Rv1=[]; Rv2=[]; Pv1=[]; Pv2=[];

DATA_H=[]; %humerus position and orientation in scapular sensor coordinate system
DATA_S=[]; %scapula position and orientation
DATA_Hruw=[]; %humerus position and orientation in scapular sensor coordinate system
DATA_Sruw=[]; %scapula position and orientation in humerus sensor coordinate system

for i=1:length(data)/nset;
    index = (i-1)*nset+(scapula-1)*4;
    %disp(['check scapula sensor : ',num2str(data(index+1,1))])
    sP  = data(index+1,2:4);                                      %Scapula sensor position (row vector)
    sR1 = (data(index+2,2:4)); %/norm(data(index+2,2:4)));
    sR2 = (data(index+3,2:4)); %/norm(data(index+3,2:4)));
    sR3 = (data(index+4,2:4)); %/norm(data(index+4,2:4)));
    S   = [sR1;sR2;sR3];                                           %Scapula sensor orientation (row vectors)

    %s(1,2:4)=sP;
    %s(2:4,2:4)=S;
    %DATA_Sruw=[DATA_Sruw;s]
    
    index = (i-1)*nset+(humerus-1)*4;
    hP = data(index+1,2:4);                                        %Humerus sensor position (row vector)
    %disp(['check humerus sensor : ',num2str(data(index+1,1))])
    hR1 = (data(index+2,2:4)); %/norm(data(index+2,2:4)));
    hR2 = (data(index+3,2:4)); %/norm(data(index+3,2:4)));
    hR3 = (data(index+4,2:4)); %/norm(data(index+4,2:4)));
    H   = [hR1;hR2;hR3];                                             %Scapula sensor orientation (row vectors)

    %h(1,2:4)=hP;
    %h(2:4,2:4)=H;
    %DATA_Hruw=[DATA_Hruw;h]
    
    % Scapula sensor fixed (transform to the local coordinate system of the scapula sensor)
    Ph=S*(hP-sP)';           % collumn vector
    %norm(Ph)
    Rh=S*H';                % orientation (collumn vectors)
    if check_flag==1
        disp('check : '), Is=S*S', Os=sP-sP
    end
    data_h(:,2:4)=[Ph';Rh']; % rowvectors
    
    % Humerus sensor fixed (transform to the local coordinate system of the humerus sensor)
    Ps=H*(sP-hP)';           % collumn vector   
    %norm(Ps)
    Rs=H*S';                % orientation (collumn vectors)
    if check_flag==1
        disp('check : '), Ih=H*H', Oh=hP-hP %pause
    end
    data_s(:,2:4)=[Ps';Rs']; % rowvectors
    
    DATA_H=[DATA_H;data_h];
    DATA_S=[DATA_S;data_s];
end

[xx,stxx]  = levmar('birdlm',zeros(6,1),DATA_H);
[xx,stxx]  = levmar('birdlm',xx,DATA_H);
[h_xx,h_stxx]  = levmar('birdlm',xx,DATA_H);
hV  = h_xx(1:3,1);
sAA = h_xx(4:6,1);
%sE  = stxx(4:6);

[xx,stxx] = levmar('birdlm',zeros(6,1),DATA_S);
[xx,stxx] = levmar('birdlm',xx,DATA_S);
[s_xx,s_stxx] = levmar('birdlm',xx,DATA_S);
sV  = s_xx(1:3,1);
hAA = s_xx(4:6,1);
%hE  = stxx(4:6);

if check_flag==1
    disp('check'), dVh=hV-hAA, dVs=sV-sAA
end

sGH=(sV+sAA)/2; % SV en SAA zouden hetzelfde punt moeten beschrijven, echter zijn op twee verschillende methode berekend (vanuit humerus sensor en scapula sensor) en daarom door twee delen=middelen
hGH=(hV+hAA)/2; % SV en SAA zouden hetzelfde punt moeten beschrijven, echter zijn op twee verschillende methode berekend (vanuit humerus sensor en scapula sensor) en daarom door twee delen=middelen
sE =(s_stxx(1:3,1)+h_stxx(4:6,1))/2;
hE =(s_stxx(4:6,1)+h_stxx(1:3,1))/2;

plotflag=0;
if plotflag==1
    figure(4),subplot(121),plot3(DATA_H(1:4:end,2),DATA_H(1:4:end,3),DATA_H(1:4:end,4),'.k'),hold on,
          subplot(121),plot3(DATA_H(1:4:end,2),DATA_H(1:4:end,3),DATA_H(1:4:end,4),' k'),hold on,axis equal
          title('relatieve humerus positie')
          xlabel('X (cm)'),ylabel('Y (cm)'),zlabel('Z (cm)')
          subplot(122),plot3(DATA_S(1:4:end,2),DATA_S(1:4:end,3),DATA_S(1:4:end,4),'.k'),hold on,
          subplot(122),plot3(DATA_S(1:4:end,2),DATA_S(1:4:end,3),DATA_S(1:4:end,4),' k'),hold on,axis equal,figure(gcf)
          title('relatieve scapula positie')
          xlabel('X (cm)'),ylabel('Y (cm)'),zlabel('Z (cm)')
          % GH 
          subplot(121),plot3(sGH(1,1),sGH(2,1),sGH(3,1),'.r','markersize',20),hold on,axis equal
          subplot(122),plot3(hGH(1,1),hGH(2,1),hGH(3,1),'.r','markersize',20),hold on,axis equal,figure(gcf)
          %print -f4 -r300 -dtiff FT2004_fig1.tif
end
      