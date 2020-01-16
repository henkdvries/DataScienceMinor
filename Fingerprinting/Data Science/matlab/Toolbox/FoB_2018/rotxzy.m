  function [x,z,y]=rotxzy(R)
% programma voor het berekenen van de rotaties x,z, en y resp. rond de X-, 
% z- en y-as uit de gegeven matrix R
z1 = asin(-R(1,2));
sx = R(3,2)/cos(z1);
cx = R(2,2)/cos(z1);
x1 = atan2(sx,cx);
sy = R(1,3)/cos(z1);
cy = R(1,1)/cos(z1);
y1 = atan2(sy,cy);
if z1 >= 0,
   z2 = pi - z1;
else
   z2 = -pi - z1;
end
sx = R(3,2)/cos(z2);
cx = R(2,2)/cos(z2);
x2 = atan2(sx,cx);
sy = R(1,3)/cos(z2);
cy = R(1,1)/cos(z2);
y2 = atan2(sy,cy);
if (-pi/2 <= z1 & z1 <= pi/2)
  y=y1;
  z=z1;
  x=x1;
else
  y=y2;
  z=z2;
  x=x2;
end
