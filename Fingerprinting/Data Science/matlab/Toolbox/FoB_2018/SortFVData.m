function[DATA]=SortFVData(data)
% [DATA]=SortFVData(data)
% Data in FoBVis are not sorted by sensor
% This program sorts the data for each observation
% INPUT:  data in mm
% OUTPUT: file: DATA in mm

sensors=[min(data(:,1)),max(data(:,1))];
n=(sensors(2)-sensors(1)+1)*4;
N=size(data,1)/n;

DATA=[];
for i=1:N
    Nm1=(i-1)*n;
    x=data(Nm1+1:Nm1+n,:);
    order=x(1:4:end,1);
    [on,I]=sort(order);
    
    for j=1:size(I)
        jm1=(j-1)*4;
        im1=(I(j)-1)*4;
        y(jm1+1:jm1+4,:)=x(im1+1:im1+4,:);
    end
    DATA=[DATA;y];
end
DATA(1:4:end,2:4)=DATA(1:4:end,2:4); %decimal error in FoBVis
