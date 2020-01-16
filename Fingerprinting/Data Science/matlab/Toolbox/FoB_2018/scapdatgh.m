function[ghh,emh, elh, sch, bah, aah, tsh, aih, ach]=scapdatgh(datah);

[m,n]=size(datah); %(9*m) x 3 matrix

for i=1:m/9
 ghh(i,:)=datah(-8+9*i,:);  
 emh(i,:)=datah(-7+9*i,:);
 elh(i,:)=datah(-6+9*i,:);
 sch(i,:)=datah(-5+9*i,:);
 bah(i,:)=datah(-4+9*i,:);
 aah(i,:)=datah(-3+9*i,:);
 tsh(i,:)=datah(-2+9*i,:);
 aih(i,:)=datah(-1+9*i,:);
 ach(i,:)=datah(9*i,:);
end