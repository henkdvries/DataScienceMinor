function gh=ghestnew(pc,ac,aa,ts,ai)

% GHESTNEW. Calculates GH from regression equations 
% according to Meskers et al 1997. juli 1996. C. Meskers.

%disp(['Warning in ghestnew: data must be provided in millimeters!!'])

Rsca=asscap96(ac,ts,ai);
Osca=(ac);

pc=Rsca'*(pc-Osca);
ac=Rsca'*(ac-Osca);
aa=Rsca'*(aa-Osca);
ts=Rsca'*(ts-Osca);
ai=Rsca'*(ai-Osca);

lacaa=norm(ac-aa);
ltspc=norm(ts-pc);
laiaa=norm(ai-aa);
lacpc=norm(ac-pc);

scx=[1 pc(1) ai(1) laiaa pc(2)]';
scy=[1 lacpc pc(2) lacaa ai(1) ]';
scz=[1 pc(2) pc(3) ltspc ]'; 


thx=[18.9743    0.2434    0.2341    0.1590    0.0558];
thy=[-3.8791   -0.1002    0.1732   -0.3940    0.1205];
thz=[9.2629   -0.2403    1.0255    0.1720];
%previous version: thz=[ 9.2629   -0.2403    1.0255    0.1720];


GHx = thx*scx;
GHy = thy*scy;
GHz = thz*scz;

gh=[GHx;GHy;GHz];

gh=(Rsca*gh)+Osca;
