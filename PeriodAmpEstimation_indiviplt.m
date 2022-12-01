%Program for estimating period/amplitude from time-series intensity data

%170925 Written

%Save option
save_o=1; %0:Do not save 1:Save
%Peak detect option
hil_o=0; %0:Use raw signal 1:Use phase information calculated by Hilbert transform 
SG_o=1;%0:Do not filter 1:filter
%%
%parameters
movL=101;  %Window size for calculating the average
SG_D=2; %Dimension for SG filtering
SG_L=21; %length for SG filtering, must be odd
%% 
set(0,'DefaultTextInterpreter','none')
%Get data files
uiwait(msgbox('Select data files(.txt or .csv)'));
[filename,pathname] = uigetfile({'*.txt;*.csv'},'Select time-series data files with two columns(Time,Signal)and one header line','MultiSelect', 'on');
%%
if isempty(filename)
    disp('Script aborted');
else
    if iscell(filename)==0
        filename={filename};
    end
    
    fullpath=strcat(pathname,filename);
    filename_all=replace(filename,{'.csv','.txt'},'');
        
    uiwait(msgbox({'User selected:'; strjoin(filename_all,'\n')},'File selection','modal'));

    n_sample=length(filename);
    
% 
%     %Dialog for getting paramters
%     prompt = {'Enter time interval for between frames (min):'};
%     dlg_title = 'Input';
%     defaultans = {'5'};
%     answer = inputdlg(prompt,dlg_title,1,defaultans);
    %%
    %Matrix,parameters
    %dT= str2double(answer{1}); %Interval of the time-lapse imaging (min)
    if any(SG_o)
    h_movL=(movL-1)/2;
    h_SG_L=(SG_L)/2;
    else
    h_movL=0;
    h_SG_L=0;
    end
        
    karnel=repmat(1/movL,movL,1); %karnel for moving average
    
    plot_titles={'Raw data','Moving average','De-trended','Auto-correlation function'};
    Data=cell(n_sample,1);
    Raw=cell(n_sample,1);
    Mov=cell(n_sample,1);
    Det=cell(n_sample,1);
    Det_SG=cell(n_sample,1);
    Hil=cell(n_sample,1);
    InstPhase=cell(n_sample,1);
    Period=cell(n_sample,1);  
    peaks=cell(n_sample,1);  
    loc_p=cell(n_sample,1);  
    Amp=cell(n_sample,1);
    norm_Amp=cell(n_sample,1);
    troughs=cell(n_sample,1);
    loc_t=cell(n_sample,1);
    Time=cell(n_sample,1);

        n_plot=5;




%     %Import data
%     for i=1:n_sample
%         fileID=fopen(fullpath{i});
%         Data{i}= cell2mat(textscan(fileID,'%*f %f','HeaderLines',1));
%     end

        


    for i=1:n_sample  
        %Time=0:dT:(length(Data{i})-1)*dT; %Time point
        fileID=fopen(fullpath{i});
        Data{i}= cell2mat(textscan(fileID,'%f %f','HeaderLines',1,'Delimiter',','));
        fclose(fileID);
        Time{i}=Data{i}(:,1)*10/60;
        dT=diff(Time{i}(1:2));
        Raw{i}=Data{i}(:,2);
        %Moving average
        Mov{i}=conv( padarray(Raw{i},[(movL-1)/2 0],'symmetric'),karnel,'valid'); %moving average to get trend
        %De-trending
        Det{i}=Raw{i}-Mov{i};
        
        if SG_o==1
            Det_SG{i}=sgolayfilt(Det{i},SG_D,SG_L);
        else
            Det_SG{i}=Det{i};
        end
           
            Hil{i}=hilbert(Det_SG{i});
            InstPhase{i}=angle(Hil{i}); 
             
            [Period{i},Amp{i},loc_p{i}, loc_t{i}]=peramp(Det_SG{i},InstPhase{i},abs(Hil{i}),dT,0,0,0);
            
            peaks{i}=Det_SG{i}(loc_p{i});
            troughs{i}=Det_SG{i}(loc_t{i});
            
            loc_p{i}=Time{i}(loc_p{i});
            loc_t{i}=Time{i}(loc_t{i});
% 
%                 
 
    end
   
    %outfolder = uigetdir('Save csv file'); %Open dialog to obtain file name from imput

%Put all data into a new structure
    Data_analyzed=struct('Filename',filename_all','Time',Time,'Raw',Raw,'Trend',Mov,'Detrended',Det,'SG',Det_SG,...
        'Phase',InstPhase,'Period',Period,'Amplitude',Amp,'NormAmp',norm_Amp,'Peaks',peaks,'PeakLocation',loc_p,'Troughs',troughs,'TroughLocation',loc_t);
    FieldNames=fieldnames(Data_analyzed);
    
    pos_t=2;
    data2plot=[3 4 5 6 7];    
            %plot
    for i=1:n_sample
        %figure
        figdata=figure('Name','Signal processing','Position',[100 100 300 700],'Visible','off');
        figdata.Color='white';
        h_data= gobjects(n_plot,1);
        for k = 1:n_plot
            h_data(k) = subplot(n_plot,1,k);
        end



                for j=1:n_plot
                    subplot(h_data(j))
                    plot(Data_analyzed(i).(FieldNames{pos_t}),Data_analyzed(i).(FieldNames{data2plot(j)}));
                    ax = gca; % current axes
                    ax.FontSize = 10; 
                    title([Data_analyzed(i).Filename,' ',FieldNames{data2plot(j)}]);
                    ylabel('Intensity (a.u.)','FontSize',10,'FontWeight','bold');
                    xlabel('Time (h)','FontSize',10,'FontWeight','bold');
                    %xlim([0 72]);

                    if j==5 %Overlay cos on Instphase
                        hold on
                        plot(Data_analyzed(i).(FieldNames{pos_t}),cos(Data_analyzed(i).(FieldNames{data2plot(j)})));
                    end
                end
            hold on 
            if any(Data_analyzed(i).PeakLocation)
                plot(Data_analyzed(i).PeakLocation,ax.YLim(2)*0.9,'v','MarkerEdgeColor','r',...
                    'MarkerFaceColor','r') %Draw a marker at a point where correlation is maximum
            end
            

            %csvwrite(outfullpath,[lags_c{:}'*dT xcor{:}]);

            %savefig(figdata,fullfile(pathname,strcat(Data_analyzed(i).Filename,'Fig.fig')));
            saveas(figdata,fullfile(pathname,strcat(Data_analyzed(i).Filename,'_Fig.pdf')),'pdf');
            
            close(figdata)
    end

str2csv(Data_analyzed,pathname,[],'_analyzed');
%%
label=arrayfun(@(x) x.('Filename'),Data_analyzed,'UniformOutput',0)';
for i=1:length(Data_analyzed)

   label{i}=label{i};
   
end
output_cell=str2csv_all4dotplot(Data_analyzed,pathname,'Period','per4dotplot',label);
output_cell=str2csv_all4dotplot(Data_analyzed,pathname,'Amplitude','amp4dotplot',label);
%output_cell=str2csv_all4plotampper(Data_analyzed,pathname,'PeakLocation','NormAmp','ampnorm4schatterplot',label);
%output_cell=str2csv_all4plotampper(Data_analyzed,pathname,'PeakLocation','Period','per4schatterplot',label);

end


