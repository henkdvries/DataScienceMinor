function [gR] = rotbones(AS)

%   function [gR]=rotbones(AS)
%
% program for calculation of bone rotations:
% 
% gR: 3x12 matrices
%     gR(:,1:3): rotations from global to thoracic LCS 
%     gR(:,4:6): rotations from thorax to clavicular LCS
%     gR(:,7:9): rotations from thorax to scapular LCS
%     gR(:,10:12): rotations from thorax to humeral LCS
%     gR(:,13:15): rotations from thorax to forearm LCS
%		 gR(:,16:18): rotations from thorax to hand LCS

[n,m]=size(AS);nDATA = n/3;

for i=1:nDATA
   gR(3*i-2:3*i,1:3)=AS(3*i-2:3*i,1:3);
   Ti = gR(3*i-2:3*i,1:3);
   gR(3*i-2:3*i,4:6)=Ti'*AS(3*i-2:3*i,4:6);
   gR(3*i-2:3*i,7:9)=Ti'*AS(3*i-2:3*i,7:9);
   gR(3*i-2:3*i,10:12)=Ti'*AS(3*i-2:3*i,10:12);
   if (m >= 15)
      gR(3*i-2:3*i,13:15)=Ti'*AS(3*i-2:3*i,13:15);
      %gR(3*i-2:3*i,16:18)=Ti'*AS(3*i-2:3*i,16:18);
   end
end