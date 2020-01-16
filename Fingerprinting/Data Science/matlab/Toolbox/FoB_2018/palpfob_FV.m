function  [gANGLES,jANGLES,modelinputr,modelinputl,AllData] = palpfob_FV(data,blvectors,receiverorder,nr_receivers,vrmlfile)
% [gANGLES,jANGLES,modelinputr,modelinputl,alldata] = palpfob_FoBViS(data,blvectors,receiverorder,nr_receivers,vrmlfile)
% main program to proces palpation data from Flock-of-Bird system and recorder with FoBViS
% to bone % and joint rotations.
%
% INPUT: 
%   data        5 receivers measured: stylus, thorax, scapula, humerus, forearm
%   blvectors   local vectors of bony landmarks w.r.t. receivers
%               order: tIJ tPX tC7 tT8 tSC sPC sAC sAA sTS sAI sGH hEM hEL uSR uSU
%
% OUTPUT: 
%   gANGLES     bone rotations:     thorax      w.r.t. Global
%                                   clavicle    w.r.t. thorax
%                                   scapula     w.r.t. thorax
%                                   humerus     w.r.t. thorax
%         
%   jANGLES     joint rotations:    thorax      w.r.t. Global
%                                   clavicle    w.r.t. thorax
%                                   scapula     w.r.t. clavicle
%                                   humerus     w.r.t. scapula
%                                   ulna        w.r.t. humerus
%                                   radius      w.r.t. ulna
%   AllData     absolute bony landmarks [left,right] for all positions [cm]
% May 4, 1999, Frans van der Helm
% 05/27/1999 Remco Rotteveel
% 29/04/2004 Jurriaan de Groot Aangepast voor 8 sensoren voor 2-zijdig meten
%                              Berekening van sGH en hGH vanuit globale
%                              data
% 08-06-2018 Jurriaan de Groot Raw data of bony landmarks added to output

%
%   'this program will proces palpation data to bone and joint'
%   'rotations. input is data: 4 receivers of the FoB system  '
%   '(order stylus, scapulalocator, humerus, thorax),         '
%   'each providing 4x4 matrix (first column, receiver number;'
%   'first row, second to fourth column, position; second to  '
%   'fourth row and second to fourth column, orientation)     '
%   '                                                         '
%   '16 lines provide one collection of 4 receivers, which    '
%   'will be processed using blvectors (local vectors of bony '
%   'landmarks w.r.t. receivers) to global positions of bony  '
%   'landmarks and subsequently local coordinate systems of   '
%   'the bones.                                               '
%   'number of positions equals number of rows divided by 16  '
%   '                                                         '
%   'The following steps will be executed:                    '
%   '                                                         '
%   '1) transformation to the global coordinate system        '
%   '   (X: left-right, Y: upwards, Z: backwards, origin IJ)  '
%   '2) calculation of local coordinate systems               '
%   '3) estimation of axial rotation of the clavicula         '
%   '4) calculation of rotation matrices w.r.t. the global    '
%   '   coordinate system (bone rotations) and the local      '
%   '   coordinate system of the proximal bone (joint         ' 
%   '   rotations)                                            '
%   '5) parameterization of rotation matrices by Euler angles '
%   '   (order can be chosen)                                 '
%   '                                                         '
%   '   < press any key to continue >                         '
%   '*********************************************************'
%   '                                                         '

if nargin==2
    receiverorder=[2:9];
    nr_receivers=8;
end

disp('start palpfob_FV.m')
nset = 4*nr_receivers;                % number of receivers x4 lines per frame
[nDATA,mDATA]=size(data); nDATA = nDATA/nset;  % number of frames measured

% **************************************************************
% Rmg is the rotation from measurement coordinate system (FoB) to
% Global coordinate system

Rmg = [0  1   0
       0  0  -1
      -1  0   0];

alldata=[];
AllData = [];

