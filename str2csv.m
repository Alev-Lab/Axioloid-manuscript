function str2csv(s,outfolder)
    FieldNames=fieldnames(s);

    for i=1:length(s)
        Header=cell(sum(cellfun(@(x) size(s(i).(x),2),FieldNames(2:end))),1);
        output_cell=cell(max(cellfun(@(x) size(s(i).(x),1),FieldNames)),sum(cellfun(@(x) size(s(i).(x),2),FieldNames(2:end))));
        
        for j=1:length(FieldNames)-1
            if  ~isempty(s(i).(FieldNames{j+1}))
                col=sum(cellfun(@(x) size(s(i).(x),2),FieldNames(2:j)))+1;
                if size(s(i).(FieldNames{j+1}),2)>1

                    Header{col,1}=strcat(FieldNames{j+1},'_x');
                    Header{col+1,1}=strcat(FieldNames{j+1},'_y');
                    output_cell(1:size(num2cell(s(i).(FieldNames{j+1})),1),col:col+1)=[num2cell(s(i).(FieldNames{j+1})(:,1)) num2cell(s(i).(FieldNames{j+1})(:,2))]; 
                else
                    Header{col,1}=FieldNames{j+1};
                    output_cell(1:size(num2cell(s(i).(FieldNames{j+1})),1),col)=num2cell(s(i).(FieldNames{j+1})); 

                end
            end
        end
        output_cell=cellfun(@(x) num2str(x),output_cell,'UniformOutput',0);
        output_cell(cellfun(@(x) isempty(x),output_cell))={' '};
        fid = fopen(strcat(outfolder,'/',s(i).Filename,'_analyzed.csv'),'wt');



        if any(fid)
            for c=1:length(Header)
                fprintf(fid,'%s,',Header{c});
            end
            fprintf(fid,'\n');
            for k=1:size(output_cell,1)
                for c=1:size(output_cell,2)
                    fprintf(fid,'%s,',output_cell{k,c});
                end
                fprintf(fid,'\n');
            end
            fclose(fid);
        end    

    end

end
