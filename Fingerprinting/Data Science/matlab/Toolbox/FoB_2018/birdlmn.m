function e=birdlmn(xx,DATA)

%gewijzigd 16-04-98 voor gebruik met nieuwe styllen, in mm en 3 kolommen

[m,n]=size(DATA);

e=zeros(m,1);

%parameters
V=xx(1:3);
AA=xx(4:6);

%for j=1:m/4
%i=j*3;
%O=DATA((i-2):i,1);
%R=DATA((i-2):i,2:4);
%e((i-2):i,1)=-AA+R*(O+V);
%end;

for j=1:m/4
   i=j*4-3;
   O=DATA(i,1:3)';
   R=DATA(i+1:i+3,1:3)';
   e((j-1)*3+1:(j-1)*3+3)=-AA+(O+R*V);
%e1((j-1)*3+1:(j-1)*3+3)=-AA+(O+R*V);
end
%e2=[0 0 0 0 0 0 0 0];
%e=[e1,e2]';

mean(abs(e));
%plot(e)