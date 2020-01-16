function[matrix, gh, em, el, aa, ts, ai, ac]=extremgh3(S_IHAx,N_IHAx,ghx,emx,elx,aax,tsx,aix,acx);

matrix=[];em=[];el=[];aa=[];ts=[];ai=[];gh=[];ac=[];
matrix=[S_IHAx,N_IHAx]; %pos, rich

tmp0 = find(matrix(:,6)==  0);
for j=tmp0 ;
   matrix(j,:)=[];
   elx(j,:)=[];
   emx(j,:)=[];
   aax(j,:)=[];
   tsx(j,:)=[];
   aix(j,:)=[];
   ghx(j,:)=[];
   acx(j,:)=[];
end;

em=emx; el=elx; aa=aax; ts=tsx; ai=aix; gh=ghx; ac=acx;
