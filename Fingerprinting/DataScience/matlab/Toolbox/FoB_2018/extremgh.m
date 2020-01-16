function[matrix, gh, em, el]=extremgh(S_IHAx,N_IHAx,ghx, emx,elx);

matrix=[];em=[];el=[];gh=[];
matrix=[S_IHAx,N_IHAx]; %pos, rich

tmp0 = find(matrix(:,6)==  0);
for j=tmp0 ;
   matrix(j,:)=[];
   elx(j,:)=[];
   emx(j,:)=[];
   ghx(j,:)=[];
end;
em=emx; el=elx; gh=ghx;