close all
%plot_flag=1; 
plot_flag=0
if plot_flag==1,
%    close(3), figure(3)
    gDUMMY=zeros(14,3);
    h1_r=plot3(gDUMMY(:,1),gDUMMY(:,2),gDUMMY(:,3),'.g'); hold on
    h2_r=plot3(gDUMMY(10,1),gDUMMY(10,2),gDUMMY(10,3),'og');
    h3_r=fill3(gDUMMY([1,2,4,3,1],1),gDUMMY([1,2,4,3,1],2),gDUMMY([1,2,4,3,1],3),'g'); %thorax
    h4_r=plot3(gDUMMY([5,  6],1),gDUMMY([5,  6],2),gDUMMY([5,  6],3),'g'); %clavicle
    h5_r=plot3(gDUMMY([7:9,7],1),gDUMMY([7:9,7],2),gDUMMY([7:9,7],3),'g'); %scapula
           h=(gDUMMY(11,:)+gDUMMY(12,:))/2;
           u=(gDUMMY(13,:)+gDUMMY(14,:))/2;
    h6_r=plot3([gDUMMY(10,1),h(1,1)],[gDUMMY(10,2),h(1,2)],[gDUMMY(10,3),h(1,3)],'g'); %humerus
    h7_r=plot3([h(1,1),u(1,1)],[h(1,2),u(1,2)],[h(1,3),u(1,3)],'g'); %ulna

    h1_l=plot3(gDUMMY(:,1),gDUMMY(:,2),gDUMMY(:,3),'.r');
    h2_l=plot3(gDUMMY(10,1),gDUMMY(10,2),gDUMMY(10,3),'or');
    h3_l=fill3(gDUMMY([1,2,4,3,1],1),gDUMMY([1,2,4,3,1],2),gDUMMY([1,2,4,3,1],3),'r'); %thorax
    h4_l=plot3(gDUMMY([5,  6],1),gDUMMY([5,  6],2),gDUMMY([5,  6],3),'r'); %clavicle
    h5_l=plot3(gDUMMY([7:9,7],1),gDUMMY([7:9,7],2),gDUMMY([7:9,7],3),'r'); %scapula
    h6_l=plot3([gDUMMY(10,1),h(1,1)],[gDUMMY(10,2),h(1,2)],[gDUMMY(10,3),h(1,3)],'r'); %humerus
    h7_l=plot3([h(1,1),u(1,1)],[h(1,2),u(1,2)],[h(1,3),u(1,3)],'r'); %ulna
    axis square, view(2),set(gca,'xlim',[-20,100],'ylim',[-55,65],'zlim',[-25,95]),figure(gcf),pause(.2)
end

