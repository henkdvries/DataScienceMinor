function [hGH, sGH] = ghestscrewsc(blvecgh,mov1,mov2,mov3,receiverorder,mm,stylfile,aas,tss,ais,acs)

%Instantane schroefas berekening, waarbij de humerus en een scapula
%receiver worden gebruikt. De assen wordt in het scapulaire receiver stelsel (Popts) met als 
%oorsprong de receiver berekend en in het humerus receiver stelsel (Popth)
%Vervolgens wordt de berekening ook nog in het lokale scapulaire assenstelsel (Popt5) uitgevoerd.

% Remco Rotteveel en Dennis Magermans (klein beetje)12/01/00

data = [mov1; mov2; mov3];
nset = 4*length(receiverorder);

stylus = receiverorder(1) - 1;
thorax = receiverorder(2) - 1;
scapulolocator = receiverorder(3) - 1;
humerus = receiverorder(4) - 1;

ijs = blvecgh(:,1); pxs = blvecgh(:,2); c7s = blvecgh(:,3); t8s = blvecgh(:,4);
scs = blvecgh(:,5); ghs = blvecgh(:,10); ems = blvecgh(:,11); els = blvecgh(:,12);

Rv1=[]; Rv2=[]; Pv1=[]; Pv2=[];
for i=1:length(data)/nset;
   index = (i-1)*nset+(scapulolocator-1)*4;
   P1 = data(index+1,2:4);
   R1 = [data(index+2,2:4) data(index+3,2:4) data(index+4,2:4)];
   index = (i-1)*nset+(humerus-1)*4;
   P2 = data(index+1,2:4);
   R2 = [data(index+2,2:4) data(index+3,2:4) data(index+4,2:4)];

   Pv1=[Pv1;P1]; %scapulaire receiver positie en rot matrix (in bird stelsel)
   Rv1=[Rv1;R1];
   Pv2=[Pv2;P2]; %bovenarm receiver positie en rot matrix (bird)
   Rv2=[Rv2;R2];
end
 
Gh=[];El=[];Em=[];Aa=[];Ts=[];Ai=[];Ac=[]; 
 
