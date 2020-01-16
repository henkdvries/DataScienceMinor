function convfunc(option,varargin)

% Callback functions for convert.m
% 05/26/1999 Remco Rotteveel

switch(option)
case 'datadir'
   datadirobj = findobj(gcbf,'Tag','datadir');
   datadir = get(datadirobj,'String');
   datafilesobj = findobj(gcbf,'Tag','datafiles');
   if (~isempty(datadir))
      if (exist(datadir) == 7)
         set(datadirobj,'UserData',[1 1]); setbuttons
         if (datadir(length(datadir)) ~= filesep)
            datadir = [datadir filesep];
            set(gcbo,'String',datadir)
         end
         content = dir([datadir '*.m']);
         datafiles = {content.name};
         if (isempty(datafiles))
            set(datadirobj,'UserData',[0 1]); setbuttons
            msgbox('The input directory does not contain any M files!','Warning','warn')
            set(datafilesobj,'String','')
            convfunc('datafiles')
         else
            datafiles = lower(sort(datafiles));
            set(datafilesobj,'Value',1)
            set(datafilesobj,'String',datafiles)
            convfunc('datafiles')
         end
      else
         set(datadirobj,'UserData',[0 0]); setbuttons
         msgbox('The input directory does not exist!','Error','error')
         set(datafilesobj,'String','')
         convfunc('datafiles')
      end
   else
      set(datadirobj,'UserData',[0 1]); setbuttons
      datafilesobj = findobj(gcbf,'Tag','datafiles');
      set(datafilesobj,'String','')
      convfunc('datafiles')
   end
   
case 'inpdir'
   inpdirobj = findobj(gcbf,'Tag','inpdir');
   inpdir = get(inpdirobj,'String');
   if (~isempty(inpdir))
      if (exist(inpdir) == 7)
         set(inpdirobj,'UserData',[1 1]); setbuttons
         if (inpdir(length(inpdir)) ~= filesep)
            inpdir = [inpdir filesep];
            set(gcbo,'String',inpdir)
         end
      else
         set(inpdirobj,'UserData',[0 0]); setbuttons
         msgbox('The output directory does not exist!','Error','error')
      end
   else
      set(inpdirobj,'UserData',[0 1]); setbuttons
   end
   
case 'vrmldir'
   vrmldirobj = findobj(gcbf,'Tag','vrmldir');
   vrmldir = get(vrmldirobj,'String');
   if (~isempty(vrmldir))
      if (exist(vrmldir) == 7)
         set(vrmldirobj,'UserData',[1 1]); setbuttons
         if (vrmldir(length(vrmldir)) ~= filesep)
            vrmldir = [vrmldir filesep];
            set(gcbo,'String',vrmldir)
         end
      else
         set(vrmldirobj,'UserData',[0 0]); setbuttons
         msgbox('The VRML directory does not exist!','Error','error')
      end
   else
      set(vrmldirobj,'UserData',[0 1]); setbuttons
   end
   
case 'datafiles'
   datafilesobj = findobj(gcbf,'Tag','datafiles');
   datafiles = get(datafilesobj,'String');
   selectedidx = get(datafilesobj,'Value');
   if (length(datafiles) == 0)
      inpfiles = '';
   else
      if (length(datafiles{1}) ~= 0)
         for i = 1:length(selectedidx)
            datafile = datafiles{selectedidx(i)};
            [path,name] = fileparts(datafile);
            inpfile = [name '.inp'];
            inpfiles{i} = inpfile;
         end
      end
   end
   inpfilesobj = findobj(gcbf,'Tag','inpfiles');
   set(inpfilesobj,'String',inpfiles);
   
case 'side'
   side = get(gcbo,'Tag');
   value = get(gcbo,'Value');
   if (value == 1)
      switch(side)
      case 'left'
         rightobj = findobj(gcbf,'Tag','right');
         set(rightobj,'Value',0)
      case 'right'
         leftobj = findobj(gcbf,'Tag','left');
         set(leftobj,'Value',0)
      end
   else
      set(gcbo,'Value',1)
   end
   
