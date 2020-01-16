function[Sopt,Se]=pivot(V,R);%V= eenheidsrichtingsvectoren, R=steunvectoren
% function[Sopt,Se]=pivot(V,R)
% calculation of the optimal pivot point as published in Woltring (1990)
% In "Biomechanics of Human Movement" (Formia)
% results are correct for elbow flexion and pro/supination
% 8/12/94
%%%%%%%%%%%%%%%%k2%%%%%%%%%%%%%%%%


[m,n]=size(V); 
Q=zeros(3,3);
s=[];
d2=[];

for i=1:m,
  q=[eye(3)-V(i,:)'*V(i,:)];
  s(:,i)=q*R(i,:)'; 
  Q=Q+q;         
end

Q_2=Q/m;
Sopt=inv(Q_2)*mean(s')';


for i=1:m;
 q=[eye(3)-V(i,:)'*V(i,:)];
 d2(:,i)=[Sopt'-R(i,:)]*q*[Sopt'-R(i,:)]';
end

Se=mean(d2');
