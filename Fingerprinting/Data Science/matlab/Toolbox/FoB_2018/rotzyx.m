   function [z,y,x]=rotzyx(R)
% programma voor het berekenen van de rotaties z,y,x resp. rond de Z-, y-
% en x-as.
y1 = asin(-R(3,1));
sx = R(3,2)/cos(y1);
cx = R(3,3)/cos(y1);
x1 = atan2(sx,cx);
sz = R(2,1)/cos(y1);
cz = R(1,1)/cos(y1);
z1 = atan2(sz,cz);
if y1 >= 0
  y2 = pi - y1;
else
  y2 = -pi - y1;
end
sx = R(3,2)/cos(y2);
cx = R(3,3)/cos(y2);
x2 = atan2(sx,cx);
sz = R(2,1)/cos(y2);
cz = R(1,1)/cos(y2);
z2 = atan2(sz,cz);
if (-pi/2 <= y1 & y1 <= pi/2)
  y=y1;
  z=z1;
  x=x1;
else
  y=y2;
  z=z2;
  x=x2;
end