case 'gh'
   gh = get(gcbo,'Tag');
   value = get(gcbo,'Value');
   mov1obj = findobj(gcbf,'Tag','mov1file');
   mov2obj = findobj(gcbf,'Tag','mov2file');
   mov3obj = findobj(gcbf,'Tag','mov3file');
   mov1but = findobj(gcbf,'Tag','selmov1file');
   mov2but = findobj(gcbf,'Tag','selmov2file');
   mov3but = findobj(gcbf,'Tag','selmov3file');
   if (value == 1)
      switch(gh)
      case 'gh-screw'
         regressobj = findobj(gcbf,'Tag','gh-regress');
         screwobj = findobj(gcbf,'Tag','gh-screw');
         set(regressobj,'Value',0)
         movdata = get(screwobj,'UserData');
         set(mov1obj,'Enable','on','BackgroundColor',[1 1 1])
         set(mov2obj,'Enable','on','BackgroundColor',[1 1 1])
         set(mov3obj,'Enable','on','BackgroundColor',[1 1 1])
         set(mov1but,'Enable','on')
         set(mov2but,'Enable','on')
         set(mov3but,'Enable','on')
         if (~isempty(movdata))
            set(mov1obj,'UserData',movdata{1}); setbuttons       
            set(mov2obj,'UserData',movdata{2}); setbuttons
            set(mov3obj,'UserData',movdata{3}); setbuttons
         end
         
      case 'gh-regress'
         screwobj = findobj(gcbf,'Tag','gh-screw');
         set(screwobj,'Value',0)
         mov1data = get(mov1obj,'UserData');
         mov2data = get(mov2obj,'UserData');
         mov3data = get(mov3obj,'UserData');
         set(screwobj,'UserData',{mov1data, mov2data, mov3data})
         set(mov1obj,'Enable','off','BackgroundColor',[0.9 0.9 0.9],'UserData',[1 1]); setbuttons         
         set(mov2obj,'Enable','off','BackgroundColor',[0.9 0.9 0.9],'UserData',[1 1]); setbuttons         
         set(mov3obj,'Enable','off','BackgroundColor',[0.9 0.9 0.9],'UserData',[1 1]); setbuttons
         set(mov1but,'Enable','off')
         set(mov2but,'Enable','off')
         set(mov3but,'Enable','off')
      end
   else
      set(gcbo,'Value',1)
   end
   
case 'checkfile'
   datadirobj = findobj(gcbf,'Tag','datadir');
   datadir = get(datadirobj,'String');
   if (isempty(datadir))
      msgbox('You must first specify a data directory!','Error','error')
   else
      file = get(gcbo,'String');
      if (~isempty(file))
         file = [datadir file];
         if (exist(file) == 2)
            set(gcbo,'UserData',[1 1]); setbuttons
         else
            set(gcbo,'UserData',[0 1]); setbuttons
            msgbox('The specified M file does not exist in the data directory!','Error','error')
         end
      end
   end
   
case 'selectfile'
   tag = varargin{1};
   boxtitle = varargin{2};
   datadirobj = findobj(gcbf,'Tag','datadir');
   datadir = get(datadirobj,'String');
   if (isempty(datadir))
      msgbox('You must first specify a data directory!','Error','error')
   else
      obj = findobj(gcbf,'Tag',tag);
      file = uigetfile([datadir '*.m'],boxtitle);
      if (file ~= 0)
         set(obj,'String',file)
         set(obj,'UserData',[1 1]); setbuttons
      else
         set(obj,'UserData',[0 1]); setbuttons
      end
   end
   
case 'receiver'
   tag = varargin{1};
   recobj = findobj(gcbf,'Tag',tag);
   rec = get(recobj,'String');
   if (~isempty(rec))
      set(recobj,'UserData',[1 1]); setbuttons
   else
      set(recobj,'UserData',[0 1]); setbuttons
   end
   
case 'stylfile'
   stylfileobj = findobj(gcbf,'Tag','stylfile');
   stylfile = get(stylfileobj,'String');
   if (~isempty(stylfile))
      if (exist(stylfile) == 2)
         set(stylfileobj,'UserData',[1 1]); setbuttons
      else
         set(stylfileobj,'UserData',[0 0]); setbuttons
         msgbox('The specified M file does not exist in the MATLAB path!','Error','error')
      end
   else
      set(stylfileobj,'UserData',[0 1]); setbuttons
   end
   
case 'mm'
   mmobj = findobj(gcbf,'Tag','mm');
   mm = get(mmobj,'String');
   if (~isempty(mm))
      set(mmobj,'UserData',[1 1]); setbuttons
   else
      set(mmobj,'UserData',[0 1]); setbuttons
   end
   
