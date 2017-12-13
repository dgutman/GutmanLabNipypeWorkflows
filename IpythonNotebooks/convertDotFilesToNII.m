
basePath = '/EHECHT_BIGDATA/POST_MORTEM_FOXES/WholeBrainMatrixConnectivity_downsample_4/';
dotFileList = {'Fox_C_fdt_matrix3_downsample_4.dot', 'Fox_D_fdt_matrix3_downsample_4.dot', 'Fox_E_fdt_matrix3_downsample_4.dot'};


cd(basePath);
for s=1:length(dotFileList)
disp(dotFileList{1,s})
end

% WORKINGDIR = '/home/ehecht/POST_MORTEM_FOXES/';Fox_C_fdt_matrix3_downsample_4.dot

% add paths of functions
% addpath('/home/ehecht/POST_MORTEM_FOXES/SCRIPTS/');
% a ddpath('/home/ehecht/matlab/NIFTI_tools/');

%SUBJID = {'Fox_10T', 'Fox_11T', 'Fox_12T', 'Fox_2T', 'Fox_3T', 'Fox_4T',
%'Fox_5T', 'Fox_7T', 'Fox_8T', 'Fox_9T', 'Fox_49A', 'Fox_50A', 'Fox_51A',
%'Fox_52A', 'Fox_54A', 'Fox_56A', 'Fox_57A', 'Fox_58A', 'Fox_59A',
%'Fox_60A', 'Fox_13U', 'Fox_14U', 'Fox_15U', 'Fox_16U', 'Fox_17U',
%'Fox_18U', 'Fox_20U', 'Fox_22U', 'Fox_23U', 'Fox_24U'};

%for s=1:length(SUBJID)
%cd(fullfile(WORKINGDIR,SUBJID{1,s},'data.bedpostX','WholeBrainMatrixConnectivity_TemplateSpace_ds0.9'))
%disp(SUBJID{1,s})
%load('connectivity_matrix_nothr.mat'); % M has size 24103 x 24103
%row=zeros(1,24103); % the first dimension is height
%col=zeros(24104,1); %  the second dimension is length
%M=cat(1,M,row);
%M=cat(2,M,col); % M is now 24104 x 24104, with zeros on the right and bottom
%B=reshape(M,64,529,17161);  % factors of (24104x24104)
%save('connectivity_matrix_nothr_reshape3d.mat','B','-v7.3');
%nii=make_nii(B);
%save_nii(nii,'connectivity_matrix_nothr_reshape3d.nii');  % image
%dimensions 64 x 529 x 17161
%end

% to get back to original size of M: N = reshape(M,24104,24104);
%N(:,24104)=[]; N(24104,:)=[];
