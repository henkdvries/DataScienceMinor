function folders = iterfolder(mydir)
% If folder is not defined select current folder
if nargin == 0
  mydir = pwd;
end
% Get a list of all files and folders in this folder.
files = dir(mydir)
% Get a logical vector that tells which is a directory.
dirFlags = [files.isdir]
% Extract only those that are directories.
subFolders = files(dirFlags)
% Print folder names to command window.
folders = {};

% Loops through folder array
% TODO: Fixing parent folder 
for k = 1 : length(subFolders)
    % Appends path to folder array
    % combining path and filename
    if strcmp(subFolders(k).name, '.') || strcmp(subFolders(k).name, '..')
   
    else 
        folders = [folders, fullfile(subFolders(k).folder, subFolders(k).name)];  
    end  
end