hw=waitbar(0,'processing');
for i = 1:nDATA
    %clc, disp(['nr=',num2str(i)])
    waitbar(i/nDATA)
    % CALCULATION OF GLOBAL COORDINATES
    pdata = data((i-1)*nset+1:(i-1)*nset+nset,2:4);
    %disp('pdata'),pdata,pause,disp('blvectors'),blvectors,pause,disp('side'),side,pause,disp('receiverorder'),receiverorder, pause
    [DATA_r] = makebl_FV(pdata,blvectors,'r',receiverorder([1:5]),5);       % make bony landmarks from receiver data
    [DATA_l] = makebl_FV(pdata,blvectors,'l',receiverorder([1:2,6:8]),5);   % make bony landmarks from receiver data

    if i == 1
        IJr = DATA_r(1,:)';                       % start with first IJ at [0 0 0]
        IJl = DATA_l(1,:)';                       % start with first IJ at [0 0 0]
    end

    gDATA_r = (Rmg*(DATA_r' - (diag(IJr)*ones(size(DATA_r))')))';
    gDATA_l = (Rmg*(DATA_l' - (diag(IJl)*ones(size(DATA_l))')))';

       % plot_flag=1;
       plot_flag = 0;
       %******************************************************************************** 
       % movement of the bony landmarks
       if plot_flag==1
           h=(gDATA_r(11,:)+gDATA_r(12,:))/2;
           u=(gDATA_r(13,:)+gDATA_r(14,:))/2;
           set(h1_r,'XData',gDATA_r( :,1),'YData',gDATA_r( :,2),'ZData',gDATA_r( :,3))
           set(h2_r,'XData',gDATA_r(10,1),'YData',gDATA_r(10,2),'ZData',gDATA_r(10,3))
           set(h3_r,'XData',gDATA_r([1,2,4,3,1],1),'YData',gDATA_r([1,2,4,3,1],2),'ZData',gDATA_r([1,2,4,3,1],3))
           set(h4_r,'XData',gDATA_r([5,  6],1),'YData',gDATA_r([5,  6],2),'ZData',gDATA_r([5,  6],3))
           set(h5_r,'XData',gDATA_r([7:9,7],1),'YData',gDATA_r([7:9,7],2),'ZData',gDATA_r([7:9,7],3))
           set(h6_r,'XData',[gDATA_r(10,1),h(1,1)],'YData',[gDATA_r(10,2),h(1,2)],'ZData',[gDATA_r(10,3),h(1,3)])
           set(h7_r,'XData',[h(1,1),u(1,1)],'YData',[h(1,2),u(1,2)],'ZData',[h(1,3),u(1,3)])

           h=(gDATA_l(11,:)+gDATA_l(12,:))/2;
           u=(gDATA_l(13,:)+gDATA_l(14,:))/2;
           set(h1_l,'XData',gDATA_l( :,1),'YData',gDATA_l( :,2),'ZData',gDATA_l( :,3))
           set(h2_l,'XData',gDATA_l(10,1),'YData',gDATA_l(10,2),'ZData',gDATA_l(10,3))
           set(h3_l,'XData',gDATA_l([1,2,4,3,1],1),'YData',gDATA_l([1,2,4,3,1],2),'ZData',gDATA_l([1,2,4,3,1],3))
           set(h4_l,'XData',gDATA_l([5,  6],1),'YData',gDATA_l([5,  6],2),'ZData',gDATA_l([5,  6],3))
           set(h5_l,'XData',gDATA_l([7:9,7],1),'YData',gDATA_l([7:9,7],2),'ZData',gDATA_l([7:9,7],3))
           set(h6_l,'XData',[gDATA_l(10,1),h(1,1)],'YData',[gDATA_l(10,2),h(1,2)],'ZData',[gDATA_l(10,3),h(1,3)])
           set(h7_l,'XData',[h(1,1),u(1,1)],'YData',[h(1,2),u(1,2)],'ZData',[h(1,3),u(1,3)])
         drawnow, pause(1/30)
       end
       %********************************************************************************    
       eval(['gDATA' num2str(i) ' = [gDATA_r,gDATA_l];'])   %Combine right and left data in GDATA
       alldata = [alldata;[gDATA_r,gDATA_l]];
      
       AllData{i} = [gDATA_r,gDATA_l];
       
end
close(hw)
%whos,return
clear IJr,clear gDATA_r,clear IJl,clear gDATA_l;

% **************************************************************
% global orientation matrices
AS=[];

for i = 1:nDATA
    for side=1:2
        sm1=(side-1)*3;
        sm2=(side-1)*15;

        eval(['gDATA = gDATA' num2str(i) ';'])
        [as(:,sm2+1:sm2+15)] = as_func(gDATA(:,sm1+1:sm1+3));
    end
    [AS] = [AS;as];
end
clear as;
%whos,return

% **************************************************************
% clavicula axial rotation
for side=1:2
    sm1=(side-1)*3;
    sm2=(side-1)*15;
    
    T = AS(:,sm2+1:sm2+3);               %check=[shoek(T(:,1),T(:,2)),shoek(T(:,2),T(:,3)),shoek(T(:,1),T(:,3))]
    C = AS(:,sm2+4:sm2+6);               %check=[shoek(C(:,1),C(:,2)),shoek(C(:,2),C(:,3)),shoek(C(:,1),C(:,3))]
    S = AS(:,sm2+7:sm2+9);               %check=[shoek(S(:,1),S(:,2)),shoek(S(:,2),S(:,3)),shoek(S(:,1),S(:,3))]
    [Cn,ROTr,ROTg]=axclav(C,S);          %check=[shoek(Cn(:,1),Cn(:,2)),shoek(Cn(:,2),Cn(:,3)),shoek(Cn(:,1),Cn(:,3))]
    AS(1:3*nDATA,sm2+4:sm2+6) = Cn;
    clear C S Cn;
