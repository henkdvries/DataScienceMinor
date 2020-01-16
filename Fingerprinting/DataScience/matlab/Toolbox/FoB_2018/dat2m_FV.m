function dat2m_FV(datfile,calfile,mfile,add_flag)  

% Program for converting files birdframe (level 1-4, point 1-156) 
% from bird output data to matlab position/rotation matrix
% 
% Input: raw Bird output format (mm, .txt)
% Output: Position/Rotation matrix in matlab format (centimeters, .m)
% 
% x  y y y     x  y y y 
%    z z z     x  z z z
%    z z z     x  z z z 
%    z z z     x  z z z
%          =>  q  y y y
% q  y y y     q  z z z  
%    z z z     q  z z z 
%    z z z     q  z z z
%    z z z
%
%  27-10-1995   Carel Meskers
%  23-03-1998   Marielle & Jochem
%  09/22/1999   Remco Rotteveel
%  02/11/2010   Jurriaan de Groot (adjustment for FoBViS data)
%   Input uit FoBVis in mm ipv inch!
%   Output in cm!
%   add dummy data for not recorded sensors

disp('start dat2m_fv.m')
inch = 25.4; %inch 2 mm
% datfile
% calfile
% mfile

data = [];
datfileid = fopen(datfile);										% open data file
while 1
   line = fgetl(datfileid);										% read line
   if (~isempty(line))												% if line is not empty
      if (line == -1)												% if not EOF
         break
      else
         if (~isempty(sscanf(line(1),'%d')))					% if first character is a number
            receiver = sscanf(line(1),'%d');					% then receiver is that number
         end
         dataline = sscanf(line(2:length(line)),'%f %f %f')';	% convert data to floating point
         data = [data; receiver dataline];					% put data in matrix
      end
%       disp('dat2m_FV.m'),pause
   end
end
fclose(datfileid);													% close data file


% FobVis Input gelijk maken aan Fob input
% Rotatiematrices van FoBVis transponeren
n=size(data,1)/4;
for i=1:n
    im1=(i-1)*4;
    p=data(im1+1,2:4);
    data(im1+1,2:4)=p/inch;
    r=data(im1+2:im1+4,2:4);
    data(im1+2:im1+4,2:4)=r';
end


for i=1:4:size(data,1)												% convert positions
  data(i,2:4) = data(i,2:4) * inch;			    					% from inches
end																	% to millimeters

[caldir,calname] = fileparts(calfile);
[vardir,varname] = fileparts(mfile);

mfileid = fopen(mfile,'w');										% open .m file for write
fprintf(mfileid,'%% Calibrated with %s\n',calname);
fprintf(mfileid,'%% Positions are in centimeters\n');           % 30 oktober 2000 veranderd
fprintf(mfileid,'%s =[\n','Data');

old = pwd;																% read in the calibration file
cd(caldir);																%
eval(['th_nonlin = ' calname ';'])								%
cd(old);																	%

k = 0;																	% create regressors for calibration
for i = 1:4:size(data,1)											%
   k = k + 1;															%
   reg(k,1:3) = data(i,2:4);										%
   [reg(k,4),reg(k,5),reg(k,6)] = rotxyz(data(i+1:i+3,2:4)');
end																		%

if (size(th_nonlin,1) == 10)										% old calibration procedure
% IN OLD PROCEDURE: PAS OP CALIBRATIE MOET IN INCHES ZIJN!!!
   reg(:,1:3) = reg(:,1:3) / inch;								    % conversion mm to inch
   T = [ones(size(reg,1),1) reg(:,1:3) reg(:,1:3).^2 reg(:,1).*reg(:,2) reg(:,1).*reg(:,3) reg(:,2).*reg(:,3)];
   error = T * th_nonlin;											%
   for i = 1:4:size(data,1)										    %
      data(i,2:4) = (data(i,2:4) + error((i-1)/4+1,:) * inch) / 10; % conversion inch to cm
   end																%
   
elseif (size(th_nonlin,1) == 29)									% new calibration procedure
% IN NEW PROCEDURE: CALIBRATIE IN MM? Jurriaan 2010-02-15
   T_cross = [];													%
   for i=1:6														%
      for j=i:6														%
         T_cross = [T_cross reg(:,i).*reg(:,j)];                    %
      end															%
   end																%
   af = sqrt(reg(:,1).^2+reg(:,2).^2+reg(:,3).^2);                  %
   T = [ones(size(reg,1),1) reg(:,1:3) af reg(:,4:6) T_cross];
   error = T * th_nonlin;											%
   for i = 1:4:size(data,1)                                         %
      data(i,2:4) = (data(i,2:4) + error((i-1)/4+1,:))/10;          %conversion mm to cm
   end																%
else
   msgbox('Calibration file format unknown!','Error','error')
end

if add_flag==1            % Add not recorded sensors in fobvis to *IM.m (2010-02-17  Jurriaan)
    [data]=AddSens2BL_FV(data);
end

[DATA]=SortFVData(data);    %2010-02-17  Jurriaan

fprintf(mfileid,'%2d %9.3f %9.3f %9.3f\n',DATA');               	% write data to mfile
fprintf(mfileid,'];');
fclose(mfileid);
disp('end dat2m_fv.m')
