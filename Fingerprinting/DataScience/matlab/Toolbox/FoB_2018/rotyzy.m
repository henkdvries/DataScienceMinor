      function [y,z,ya]=rotyzy(r)
%
%     programma voor het berekenen van de rotaties rond achtereenvolgens
%     de y-, z- en lokale y-as uit de rotatiematrix r. er zijn twee 
%     oplossingen: de oplossing met de kleinste rotaties wordt uitgekozen.
%
z1 = acos(r(2,2));
if (z1==0)
    y=acos(r(1,1));
    z=z1;
    ya=0.0;
    return
end
sy = r(3,2)/sin(z1);
cy = -r(1,2)/sin(z1);
y1 = atan2(sy,cy);
sya = r(2,3)/sin(z1);
cya = r(2,1)/sin(z1);
ya1 = atan2(sya,cya);

z2 = -z1;
sy = r(3,2)/sin(z2);
cy = -r(1,2)/sin(z2);
y2 = atan2(sy,cy);
sya = r(2,3)/sin(z2);
cya = r(2,1)/sin(z2);
ya2 = atan2(sya,cya);

%if (0 <= z1 & z1 <= pi)
if abs(z1 <= pi)
    y = y1;
    z = z1;
    ya = ya1;
else
    y = y2;
    z = z2;
    ya = ya2;
end

check_flag=0;
if check_flag==1
    r1=roty(y)*rotz(z)*roty(ya);
    
    if max(r-r1) > 1e-5
        disp('WARNING function rotyzy.m: INPUT MATRIX AND OUTPUT ANGLES DO NOT MATCH')
        r,r1,d=r-r1
        pause
        disp('return')
    end
    plot_flag=0;
    if plot_flag==1
        figure(999) 
        plot(y*180/pi,3,'.b'),hold on
        plot(z*180/pi,2,'.r')
        plot(ya*180/pi,1,'.g')
        set(gca,'ylim',[0,5])
    end
end