end

       plot_flag=0;
       %******************************************************************************** 
       if plot_flag==1
           figure
           for j=1:4
               jm1=(j-1)*3;
               for i=1:nDATA
                   im1=(i-1)*3;
                   Ao=AS(im1+1:im1+3,jm1+1:jm1+3);
                   A1=AS(im1+1:im1+3,jm1+16:jm1+18);
                   
                   %disp('angles')
                   %check=[shoek(Ao(:,1),Ao(:,2)),shoek(Ao(:,2),Ao(:,3)),shoek(Ao(:,1),Ao(:,3))]
                   %check=[shoek(A1(:,1),A1(:,2)),shoek(A1(:,2),A1(:,3)),shoek(A1(:,1),A1(:,3))]
                   %disp('norm')
                   %norm(Ao(:,1)),norm(Ao(:,2)),norm(Ao(:,3))
                   %norm(A1(:,1)),norm(A1(:,2)),norm(A1(:,3)),pause
                   
                   plot3([0,Ao(1,1)],[0,Ao(2,1)],[0,Ao(3,1)],'b','linewidth',2),hold on
                   plot3([0,Ao(1,2)],[0,Ao(2,2)],[0,Ao(3,2)],'r','linewidth',2)
                   plot3([0,Ao(1,3)],[0,Ao(2,3)],[0,Ao(3,3)],'g','linewidth',2)
                   
                   plot3([0,A1(1,1)],[0,A1(2,1)],[0,A1(3,1)],'b','linewidth',1)
                   plot3([0,A1(1,2)],[0,A1(2,2)],[0,A1(3,2)],'r','linewidth',1)
                   plot3([0,A1(1,3)],[0,A1(2,3)],[0,A1(3,3)],'g','linewidth',1)
                   set(gca,'xlim',[-1,1],'ylim',[-1,1],'zlim',[-1,1]),view(3)
                   title(num2str(j)),axis square, figure(gcf),pause(.1),hold off
               end
           end
       end

% **************************************************************
% bone and joint rotations
%f=[
%   '4) calculation of rotation matrices w.r.t. the global    '
%   '   coordinate system (bone rotations) and the local      '
%   '   coordinate system of the proximal bone (joint         ' 
%   '   rotations)                                            '];

for side=1:2
    sm2=(side-1)*15;

    [gR(:,sm2+1:sm2+15)]=rotbones(AS(:,sm2+1:sm2+15)); %figure,plot([gR(2:3:end,sm2+10:sm2+12)],'.'),figure(gcf),pause
    [jR(:,sm2+1:sm2+15)]=rotjoint(AS(:,sm2+1:sm2+15));
end

% **************************************************************

%f=[
%   '5) parameterization of rotation matrices by Euler angles '
%   '                                                         '];

for side=1:2
    sm2=(side-1)*15;
    
    [gANGLES(1:nDATA,sm2+ 1:sm2+ 3)]=roteuler(gR(:,sm2+1 :sm2+ 3),1);
    [gANGLES(1:nDATA,sm2+ 4:sm2+ 6)]=roteuler(gR(:,sm2+4 :sm2+ 6),3);
    [gANGLES(1:nDATA,sm2+ 7:sm2+ 9)]=roteuler(gR(:,sm2+7 :sm2+ 9),3);
    [gANGLES(1:nDATA,sm2+10:sm2+12)]=roteuler(gR(:,sm2+10:sm2+12),6);
    [gANGLES(1:nDATA,sm2+13:sm2+15)]=zeros(nDATA,3);
    
    
    [jANGLES(1:nDATA,sm2+ 1:sm2+ 3)]=roteuler(jR(:,sm2+ 1:sm2+ 3),1);
    [jANGLES(1:nDATA,sm2+ 4:sm2+ 6)]=roteuler(jR(:,sm2+ 4:sm2+ 6),3);
    [jANGLES(1:nDATA,sm2+ 7:sm2+ 9)]=roteuler(jR(:,sm2+ 7:sm2+ 9),3);
    [jANGLES(1:nDATA,sm2+10:sm2+12)]=roteuler(jR(:,sm2+10:sm2+12),6);
    [jANGLES(1:nDATA,sm2+13:sm2+15)]=zeros(nDATA,3);
end

if (size(gR,2) == 30)
    disp('Calculation of elbow flexion and pro- supination')
    for side=1:2
        sm1=(side-1)*3;
        sm2=(side-1)*15;
        
        xx = zeros(3,1);
        fakt = 180/pi;
        for i = 1:nDATA