[m,f]=size(Rv1);
  for i=1:m,           %aantal samples

    Rma=reshape(Rv1(i,:),3,3)'; %rot matrix scapulaire receiver t.o.v. bird
    Rm1=Rma/norm(Rma);
    Rmb=reshape(Rv2(i,:),3,3)'; %rot matrix humerus receiver t.o.v. bird
    Rm2=Rmb/norm(Rmb);

    Rm21=Rm1*Rm2';              				%rot mat hum.rec. in scap.rec. orientatie
    Rm11=Rm1*Rm1';              				%rot mat scap.rec. in scap.rec. orientatie
    Pv21(i,:)=[Rm1*[Pv2(i,:)-Pv1(i,:)]']';%pos hum rec(2)in scap rec stelsel(1)
    Rv21(i,:)=[reshape(Rm21',1,9)];       %rot hum oa in scap rec stelsel
    Pv11(i,:)=[Rm1*[Pv1(i,:)-Pv1(i,:)]']';%pos scap rec in scap rec stelsel
    Rv11(i,:)=[reshape(Rm11',1,9)];       %rot mat scap in scap rec stelsel
    
    Rm12=Rm2*Rm1'; 								%rot mat scap rec. in hum rec. orientatie
    Rm22=Rm2*Rm2'; 								%rot mat hum rec. in hum rec. orientatie
    Pv12(i,:)=[Rm2*[Pv1(i,:)-Pv2(i,:)]']';%pos scap rec(1)in hum rec stelsel(2)
    Rv12(i,:)=[reshape(Rm12',1,9)];       %rot scap rec in hum rec stelsel
    Pv22(i,:)=[Rm2*[Pv2(i,:)-Pv2(i,:)]']';%pos hum rec in hum rec stelsel
    Rv22(i,:)=[reshape(Rm22',1,9)];       %rot hum scap in hum rec stelsel

    Gh1=Rm2' * ghs + Pv2(i,:)';Gh=[Gh;Gh1'];
    El1=Rm2' * els + Pv2(i,:)';El=[El;El1'];%bird coord (Rm2 is rotatiematrix humerus receiver)
    Em1=Rm2' * ems + Pv2(i,:)';Em=[Em;Em1'];
    Aa1=Rm1' * aas + Pv1(i,:)';Aa=[Aa;Aa1'];%liggende vectoren
    Ts1=Rm1' * tss + Pv1(i,:)';Ts=[Ts;Ts1'];  
    Ai1=Rm1' * ais + Pv1(i,:)';Ai=[Ai;Ai1'];
    Ac1=Rm1' * acs + Pv1(i,:)';Ac=[Ac;Ac1'];

	 ghsc(i,:)=[Rm1*[Gh1'-Pv1(i,:)]']';
    elsc(i,:)=[Rm1*[El1'-Pv1(i,:)]']';  %scapula receiver stelsel 
    emsc(i,:)=[Rm1*[Em1'-Pv1(i,:)]']';  
    aasc(i,:)=[Rm1*[Aa1'-Pv1(i,:)]']'; 
    tssc(i,:)=[Rm1*[Ts1'-Pv1(i,:)]']'; 
    aisc(i,:)=[Rm1*[Ai1'-Pv1(i,:)]']';
    acsc(i,:)=[Rm1*[Ac1'-Pv1(i,:)]']';

    
    ghhu(i,:)=[Rm2*[Gh1'-Pv2(i,:)]']';
    elhu(i,:)=[Rm2*[El1'-Pv2(i,:)]']';  %humerus receiver stelsel
    emhu(i,:)=[Rm2*[Em1'-Pv2(i,:)]']';  
    aahu(i,:)=[Rm2*[Aa1'-Pv2(i,:)]']'; 
    tshu(i,:)=[Rm2*[Ts1'-Pv2(i,:)]']'; 
    aihu(i,:)=[Rm2*[Ai1'-Pv2(i,:)]']';
    achu(i,:)=[Rm2*[Ac1'-Pv2(i,:)]']';
end;
Rv22(1:9,1:9);
Pv22(1:9,:);
[n,v,s]=iha_rel(Rv22,Rv12,Pv22,Pv12);

matrix=[s,n]; 
tmp0 = find(matrix(:,6)==  0); % nullen eruit
for j=tmp0 ;
   matrix(j,:)=[];
end
[mm,nm]=size(matrix);


[hGH,Pe5]=pivot(matrix(:,4:6),matrix(:,1:3))% GH in hum rec assenstelsel

% alle data naar het scapulaire stelsel (local bone coordinate system)
datas=[];Rm15=[];Rm25=[];Rm5=[];Rv15=[];Rv25=[];Rv5=[];Rm55=[];Rv55=[];Rscaptotaal=[];
 for i=1:m
 	datsc=[ghsc(i,:);emsc(i,:);elsc(i,:);Pv11(i,:);Pv21(i,:);aasc(i,:);tssc(i,:);aisc(i,:);acsc(i,:)];
    [das, Rscap]=scapstegh(datsc);
    Rscaptotaal=[Rscaptotaal;Rscap];
    datas=[datas;das];
 
	%controle R5s moet [1,0,0;0,1,0;0,0,1;] zijn
	[R1s,R2s,R5s]=scrotgh(Rv11(i,:),Rv21(i,:),Rscap);  %rot matr. van scap. en humerus in lok. scap stelsel
 
 	Rm15=[Rm15;R1s];  %rot matr. scapulaire rec in lok. scap stelsel
 	Rm25=[Rm25;R2s];  %rot matr. bovenarm rec in lok. scap stelsel
 	Rm55=[Rm55;R5s];  %niet nodig, controle

	Rv15(i,:)=[reshape(R1s',1,9)];
	Rv25(i,:)=[reshape(R2s',1,9)];
	Rv55(i,:)=[reshape(R5s',1,9)];

	Rm5=[Rm5;Rscap];                    %Rscap (rot matrix van scapulair naar lokaal scap.)in alle standen
	Rv5(i,:)=[reshape(Rscap',1,9)];
end
[ghS,emS, elS, scS, baS, aaS, tsS, aiS, acS]=scapdatgh(datas);    %alles in lokaal scapulair stelsel
[N_IHA5,V_IHA5,S_IHA5]=iha_rel(Rv55,Rv25,aaS,elS);     				%alle assen in lokaal scapulair stelsel
[matrix5, gh5,em5, el5,aa5,ts5,ai5,ac5]=extremgh3(S_IHA5,N_IHA5,ghS,emS,elS,aaS,tsS,aiS,acS); %nullen eruit
[Popt5,Pe5]=pivot(matrix5(:,4:6),matrix5(:,1:3));      				%berekening GH rotatie centrum

matrix15=matrix5(1:2:end,:);
matrix25=matrix5(2:2:end,:);
[Popt15,Pe15]=pivot(matrix15(:,4:6),matrix15(:,1:3));
[Popt25,Pe25]=pivot(matrix25(:,4:6),matrix25(:,1:3));

sGH = Popt5 %GH volgens schroefasmethode in het scapulaire assenstelsel





