function calfunc(option)

% Callback functions for calibration.m
% 05/26/1999 Remco Rotteveel

switch(option)
case 'datdir'
   datdirobj = findobj(gcbf,'Tag','datdir');
   datdir = get(datdirobj,'String');
   datfilesobj = findobj(gcbf,'Tag','datfiles');
   if (~isempty(datdir))
      if (exist(datdir) == 7)
         set(datdirobj,'UserData',[1 1]); setbuttons
         if (datdir(length(datdir)) ~= filesep)
            datdir = [datdir filesep];
            set(gcbo,'String',datdir)
         end
         content = dir([datdir '*.dat']);
         datfiles = {content.name};
         if (isempty(datfiles))
            set(datdirobj,'UserData',[0 1]); setbuttons
            msgbox('The input directory does not contain any DAT files!','Warning','warn')
            set(datfilesobj,'String','')
            calfunc('datfiles')
         else
            datfiles = lower(sort(datfiles));
            set(datfilesobj,'Value',1)
            set(datfilesobj,'String',datfiles)
            calfunc('datfiles')
         end
      else
         set(datdirobj,'UserData',[0 0]); setbuttons
         msgbox('The input directory does not exist!','Error','error')
         set(datfilesobj,'String','')
         calfunc('datfiles')
      end
   else
      set(datdirobj,'UserData',[0 1]); setbuttons
      datfilesobj = findobj(gcbf,'Tag','datfiles');
      set(datfilesobj,'String','')
      calfunc('datfiles')
   end
   
case 'mdir'
   mdirobj = findobj(gcbf,'Tag','mdir');
   mdir = get(mdirobj,'String');
   if (~isempty(mdir))
      if (exist(mdir) == 7)
         set(mdirobj,'UserData',[1 1]); setbuttons
         if (mdir(length(mdir)) ~= filesep)
            mdir = [mdir filesep];
            set(gcbo,'String',mdir)
         end
      else
         set(mdirobj,'UserData',[0 0]); setbuttons
         msgbox('The output directory does not exist!','Error','error')
      end
   else
      set(mdirobj,'UserData',[0 1]); setbuttons
   end
   
case 'datfiles'
   datfilesobj = findobj(gcbf,'Tag','datfiles');
   datfiles = get(datfilesobj,'String');
   selectedidx = get(datfilesobj,'Value');
   if (length(datfiles) == 0)
      mfiles = '';
   else
      if (length(datfiles{1}) ~= 0)
         for i = 1:length(selectedidx)
            datfile = datfiles{selectedidx(i)};
            [path,name] = fileparts(datfile);
            mfile = [name '.m'];
            mfiles{i} = mfile;
         end
      end
   end
   mfilesobj = findobj(gcbf,'Tag','mfiles');
   set(mfilesobj,'String',mfiles);
   
case 'calfile'
   calfileobj = findobj(gcbf,'Tag','calfile');
   calfile = get(calfileobj,'String');
   if (~isempty(calfile))
      if (exist(calfile) == 2)
         set(calfileobj,'UserData',[1 1]); setbuttons
      else
         set(calfileobj,'UserData',[0 0]); setbuttons
         msgbox('The calibration file does not exist!','Error','error')
      end
   else
      set(calfileobj,'UserData',[0 1]); setbuttons
   end
   
case 'selcalfile'
   [file,path] = uigetfile('*.m','Select calibration file');
   if (file ~= 0)
      calfile = [path file];
      calfileobj = findobj(gcbf,'Tag','calfile');
      set(calfileobj,'String',calfile)
      set(calfileobj,'UserData',[1 1]); setbuttons
   else
      calfileobj = findobj(gcbf,'Tag','calfile');
      set(calfileobj,'UserData',[0 1]); setbuttons
   end
   
case 'calibrate'
   datdirobj = findobj(gcbf,'Tag','datdir');
   datdir = get(datdirobj,'String');
   datfilesobj = findobj(gcbf,'Tag','datfiles');
   datfilesidx = get(datfilesobj,'Value');
   datfiles = get(datfilesobj,'String');
   mdirobj = findobj(gcbf,'Tag','mdir');
   mdir = get(mdirobj,'String');
   mfilesobj = findobj(gcbf,'Tag','mfiles');
   mfiles = get(mfilesobj,'String');
   calfileobj = findobj(gcbf,'Tag','calfile');
   calfile = get(calfileobj,'String');
   w = waitbar(0,'Calibrating...');
   waitbar(0)
   try
      for i = 1:length(datfilesidx)
         datfile = [datdir datfiles{datfilesidx(i)}];
         mfile = [mdir mfiles{i}];
         dat2m(datfile,calfile,mfile)
         waitbar(i/length(datfilesidx))
      end
      close(w)
   catch
      msgbox({'An error occurred, please contact your local FoB specialist.',['(' lasterr ')']},'Error','error')
      close(w)
   end
   
case 'savedefs'
   cal = which('calibrate');
   caldir = fileparts(cal);
   datdirobj = findobj(gcbf,'Tag','datdir');
   datdir = get(datdirobj,'String');
   mdirobj = findobj(gcbf,'Tag','mdir');
   mdir = get(mdirobj,'String');
   calfileobj = findobj(gcbf,'Tag','calfile');
   calfile = get(calfileobj,'String');
   defsfile = [caldir filesep 'caldefs'];
   save(defsfile,'datdir','mdir','calfile')
   
case 'loaddefs'
   cal = which('calibrate');
   caldir = fileparts(cal);
   defsfile = [caldir filesep 'caldefs.mat'];
   if (exist(defsfile) == 2)
      load(defsfile)
      datdirobj = findobj(gcbf,'Tag','datdir');
      set(datdirobj,'String',datdir);
      calfunc('datdir')
      mdirobj = findobj(gcbf,'Tag','mdir');
      set(mdirobj,'String',mdir);
      calfunc('mdir')
      calfileobj = findobj(gcbf,'Tag','calfile');
      set(calfileobj,'String',calfile);
      calfunc('calfile')
   end
   setbuttons
   
end

function setbuttons
calbutton = findobj(gcbf,'Tag','calibrate');
defbutton = findobj(gcbf,'Tag','defaults');
datdirobj = findobj(gcbf,'Tag','datdir');
datdir = get(datdirobj,'UserData');
mdirobj = findobj(gcbf,'Tag','mdir');
mdir = get(mdirobj,'UserData');
calfileobj = findobj(gcbf,'Tag','calfile');
calfile = get(calfileobj,'UserData');
status = [datdir; mdir; calfile];
if (status(:,1) == ones(size(status,1),1))
   set(calbutton,'Enable','On')
else
   set(calbutton,'Enable','Off')
end
if (status(:,2) == ones(size(status,1),1))
   set(defbutton,'Enable','On')
else
   set(defbutton,'Enable','Off')
end


