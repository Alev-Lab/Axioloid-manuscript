function output_cell=str2csv_all4dotplot(s,outfolder,field,name,lab)

           Header={'name';'nth_peak';'value'};
%     g=cell(length(s),1);       
%     for i=1:length(s)
%         g{i} = repmat(lab(i),length(s(i).(field)),1);
%     end

           output_cell=cell(sum(cell2mat(arrayfun(@(x) length(x.(field)),s,'UniformOutput',0))),3);
    pos=1;
    for i=1:length(s)

           if ~isempty(s(i).(field))
           
           output_cell(pos:pos+size(s(i).(field),1)-1,1)=repmat(lab(i),length(s(i).(field)),1);
           
           output_cell(pos:pos+size(s(i).(field),1)-1,2)=num2cell(repmat(i,length(s(i).(field)),1));
           output_cell(pos:pos+size(s(i).(field),1)-1,3)=num2cell(s(i).(field));
            
                    %disp(output_cell(1:size(num2cell(s(i).(field)),1),i))
                    
           pos=pos+length(s(i).(field));
           end

    end

    if any(outfolder)
        fid = fopen(strcat(outfolder,'/',name,'.csv'),'wt');
    else
        fid = fopen(strcat(name,'.csv'),'wt');
    end

    if any(fid)
        for c=1:length(Header)
            fprintf(fid,'%s,',Header{c});
        end
        fprintf(fid,'\n');

        for k=1:size(output_cell,1)
            for c=1:3

                if ischar(output_cell{k,c}) 
                    fprintf(fid,'%s,',output_cell{k,c});
                else
                    fprintf(fid,'%.2f,',output_cell{k,c});
                end
            end
            fprintf(fid,'\n');
        end
        fclose(fid);
    end    
%         output_cell=cellfun(@(x) num2str(x),output_cell,'UniformOutput',0);
%         output_cell(cellfun(@(x) isempty(x),output_cell))={' '};
        


end
