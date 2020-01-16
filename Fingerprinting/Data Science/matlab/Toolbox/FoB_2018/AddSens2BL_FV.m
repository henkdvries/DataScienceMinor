function[BL]=AddSens2BL_FV(data)
%[BL]=AddSens2BL_FV(data)
% Supplement BonyLandmark records in FoBVis to full sensor series
% Input 
%   calibrated bony landmark recordings

Xdummy=[0 0 0];
Rdummy=diag(ones(3,1));
XR=[Xdummy;Rdummy];
BL=[];

bl=[ones(4,1)*2,[XR]
    ones(4,1)*3,[XR]
    ones(4,1)*4,[XR]
    ones(4,1)*5,[XR]
    ones(4,1)*6,[XR]
    ones(4,1)*7,[XR]
    ones(4,1)*8,[XR]
    ones(4,1)*9,[XR]];

N=size(data)/8;    
for i=1:N
    im1=(i-1)*8;
    X=data(im1+1:im1+8,:);
    Y=bl;
    
    xm1=(X(1,1)-2)*4;
    Y(xm1+1:xm1+4,:)=X(1:4,:);
    xm1=(X(5,1)-2)*4;
    Y(xm1+1:xm1+4,:)=X(5:8,:);
    BL=[BL;Y];
end