function rot2vrml(allIJ,jR,ELx,PSy,file)

% function vrml = rot2vrml(jR)
%
% This function converts rotation matrices to quaternions
% (combined rotation axis and angle) for use in VRML.

for i = 1:3:size(jR,1)								% for every position
   for j = 1:3:12										% and for every joint
      R = jR(i:i+2,j:j+2);							% get rotation matrix
      e4 = sqrt((trace(R) + 1) / 4);			% 4th Euler parameter
      e1 = (R(3,2) - R(2,3)) / (4 * e4);		% 1st Euler parameter
      e2 = (R(1,3) - R(3,1)) / (4 * e4);		% 2nd Euler parameter
      e3 = (R(2,1) - R(1,2)) / (4 * e4);		% 3rd Euler parameter
      phi = 2 * acos(e4);							% rotation angle
%      if (phi > pi / 2)
%         phi = pi - phi;
%      end
      if (phi ~= 0)
         lambda1 = e1 / sin(phi / 2);			% 1st coordinate of rotation axis
         lambda2 = e2 / sin(phi / 2);			% 2nd coordinate of rotation axis
         lambda3 = e3 / sin(phi / 2);			% 3rd coordinate of rotation axis
      else
         lambda1 = 0;
         lambda2 = 0;
         lambda3 = 0;
      end
      
      vrml((i+2)/3,(4*j-1)/3:((4*j-1)/3)+3) = [lambda1 lambda2 lambda3 phi];
   end
end

ulna_ax = [0.9916 0.0486 -0.1234];				% rotation axis ulna
radius_ax = [-0.1222 0.9924 0.0129];			% rotation axis radius
for i = 1:size(vrml,1)								% put axis and rotation in one matrix
   ulna_rot(i,1:4) = [ulna_ax ELx(i)];			% :
   radius_rot(i,1:4) = [radius_ax PSy(i)];	% :
end														% :

names = {'IJ_pos','IJ_rot','SC_rot','AC_rot','GH_rot','EL_rot','PS_rot'};
values = {allIJ,vrml(:,1:4),vrml(:,5:8),vrml(:,9:12),vrml(:,13:16),ulna_rot,radius_rot};
key = (0:1/(size(vrml,1)-1):1)';

[wrlpath,wrlfile] = fileparts(file);
wrl = fopen([wrlpath filesep wrlfile '.wrl'],'w');

fprintf(wrl,'%c','#VRML V2.0 utf8');
fprintf(wrl,'%c\n\n',' ');

for i = 1:length(names)
   if (size(values{i},2) == 3)
      node = 'PositionInterpolator';
      eventType = 'SFVec3f';
      format = '%6.6f %6.6f %6.6f\n';
   end
   if (size(values{i},2) == 4)
      node = 'OrientationInterpolator';
      eventType = 'SFRotation';
      format = '%6.6f %6.6f %6.6f %6.6f\n';
   end
   fprintf(wrl,'%c',['DEF ' names{i} ' ' node ' {']);
   fprintf(wrl,'%c\n',' ');
   fprintf(wrl,'%c','key [');
   fprintf(wrl,'%c\n',' ');
   fprintf(wrl,'%6.6f\n',key);
   fprintf(wrl,'%c\n',']');
   fprintf(wrl,'%c','keyValue [');
   fprintf(wrl,'%c\n',' ');
   fprintf(wrl,format,values{i}');
   fprintf(wrl,'%c',']}');
   fprintf(wrl,'%c\n\n',' ');
end

fclose(wrl);