%[gANGLES(12);pi/2;pi/2],[gR(3*i-2:3*i,sm2+10:sm2+12) gR(3*i-2:3*i,sm2+13:sm2+15)]
            [xx,stxx]=levmar('gh_elbow',[gANGLES(12);pi/2;pi/2],[gR(3*i-2:3*i,sm2+10:sm2+12) gR(3*i-2:3*i,sm2+13:sm2+15)]);
            jANGLES(i,sm2+13:sm2+14) = xx(2:3)'*fakt;
            %gANGLES(i,sm2+12) = xx(1)*fakt;
            gANGLES(i,sm2+13) = xx(1)*fakt;
        end
    end
end

        plot_flag=0;
        %******************************************************************************** 
        if plot_flag==1
            figure
            for i=1:15
                subplot(5,3,i)
                plot(gANGLES(:,11),gANGLES(:,i),'.r',gANGLES(:,11),gANGLES(:,i),'-k',gANGLES(:,26),gANGLES(:,15+i),'.g',gANGLES(:,26),gANGLES(:,15+i),'-k')
                tln=[];
                I=num2str(i);
                for j=1:size(I,2)
                    tln=[tln,'_',I(j)];
                end
                title(['gANGLES',tln])
                %title(['gANGLES_',num2str(i)])
            end
            figure
            for i=1:15
                subplot(5,3,i)
                plot(jANGLES(:,11),jANGLES(:,i),'.r',jANGLES(:,11),jANGLES(:,i),'-k',jANGLES(:,26),jANGLES(:,15+i),'.g',jANGLES(:,26),jANGLES(:,15+i),'-k')
                tln=[];
                I=num2str(i);
                for j=1:size(I,2)
                    tln=[tln,'_',I(j)];
                end
                title(['jANGLES',tln])
                %title(['jANGLES_',num2str(i)])
            end
            figure(gcf)
        end
 
        
% **************************************************************
%
% output for shoulder/elbow model
% Noption = 3
%
% **************************************************************

if nr_receivers==8
    for side=1:2
        sm1=(side-1)*3;
        sm2=(side-1)*15;
        allIJ(:,sm1+1:sm1+3) = alldata(1:14:nDATA*14,sm1+1:sm1+3);  % motion of IJ
        ELx(:,side) = jANGLES(:,sm2+13);             % elbow flexion/extension
        PSy(:,side) = jANGLES(:,sm2+14);             % pro/supination
    end
else
    for side=1:2
        sm1=(side-1)*3;
        allIJ(:,sm1+1:sm1+3) = alldata(1:12:nDATA*12,sm1+1:sm1+3);  % motion of IJ
        ELx(:,side) = zeros(nDATA,1); % elbow flexion/extension
        PSy(:,side) = zeros(nDATA,1); % pro/supination
    end
end

PO = zeros(nDATA,6);  % wrist rotation
HF = zeros(nDATA,6);  % external hand forces
UM = zeros(nDATA,6);  % external hand moments

modelinputr = [gANGLES(:,   1:   3) allIJ(:,1:3) gANGLES(:,   4:   6) gANGLES(:,   7:   9) gANGLES(:,   10:   12) ELx(:,1) PSy(:,1) PO(:,1:3) HF(:,1:3) UM(:,1:3)]; 
modelinputl = [gANGLES(:,15+1:15+3) allIJ(:,4:6) gANGLES(:,15+4:15+6) gANGLES(:,15+7:15+9) gANGLES(:,15+10:15+12) ELx(:,2) PSy(:,2) PO(:,4:6) HF(:,4:6) UM(:,4:6)]; 
save modelinput modelinputr modelinputl
save rotdata AS jR gR jANGLES gANGLES gDATA 		%%% JURRIAAN 15-01-2002

        plot_flag=0;
        %******************************************************************************** 
        if plot_flag==1
            figure
            for i=1:17
                subplot(6,3,i)
                plot(modelinputr(:,14),modelinputr(:,i),'.r',modelinputr(:,14),modelinputr(:,i),'-k',modelinputl(:,14),modelinputl(:,i),'.g',modelinputl(:,14),modelinputl(:,i),'-k')
                title(['modelinput',num2str(i)])
            end
        end
        %******************************************************************************** 

