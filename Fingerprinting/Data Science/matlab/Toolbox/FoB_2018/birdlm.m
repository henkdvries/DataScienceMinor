function e=birdlm(xx,DATA)

[m,n]=size(DATA);

%parameters
V=xx(1:3);
AA=xx(4:6);

for j=1:m/4
 i=j*4-3;
 O=DATA(i,2:4)';
 R=DATA(i+1:i+3,2:4)';
 e((j-1)*3+1:(j-1)*3+3)=-AA+(O+R*V);
end

e = e';
mean(abs(e));
%plot(e)