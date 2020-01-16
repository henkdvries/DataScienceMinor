function[Cn,ROTr,ROTg]=axclav(C,S)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 02-08-91 %%
%                                                                       %
%  In de functie axclav wordt uit de positie matrices van clavicula en  %
%  scapula de axiale rotatie van de clavicula geschat en de nieuwe      %
%  positie matrix van de clavicula.                                     %
%                                                                       %
%       input : C (originele positiematrix van de clavicula)            %
%               S (positiematrix van de scapula)                        %
%       output: Cn (nieuwe positiematrix van de clavicula)              %
%               rot (rotaties van de clavicula rond de lokale assen)    %
%                                                                       %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Ruststand van clavicula en scapula:
  Co = C(1:3,1:3); So = S(1:3,1:3);

% Relatie clavicula-scapula in ruststand:
  Mp = Co'*So;

% Bepalen van de rotaties van de clavicula rond de lokale assen t.o.v.
% thorax LCS:

[n,m]=size(C);nDATA = n/3;

r=[];
for i=1:nDATA
  Rc=Co'*C(3*i-2:3*i,1:3);
  r = [r;Rc];
end  

% r = rot2a(C,0);

% Bepalen van de eulerrotaties (y,z,x):
  [ROTg]=roteuler(r,3);
  [ROTr]=ROTg*(pi/180);
  [rij,kolom]=size(ROTr);

  BETA = ROTr(:,1); GAMMA = ROTr(:,2); ALPHA = ROTr(:,3);

for I=1:rij
  beta=BETA(I);gamma=GAMMA(I);          % Benodigde hoeken
  RS  = S(I*3-2:I*3,1:3);                 % Scapula stand i
%____________________________________________________________________

% (Berekening van axiale rotatie volgens axrot (vd Helm))
 
    Ma = Co*roty(beta)*rotz(gamma);
    alpha=0;
    Sposd = Ma*rotx(alpha)*Mp;
    Spos=RS;
    Emat = Sposd'*Spos;
    E = acos(Emat(1,1)) + acos(Emat(2,2)) + acos(Emat(3,3));
    SSQ = E*E;
    SSQo = 0;
    while abs(SSQ-SSQo)>0.001,
      dalpha = max(0.1,alpha)*sqrt(eps);
      Sposdd = Ma*rotx(alpha + dalpha)*Mp;
      Ematd = Sposdd'*Spos;
      Ed = acos(Ematd(1,1)) + acos(Ematd(2,2)) + acos(Ematd(3,3));
      dEdalpha = (Ed - E)/dalpha;
      V = E/dEdalpha;
      d=2;
      alpha0=alpha;
      SSQo = SSQ;
      while (SSQo <= SSQ) & ((abs(SSQo - SSQ) > 0.001)|(d==2)),
	d = d/2;
	alpha1 = alpha0 - d*V;
	Sposd = Ma*rotx(alpha1)*Mp;
	Emat = Sposd'*Spos;
	E = acos(Emat(1,1)) + acos(Emat(2,2)) + acos(Emat(3,3));
	SSQ=E*E;
      end
      alpha=alpha1;

    end
%[I,alpha]
%pause
%____________________________________________________________________

    ALPHA(I) = alpha; 
end

  ROTr(1:rij,3)=ALPHA;
  ROTg(1:rij,3)=ALPHA*180/pi;

% Berekenen van de nieuwe positiematrix van de clavicula :
% (volgens Ci = Co * R waarbij R = (roty*rotz*rotx)

for I=1:rij
  Ry = roty(BETA(I));
  Rz = rotz(GAMMA(I));
  Rx = rotx(ALPHA(I));
  Cn(I*3-2:I*3,1:3) = Co*Ry*Rz*Rx;

end

