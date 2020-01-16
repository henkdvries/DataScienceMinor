function[ANGg] = roteulern(R,EP)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% function[ANGg] = roteulern(R,EP)                                         %
%                                                                           %
% Deze functie heeft de matrix R als input, waarin een aantal afzonderlijke %
% rotatiematrices zijn weergegeven.                                         %
% De rotatiematrices worden ontleed in de eulerhoeken rond de globale       %
% assen                                                                     %
% alpha : eerste rotatie                                                    %
% beta  : tweede rotatie                                                    %
% gamma : derde rotatie                                                     %
%                                                                           %
% De eulerparameter EP wordt gebruikt om de volgorde van de rotaties aan te %
% geven:     EP:         ROTATIEVOLGORDE:                                   %
%             1          XYZ    (thor)                                      %
%             2          XZY                                                %
%             3          YZX    (clav,scap)                                 %
%             4          ZYX                                                %
%             5          ZXY                                                %
%             6          YZY    (hum)                                       %
%             7          YXZ    (hand)                                      %
%                                                                           %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ALPHA = [];
BETA = [];
GAMMA = [];

[m,n]=size(R);

% Aantal rotatiematrices
NMAT = m/3;

% Inlezen van de k-de rotatiematrix 

for K = 1:NMAT

  Rk = R(3*K-2:3*K,1:3);

% Bepalen van eulerhoeken alpha,beta,gamma.

  if EP==1,
    [alpha,beta,gamma] = rotxyz(Rk);
  end

  if EP==2,
    [alpha,beta,gamma] = rotxzy(Rk);
  end

  if EP==3,
    [alpha,beta,gamma] = rotyzx(Rk);
  end

  if EP==4,
    [alpha,beta,gamma] = rotzyx(Rk);
  end

  if EP==5,
    [alpha,beta,gamma] = rotzxy(Rk);
  end

  if EP==6,
    [alpha,beta,gamma] = rotyzy(Rk);
  end

  if EP==7,
    [alpha,beta,gamma] = rotyxz(Rk);
  end

  ALPHA = [ALPHA;alpha];
  BETA  = [BETA; beta ];
  GAMMA = [GAMMA;gamma];

end

ANGr = [ALPHA,BETA,GAMMA];
ANGg = ANGr*(180/pi);

