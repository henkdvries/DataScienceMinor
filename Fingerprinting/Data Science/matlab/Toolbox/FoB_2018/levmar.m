function [xx,stxx] = levmar(func,xx,DATA)

% Programma voor het schatten van de parametervector xx m.b.v. een kleinste
% kwadraten kriterium, gebruik makend van de Levenberg-Marquardt algoritme
% en de functie 'func' waarmee de functiewaarden met parametervector xx 
% berekend worden. 'func' is een functie van de vorm [e]=func(xx,DATA),
% waarin e de foutvector is.

[mD,nD]=size(DATA);
[mx,nx]=size(xx);
git=0;
alpha = 0.01;
eval(['[e]=' func '(xx,DATA);']);
[me,ne]=size(e);
if (ne > me)
  disp(['error in levmar.m: error-vector e of ' func 'should be columnvector'])
  return
end
SSQ = e'*e;
tol1 = SSQ/100000;
SSQo = SSQ - tol1 - 1;
%
% Gauss-Newton benadering parameters
%
while (abs(SSQo - SSQ) > tol1 & git <= 50),
  for k = 1:max(mx,nx),
    hjxx(k)=max(abs(xx(k)),0.1)*sqrt(eps);
    xx(k) = xx(k) + hjxx(k);
    eval(['[he]=' func '(xx,DATA);']);
    J(1:me,k) = (1/hjxx(k))*(he-e);
    xx(k) = xx(k) - hjxx(k);
  end  
%  Va = (J'*e)/me;
  JTJ = J'*J;
  SSQo=SSQ;
  xxo = xx;
  while SSQ >= SSQo,
    xx=xxo;
    V=(inv(alpha*(diag(diag(JTJ))) + JTJ)/me)*((J'*e)/me);
    xx = xx - V;
    eval(['[ve]=' func '(xx,DATA);']);
    SSQ = ve'*ve;
  %  disp(['first loop; SSQ = ' num2str(SSQ) ])
    alpha = alpha*4;
  end
  alpha = alpha/8;
  fakt = 0.5;
  while (SSQ <= SSQo),
    fakt=fakt*2;
    xx = xx - fakt*V;
    eval(['[fe]=' func '(xx,DATA);']);
    SSQoo = SSQo;
    SSQo = SSQ;
    SSQ = fe'*fe;
  %  disp(['second loop; SSQ = ' num2str(SSQ) ])
  end
  xx = xx + fakt*V;
  git = git + 1;
  eval(['[e]=' func '(xx,DATA);']);
  SSQo = SSQoo;
  SSQ = e'*e;
  %disp(['iteration ' num2str(git) ', SSQ = ' num2str(SSQ)])
end
%
% berekening variantie parameters: Ljung (1987), volgens (9.11)
%
Ephiphiinv = inv((J'*J)/me);
lambdaN = sum(e.^2)/me;
Pn = lambdaN * Ephiphiinv;
stxx = diag(Pn)/me;
