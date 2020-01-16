function [jR] = rotjoint(AS)

%   function [jR]=rotjoint(AS)
%
% program for calculation of bone rotations:
% 
% jR: 3x12 matrices
%     jR(:,1:3): rotations from global to thoracic LCS 
%     jR(:,4:6): rotations from thoracic to clavicular LCS
%     jR(:,7:9): rotations from clavicular to scapular LCS
%     jR(:,10:12): rotations from scapular to humeral LCS
%     jR(:,13:15): rotations from humeral to forearm LCS
%
% 06/11/1999 Remco Rotteveel

[n,m]=size(AS);nDATA = n/3;

%jR(1:n,1:3) = AS(:,1:3);
%
%for i=1:nDATA
%   jR(3*i-2:3*i,4:6)=AS(3*i-2:3*i,1:3)'*AS(3*i-2:3*i,4:6);
%   jR(3*i-2:3*i,7:9)=AS(3*i-2:3*i,4:6)'*AS(3*i-2:3*i,7:9);
%   jR(3*i-2:3*i,10:12)=AS(3*i-2:3*i,7:9)'*AS(3*i-2:3*i,10:12);
%   if (m == 15)
%      jR(3*i-2:3*i,13:15)=AS(3*i-2:3*i,10:12)'*AS(3*i-2:3*i,13:15);
%   end
%end

T0 = AS(1:3,1:3); % initial thorax orientation

for i=1:nDATA
   jR(3*i-2:3*i,1:3)=T0'*AS(3*i-2:3*i,1:3);
   jR(3*i-2:3*i,4:6)=AS(3*i-2:3*i,1:3)'*AS(3*i-2:3*i,4:6);
   jR(3*i-2:3*i,7:9)=AS(3*i-2:3*i,4:6)'*AS(3*i-2:3*i,7:9);
   jR(3*i-2:3*i,10:12)=AS(3*i-2:3*i,7:9)'*AS(3*i-2:3*i,10:12);
   if (m == 15)
      jR(3*i-2:3*i,13:15)=AS(3*i-2:3*i,10:12)'*AS(3*i-2:3*i,13:15);
   end
end