case 'selstylfile'
   stylfile = uigetfile('*.m','Select stylus file');
   if (stylfile ~= 0)
      if (exist(stylfile) == 2)
         stylfileobj = findobj(gcbf,'Tag','stylfile');
         set(stylfileobj,'String',stylfile)
         set(stylfileobj,'UserData',[1 1]); setbuttons
      else
         stylfileobj = findobj(gcbf,'Tag','stylfile');
         set(stylfileobj,'UserData',[0 1]); setbuttons
         msgbox('The specified M file does not exist in the MATLAB path!','Error','error')
      end
   end
   
case 'convert'
   datadirobj = findobj(gcbf,'Tag','datadir');
   datadir = get(datadirobj,'String');
   datafilesobj = findobj(gcbf,'Tag','datafiles');
   datafilesidx = get(datafilesobj,'Value');
   datafiles = get(datafilesobj,'String');
   inpdirobj = findobj(gcbf,'Tag','inpdir');
   inpdir = get(inpdirobj,'String');
   vrmldirobj = findobj(gcbf,'Tag','vrmldir');
   vrmldir = get(vrmldirobj,'String');
   imfileobj = findobj(gcbf,'Tag','imfile');
   imfile = get(imfileobj,'String');
   aafileobj = findobj(gcbf,'Tag','aafile');
   aafile = get(aafileobj,'String');
   tsfileobj = findobj(gcbf,'Tag','tsfile');
   tsfile = get(tsfileobj,'String');
   aifileobj = findobj(gcbf,'Tag','aifile');
   aifile = get(aifileobj,'String');
   stylfileobj = findobj(gcbf,'Tag','stylfile');
   stylfile = get(stylfileobj,'String');
   w = waitbar(0,'Converting...');
   leftobj = findobj(gcbf,'Tag','left');
   left = get(leftobj,'Value');
   if (left)
      side = 'l';
   else
      side = 'r';
   end
   stylusobj = findobj(gcbf,'Tag','stylus');
   stylus = str2num(get(stylusobj,'String'));
   thoraxobj = findobj(gcbf,'Tag','thorax');
   thorax = str2num(get(thoraxobj,'String'));
   scaplocobj = findobj(gcbf,'Tag','scaploc');
   scaploc = str2num(get(scaplocobj,'String'));
   humerusobj = findobj(gcbf,'Tag','humerus');
   humerus = str2num(get(humerusobj,'String'));
   wristobj = findobj(gcbf,'Tag','wrist');
   wrist = str2num(get(wristobj,'String'));
   receiverorder = [stylus thorax scaploc humerus wrist]; %%bijv. [2 4 3 5] als wrist=[];
   mmobj = findobj(gcbf,'Tag','mm');
   mm = str2num(get(mmobj,'String'));
   inpfilesobj = findobj(gcbf,'Tag','inpfiles');
   inpfiles = get(inpfilesobj,'String');
   addpath(datadir)
   [path,imname] = fileparts(imfile);
   eval(imname)
   eval(['IM = ' imname ';'])
   [path,aaname] = fileparts(aafile);
   eval(aaname)
   eval(['loc1 = ' aaname ';'])
   [path,tsname] = fileparts(tsfile);
   eval(tsname)
   eval(['loc2 = ' tsname ';'])
   [path,ainame] = fileparts(aifile);
   eval(ainame)
   eval(['loc3 = ' ainame ';'])
   [path,stylfile] = fileparts(stylfile);
   ghscrewobj = findobj(gcbf,'Tag','gh-screw');
   usescrew = get(ghscrewobj,'Value');
   if (usescrew)
	   mov1obj = findobj(gcbf,'Tag','mov1file');
	   mov1file = get(mov1obj,'String');
	   mov2obj = findobj(gcbf,'Tag','mov2file');
	   mov2file = get(mov2obj,'String');
	   mov3obj = findobj(gcbf,'Tag','mov3file');
	   mov3file = get(mov3obj,'String');
	   [path,mov1name] = fileparts(mov1file);
	   eval(mov1name)
	   eval(['mov1 = ' mov1name ';'])
	   [path,mov2name] = fileparts(mov2file);
	   eval(mov2name)
	   eval(['mov2 = ' mov2name ';'])
	   [path,mov3name] = fileparts(mov3file);
	   eval(mov3name)
      eval(['mov3 = ' mov3name ';'])
      oftochmaarniet = 0;
   else
      mov1 = 0;
      mov2 = 0;
      mov3 = 0;
      oftochmaarniet = 1;
   end
   
   waitbar(0)
  % try
      for i = 1:length(datafilesidx)
         datafile = datafiles{datafilesidx(i)};
         [path,dataname] = fileparts(datafile);
         eval(dataname)
         eval(['data = ' dataname ';'])
         inpfile = [inpdir inpfiles{i}];
         vrmlfile = [vrmldir inpfiles{i}];
         [blvectors,hGH, sGH] = rec2blsc(IM,loc1,loc2,loc3,mov1,mov2,mov3,oftochmaarniet,receiverorder,mm,stylfile);
         %[blvectors] = rec2bl_gh(IM,loc1,loc2,loc3,mov1,mov2,mov3,oftochmaarniet,receiverorder,mm,stylfile);%origineel zonder _gh
         [gANGLES,jANGLES,modelinput] = palpfob(data,blvectors,side,receiverorder,0,vrmlfile);
         eval(['save ''' inpfile ''' modelinput -ascii'])
         
         %%%%%%%% marielle 16-10-2000 jANGLES wegschrijven voor clavicula en exorotatie studie%%%%%%%%%%%%%%%%%%%%%%%
         %%%%%%%% bijgewerkt voor clavicula ## 21-3-2001
         if length(inpfile)==34   %c:\clavicle\dataverw\eg\eglab1.m
            inpfile2=[inpfile(1:30),'j',inpfile(31:34)]
    	      eval(['save ''' inpfile2 ''' jANGLES -ascii'])
            if inpfile(28:30)==['ab1']
				   inpfile3=[inpfile(1:12),'gh',inpfile(24:30),'gh',inpfile(31:34)]
               eval(['save ''' inpfile3 ''' hGH sGH -ascii'])
            end    
         elseif length(inpfile)==35  
	         inpfile2=[inpfile(1:31),'j',inpfile(34:37)]
   	      eval(['save ''' inpfile2 ''' jANGLES -ascii'])
            if inpfile(29:31)==['ab1']
				   inpfile3=[inpfile(1:12),'gh',inpfile(24:31),'gh',inpfile(32:35)]
               eval(['save ''' inpfile3 ''' hGH sGH -ascii'])
            end    
         end 
        
         if length(inpfile)==38 %36, origineel   %c:\exorotatie\dataverw\eg\eglab1.m 38 van maken bij problemen
            inpfile2=[inpfile(1:32),'j',inpfile(33:36)]
    	      eval(['save ''' inpfile2 ''' jANGLES -ascii'])
            if inpfile(30:32)==['ab1']
				   inpfile3=[inpfile(1:14),'gh',inpfile(26:32),'gh',inpfile(33:36)]
               eval(['save ''' inpfile3 ''' hGH sGH -ascii'])
            end    
         elseif length(inpfile)==37  
	         inpfile2=[inpfile(1:33),'j',inpfile(34:37)]
   	      eval(['save ''' inpfile2 ''' jANGLES -ascii'])
            if inpfile(31:33)==['ab1']
				   inpfile3=[inpfile(1:14),'gh',inpfile(26:33),'gh',inpfile(34:37)]
               eval(['save ''' inpfile3 ''' hGH sGH -ascii'])
            end    
         end 
         %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

         waitbar(i/length(datafilesidx))
      end
      close(w)
   %catch
   %   msgbox({'An error occurred, please contact your local FoB specialist.',['(' lasterr ')']},'Error','error')
   %   close(w)
   %end
   
case 'savedefs'
   conv = which('convert');
   convdir = fileparts(conv);
   datadirobj = findobj(gcbf,'Tag','datadir');
   datadir = get(datadirobj,'String');
   inpdirobj = findobj(gcbf,'Tag','inpdir');
   inpdir = get(inpdirobj,'String');
   vrmldirobj = findobj(gcbf,'Tag','vrmldir');
   vrmldir = get(vrmldirobj,'String');
   stylusobj = findobj(gcbf,'Tag','stylus');
   stylus = get(stylusobj,'String');
   thoraxobj = findobj(gcbf,'Tag','thorax');
   thorax = get(thoraxobj,'String');
   scaplocobj = findobj(gcbf,'Tag','scaploc');
   scaploc = get(scaplocobj,'String');
   humerusobj = findobj(gcbf,'Tag','humerus');
   humerus = get(humerusobj,'String');
   wristobj = findobj(gcbf,'Tag','wrist');
   wrist = get(wristobj,'String');
   stylfileobj = findobj(gcbf,'Tag','stylfile');
   stylfile = get(stylfileobj,'String');
   mmobj = findobj(gcbf,'Tag','mm');
   mm = get(mmobj,'String');
   defsfile = [convdir filesep 'convdefs'];
   save(defsfile,'datadir','inpdir','vrmldir','stylus','thorax','scaploc','humerus','wrist','stylfile','mm')
   
case 'loaddefs'
   conv = which('calibrate');
   convdir = fileparts(conv);
   defsfile = [convdir filesep 'convdefs.mat'];
   if (exist(defsfile) == 2)
      load(defsfile)
      datadirobj = findobj(gcbf,'Tag','datadir');
      set(datadirobj,'String',datadir);
      convfunc('datadir')
      inpdirobj = findobj(gcbf,'Tag','inpdir');
      set(inpdirobj,'String',inpdir);
      convfunc('inpdir')
      vrmldirobj = findobj(gcbf,'Tag','vrmldir');
      set(vrmldirobj,'String',vrmldir);
      convfunc('vrmldir')
      stylusobj = findobj(gcbf,'Tag','stylus');
      set(stylusobj,'String',stylus);
      convfunc('receiver','stylus')
      thoraxobj = findobj(gcbf,'Tag','thorax');
      set(thoraxobj,'String',thorax);
      convfunc('receiver','thorax')
      scaplocobj = findobj(gcbf,'Tag','scaploc');
      set(scaplocobj,'String',scaploc);
      convfunc('receiver','scaploc')
      humerusobj = findobj(gcbf,'Tag','humerus');
      set(humerusobj,'String',humerus);
      convfunc('receiver','humerus')
      wristobj = findobj(gcbf,'Tag','wrist');
      set(wristobj,'String',wrist);
      stylfileobj = findobj(gcbf,'Tag','stylfile');
      set(stylfileobj,'String',stylfile);
      convfunc('stylfile')
      mmobj = findobj(gcbf,'Tag','mm');
      set(mmobj,'String',mm);
      convfunc('mm')
   end
   
end

function setbuttons
convbutton = findobj(gcbf,'Tag','convert');
defbutton = findobj(gcbf,'Tag','defaults');
datadirobj = findobj(gcbf,'Tag','datadir');
datadir = get(datadirobj,'UserData');
inpdirobj = findobj(gcbf,'Tag','inpdir');
inpdir = get(inpdirobj,'UserData');
vrmldirobj = findobj(gcbf,'Tag','vrmldir');
vrmldir = get(vrmldirobj,'UserData');
imfileobj = findobj(gcbf,'Tag','imfile');
imfile = get(imfileobj,'UserData');
aafileobj = findobj(gcbf,'Tag','aafile');
aafile = get(aafileobj,'UserData');
tsfileobj = findobj(gcbf,'Tag','tsfile');
tsfile = get(tsfileobj,'UserData');
aifileobj = findobj(gcbf,'Tag','aifile');
aifile = get(aifileobj,'UserData');
stylfileobj = findobj(gcbf,'Tag','stylfile');
stylfile = get(stylfileobj,'UserData');
stylusobj = findobj(gcbf,'Tag','stylus');
stylus = get(stylusobj,'UserData');
thoraxobj = findobj(gcbf,'Tag','thorax');
thorax = get(thoraxobj,'UserData');
scaplocobj = findobj(gcbf,'Tag','scaploc');
scaploc = get(scaplocobj,'UserData');
humerusobj = findobj(gcbf,'Tag','humerus');
humerus = get(humerusobj,'UserData');
mmobj = findobj(gcbf,'Tag','mm');
mm = get(mmobj,'UserData');
mov1obj = findobj(gcbf,'Tag','mov1file');
mov2obj = findobj(gcbf,'Tag','mov2file');
mov3obj = findobj(gcbf,'Tag','mov3file');
mov1 = get(mov1obj,'UserData');
mov2 = get(mov2obj,'UserData');
mov3 = get(mov3obj,'UserData');
status = [datadir; inpdir; vrmldir; imfile; aafile; tsfile; aifile; stylfile; stylus; thorax; scaploc; humerus; mm; mov1; mov2; mov3];
if (status(:,1) == ones(size(status,1),1))
   set(convbutton,'Enable','On')
else
   set(convbutton,'Enable','Off')
end
if (status(:,2) == ones(size(status,1),1))
   set(defbutton,'Enable','On')
else
   set(defbutton,'Enable','Off')
end