% calculating the rotation matrix from scapula LCS using AA to scapula LCS using AC
% for use in VRML visualizations
for i = 1:nDATA
    im1=(i-1)*3;
    eval(['gDATA = gDATA' num2str(i) ';'])
    for side=1:2
        sm1=(side-1)*3;
        sm2=(side-1)*15;

        AC = gDATA( 6,sm1+1:sm1+3)';
        TS = gDATA( 8,sm1+1:sm1+3)';
        AI = gDATA( 9,sm1+1:sm1+3)'; 
        S = asscap(AC,TS,AI);		            % using AC instead of AA
        AS(im1+1:im1+3,sm2+7:sm2+9) = S;		% replacing the values in [AS]
    end  
end

       plot_flag=0;
       %******************************************************************************** 
       if plot_flag==1;
           for j=1:4
               jm1=(j-1)*3;
               for i=1:nDATA
                   im1=(i-1)*3;
                   Ao=AS(im1+1:im1+3,jm1+1:jm1+3);
                   A1=AS(im1+1:im1+3,jm1+16:jm1+18);
                
                   plot3([0,Ao(1,1)],[0,Ao(2,1)],[0,Ao(3,1)],'b','linewidth',2),hold on
                   plot3([0,Ao(1,2)],[0,Ao(2,2)],[0,Ao(3,2)],'r','linewidth',2)
                   plot3([0,Ao(1,3)],[0,Ao(2,3)],[0,Ao(3,3)],'g','linewidth',2)
                   
                   plot3([0,A1(1,1)],[0,A1(2,1)],[0,A1(3,1)],'b','linewidth',1)
                   plot3([0,A1(1,2)],[0,A1(2,2)],[0,A1(3,2)],'r','linewidth',1)
                   plot3([0,A1(1,3)],[0,A1(2,3)],[0,A1(3,3)],'g','linewidth',1)
                   set(gca,'xlim',[-1,1],'ylim',[-1,1],'zlim',[-1,1]),view(3)
                   title(num2str(j)),axis square, figure(gcf),pause(.1),hold off
               end
           end
       end
       %******************************************************************************** 


for side=1:2
    sm2=(side-1)*15;
    [jR(:,sm2+1:sm2+15)]=rotjoint(AS(:,sm2+1:sm2+15));
end


       plot_flag=0;
       %******************************************************************************** 
       if plot_flag==1
           for j=1:4
               jm1=(j-1)*3;
               for i=1:nDATA
                   im1=(i-1)*3;
                   Ao=AS(im1+1:im1+3,jm1+1:jm1+3);
                   A1=AS(im1+1:im1+3,jm1+16:jm1+18);
                
                   plot3([0,Ao(1,1)],[0,Ao(2,1)],[0,Ao(3,1)],'b','linewidth',2),hold on
                   plot3([0,Ao(1,2)],[0,Ao(2,2)],[0,Ao(3,2)],'r','linewidth',2)
                   plot3([0,Ao(1,3)],[0,Ao(2,3)],[0,Ao(3,3)],'g','linewidth',2)
                   
                   plot3([0,A1(1,1)],[0,A1(2,1)],[0,A1(3,1)],'b','linewidth',1)
                   plot3([0,A1(1,2)],[0,A1(2,2)],[0,A1(3,2)],'r','linewidth',1)
                   plot3([0,A1(1,3)],[0,A1(2,3)],[0,A1(3,3)],'g','linewidth',1)
                   set(gca,'xlim',[-1,1],'ylim',[-1,1],'zlim',[-1,1]),view(3)
                   title(num2str(j)),axis square, figure(gcf),pause(.1),hold off
               end
           end
       end
       %******************************************************************************** 


%save alles
%save %%% Jurriaan 15-01-2002

%rot2vrml(allIJ(:,1:3)/100,jR(:, 1:15),(ELx(:,1)*pi)/180,(PSy(:,1)*pi)/180,[vrmlfile '_r']); %right side
%rot2vrml(allIJ(:,4:6)/100,jR(:,16:30),(ELx(:,2)*pi)/180,(PSy(:,2)*pi)/180,[vrmlfile '_l']); %left side
disp('end palpfob_fv.m')
