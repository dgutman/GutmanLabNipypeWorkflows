#!/usr/bin/perl

$RAWDATAPATH="/home/ehecht/BIGDATA/Stout_Homo_Faber/RAWDATA/";
$WORKINGDATAPATH="/home/ehecht/BIGDATA/Stout_Homo_Faber/WORKINGDATA/"; 
$OUTPUTDATAPATH="/home/ehecht/BIGDATA/Stout_Homo_Faber/WORKINGDATA/IFG-PrCG_Segmentation"; 

$subjIDSTRING="Homofabor_ID001_BITC20150129 HOMO-FABERSubject1_BITC20150527 HOMO_FABERSubject#1_BITC20151022 Homofabor_ID002_BITC20141205 HOMO-FABERSubject2_BITC20150527 HOMO_FABERSubject#2_BITC20151019 Homofabor_ID003_BITC20141211 HOMO-FABERSubject3_BITC20150408 HOMO-FABERSubject3_BITC20150422 HOMO-FABERSubject3_BITC20150508 Homofabor_ID004_BITC20141212 Homofabor_ID005_BITC20141216 HOMO-FABERSubject5_BITC20150504 HOMO_FABERSubject#5_BITC20151007 Homofabor_ID006_BITC20150114 HOMO-FABERSubject#6_BITC20150625 HOMO-FABERSubject_BITC20150604 Homofabor_ID007_BITC20150129 HOMO-FABERSubject7_BITC20150410 HOMO_FABERSubject#7_BITC20150708 Homofabor_ID008_BITC20150226 HOMO-FABERSubject#8_BITC20150612 Homofabor_ID009_BITC20150121 HOMO_FABERSubject#9_BITC20150701 HOMO_FABERSubject#9_BITC20151021 Homofabor_ID010_BITC20150123 HOMO-FABERSubject10_BITC20150421 HOMO-FABERSubject10_BITC20150508 HOMO-FABERSubject11_BITC20150610 HOMO_FABERSubject11_BITC20160111 HOMOFABERSubject12_BITC20150902 HOMO_FABERSubject#13_BITC20151026 HOMO_FABERSubject14_BITC20150813 HOMO_FABERSubject14_BITC20151202 HOMOFABER_BITC20150831 HOMOFABERSubject15_BITC20150831 HOMOFABERSubject50_BITC20150831 HOMO_FABERSubject15_BITC20151208 HOMO_FABERSubject16_BITC20151216 HOMO_FABERSubject17_BITC20151112 HOMO_FABERSubject18_BITC20151120 HOMO_FABERSubject19_BITC20151117 HOMO_FABERSubject20_BITC20151120 HOMO_FABERSubject21_BITC20151105 HOMO_FABERSubject22_BITC20151119 HOMO_FABERSubject22_BITC20160121 HOMO_FABERSubject23_BITC20151209 HOMO_FABERSubject24_BITC20151112 HOMO_FABERSubject24_BITC20160111 HOMO_FABERSubject25_BITC20151210 HOMO_FABERSubject26_BITC20151117 HOMO_FABERSubject26_BITC20160127 HOMO_FABERSubject27_BITC20151203 HOMO_FABERSubject27_BITC20160205 HOMO_FABERSubject28_BITC20160126 HOMO_FABERSubject29_BITC20151116 HOMO_FABERSubject31_BITC20160204 HOMO_FABERSubject32_BITC20160203 HOMO_FABERSubject34_BITC20160129";
@subjID = split(/ /,$subjIDSTRING);

$subjSTRING="Subj01_Scan1 Subj01_Scan2 Subj01_Scan3 Subj02_Scan1 Subj02_Scan2a Subj02_Scan2b Subj03_Scan1 Subj03_Scan2a Subj03_Scan2b Subj03_Scan3 Subj04_Scan1 Subj05_Scan1 Subj05_Scan2 Subj05_Scan3 Subj06_Scan1 Subj06_Scan2a Subj06_Scan2b Subj07_Scan1 Subj07_Scan2 Subj07_Scan3 Subj08_Scan1 Subj08_Scan2 Subj09_Scan1 Subj09_Scan2 Subj09_Scan3 Subj10_Scan1 Subj10_Scan2 Subj10_Scan3 Subj11_Scan1 Subj11_Scan2 Subj12_Scan1 Subj13_Scan1 Subj14_Scan1 Subj14_Scan2 Subj15_Scan1 Subj15_Scan1b Subj15_Scan1b Subj15_Scan2 Subj16_Scan1 Subj17_Scan1 Subj18_Scan1 Subj19_Scan1 Subj20_Scan1 Subj21_Scan1 Subj22_Scan1 Subj22_Scan2 Subj23_Scan1 Subj24_Scan1 Subj24_Scan2 Subj25_Scan1 Subj26_Scan1 Subj26_Scan2 Subj27_Scan1 Subj27_Scan2 Subj28_Scan1 Subj29_Scan1 Subj31_Scan1 Subj32_Scan1 Subj34_Scan1";
@subj = split(/ /,$subjSTRING);

$volSTRING="07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97";
@vol = split(/ /,$volSTRING);

$roiSTRING="IFG-vPrCG"; 
@roi = split(/ /,$roiSTRING);

$hemiSTRING="L R";
@hemi = split(/ /,$hemiSTRING);

# run topup first, then feed topup output into eddy (the new eddy, not the old eddy_correct)

for($i=0;$i<=$#subj;$i++)	{

print "#\$ -cwd\n";
print "#\$ -S /bin/bash \n";
print "export FSLDIR=/usr/local/fsl  \n";
print ". /usr/share/fsl/5.0/etc/fslconf/fsl.sh \n";
print "export PATH=\$PATH:\$FSLDIR/bin \n";
print "#!/bin/bash \n";

# set up directories
$statement  = " mkdir $WORKINGDATAPATH/" . $subj[$i] . "/ ";
#print "$statement \n";
$statement  = " mkdir $WORKINGDATAPATH/" . $subj[$i] . "/T1/ ";
#print "$statement \n";
$statement  = " mkdir $WORKINGDATAPATH/" . $subj[$i] . "/DTI/ ";
#print "$statement \n";
$statement  = " mkdir $WORKINGDATAPATH/" . $subj[$i] . "/DTI/data/ ";
#print "$statement \n";
$statement  = " mkdir $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/ ";
#print "$statement \n";
$statement  = " mkdir $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/5B0_PA/ ";
#print "$statement \n";
$statement  = " mkdir $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/ ";
#print "$statement \n";
$statement  = " mkdir $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_ADC/ ";
#print "$statement \n";
$statement  = " mkdir $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_FA/ ";
#print "$statement \n";
$statement  = " mkdir $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_TENSOR/ ";
#print "$statement \n";
$statement  = " mkdir $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_TRACEW/ ";
#print "$statement \n";

# convert dicoms
$statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/T1/ ";
$statement .= " $RAWDATAPATH/" . $subjID[$i] . "/t1*/ ";
#print "$statement \n";
$statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/5B0_PA/ ";
$statement .= " $RAWDATAPATH/" . $subjID[$i] . "/cmrr_mbep2d_diff_*5B0_PA*/ ";
#print "$statement \n";
$statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/ ";
$statement .= " $RAWDATAPATH/" . $subjID[$i] . "/cmrr_mbep2d_diff_AP_[1-9]*/ ";
#print "$statement \n";
$statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_ADC/ ";
$statement .= " $RAWDATAPATH/" . $subjID[$i] . "/cmrr_mbep2d_diff_AP_ADC_[1-9]*/ ";
#print "$statement \n";
$statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_FA/ ";
$statement .= " $RAWDATAPATH/" . $subjID[$i] . "/cmrr_mbep2d_diff_AP_FA_[1-9]*/ ";
#print "$statement \n";
$statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_TRACEW/ ";
$statement .= " $RAWDATAPATH/" . $subjID[$i] . "/cmrr_mbep2d_diff_AP_TRACEW_[1-9]*/ ";
#print "$statement \n";

# rename files
$statement  = " mv $WORKINGDATAPATH/" . $subj[$i] . "/T1/co*.nii.gz ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/T1/struc_raw.nii.gz ";
#print "$statement \n";
$statement  = " mv $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/5B0_PA/*.nii.gz ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/5B0_PA/nodif_PA.nii.gz ";
#print "$statement \n";
$statement  = " mv $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/5B0_PA/*.bval ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/5B0_PA/nodif_PA_bval ";
#print "$statement \n";
$statement  = " mv $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/5B0_PA/*.bvec ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/5B0_PA/nodif_PA_bvec ";
#print "$statement \n";
$statement  = " mv $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/*.nii.gz ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/data_AP.nii.gz ";
#print "$statement \n";
$statement  = " mv $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/*.bval ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/data_AP_bval ";
#print "$statement \n";
$statement  = " mv $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/*.bvec ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/data_AP_bvec ";
#print "$statement \n";
$statement  = " mv $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_ADC/*.nii.gz ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_ADC/AP_ADC.nii.gz ";
#print "$statement \n";
$statement  = " mv $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_FA/*.nii.gz ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_FA/AP_FA.nii.gz ";
#print "$statement \n";
$statement  = " mv $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_TRACEW/*.nii.gz ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_TRACEW/AP_TRACEW.nii.gz ";
#print "$statement \n";
$statement  = " mv $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_TRACEW/*.bval ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_TRACEW/AP_TRACEW_bval ";
#print "$statement \n";
$statement  = " mv $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_TRACEW/*.bvec ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_TRACEW/AP_TRACEW_bvec ";
#print "$statement \n";

# get AP avg b0
$statement  = " fslsplit $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/data_AP.nii.gz ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/vol -t ";
#print "$statement \n";
$statement  = " fslmaths $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/vol0000.nii.gz ";
$statement .= " -add $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/vol0001.nii.gz ";
$statement .= " -add $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/vol0002.nii.gz ";
$statement .= " -add $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/vol0003.nii.gz ";
$statement .= " -add $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/vol0004.nii.gz ";
$statement .= " -add $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/vol0005.nii.gz ";
$statement .= " -add $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/vol0006.nii.gz ";
$statement .= " -div 7 $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/avg_b0_AP.nii.gz ";
#print "$statement \n";

# get PA avg b0
$statement  = " fslsplit $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/5B0_PA/nodif_PA.nii.gz ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/5B0_PA/vol -t ";
#print "$statement \n";
$statement  = " fslmaths $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/5B0_PA/vol0000.nii.gz ";
$statement .= " -add $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/5B0_PA/vol0001.nii.gz ";
$statement .= " -add $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/5B0_PA/vol0002.nii.gz ";
$statement .= " -add $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/5B0_PA/vol0003.nii.gz ";
$statement .= " -add $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/5B0_PA/vol0004.nii.gz ";
$statement .= " -div 5 $WORKINGDATAPATH/" .$subj[$i] . "/DTI/preprocess/5B0_PA/avg_b0_PA.nii.gz ";
#print "$statement \n";

# get AP dti
$x=0;
$statement  = " fslmerge -t $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/dti_AP.nii.gz ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/vol00" . $vol[$x] . ".nii.gz ";
for($x=1;$x<=$#vol;$x++)	{
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/vol00" . $vol[$x] . ".nii.gz ";
				}
#print "$statement \n";
$statement  = " fslroi $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/dti_AP.nii.gz ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/dti_AP_trim.nii.gz ";
$statement .= " 0 -1 0 -1 0 110 ";
#print "$statement \n"; # topup needs an even # of slices

# make merged avg b0
$statement  = " fslmerge -t $WORKINGDATAPATH/" .$subj[$i] . "/DTI/preprocess/merged_b0_AP-PA.nii.gz ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/avg_b0_AP.nii.gz ";
$statement .= " $WORKINGDATAPATH/" .$subj[$i] . "/DTI/preprocess/5B0_PA/avg_b0_PA.nii.gz ";
#print "$statement \n";
$statement  = " fslroi $WORKINGDATAPATH/" .$subj[$i] . "/DTI/preprocess/merged_b0_AP-PA.nii.gz ";
$statement .= " $WORKINGDATAPATH/" .$subj[$i] . "/DTI/preprocess/merged_b0_AP-PA_trim.nii.gz ";
$statement .= " 0 -1 0 -1 0 110 ";
#print "$statement \n";  # topup needs an even # of slices
$statement  = " fslmerge -t $WORKINGDATAPATH/" .$subj[$i] . "/DTI/preprocess/merged_b0_AP-PA_dti_trim.nii.gz ";
$statement .= " $WORKINGDATAPATH/" .$subj[$i] . "/DTI/preprocess/merged_b0_AP-PA_trim.nii.gz ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/dti_AP_trim.nii.gz ";
#print "$statement \n";  # will be input for eddy

# topup unwarping
$statement  = " topup ";
$statement .= " --imain=$WORKINGDATAPATH/" .$subj[$i] . "/DTI/preprocess/merged_b0_AP-PA_trim.nii.gz ";
$statement .= " --datain=$WORKINGDATAPATH/acq_params.txt ";
$statement .= " --config=/usr/share/fsl/5.0/etc/flirtsch/b02b0.cnf ";
$statement .= " --out=$WORKINGDATAPATH/" .$subj[$i] . "/DTI/preprocess/topup ";
$statement .= " --fout=$WORKINGDATAPATH/" .$subj[$i] . "/DTI/preprocess/topup_fieldmap "; # can be used for FEAT
$statement .= " --iout=$WORKINGDATAPATH/" .$subj[$i] . "/DTI/preprocess/merged_b0_unwarped.nii.gz ";
#print "$statement \n";
$statement  = " applytopup ";
$statement .= " --method=jac "; # because dti images are only acquired in AP direction; not merging AP+PA
$statement .= " --imain=$WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/dti_AP_trim.nii.gz ";
$statement .= " --inindex=1 "; # because in the merged_b0_AP-PA file used to drive topup, the AP data is first
$statement .= " --datain=$WORKINGDATAPATH/acq_params.txt ";
$statement .= " --topup=$WORKINGDATAPATH/" .$subj[$i] . "/DTI/preprocess/topup ";
$statement .= " --out=$WORKINGDATAPATH/" .$subj[$i] . "/DTI/preprocess/dti_unwarped.nii.gz ";
#print "$statement \n";

# make data, nodif, and nodif_brain_mask
$statement  = " fslsplit $WORKINGDATAPATH/" .$subj[$i] . "/DTI/preprocess/merged_b0_unwarped.nii.gz ";
$statement .= " $WORKINGDATAPATH/" .$subj[$i] . "/DTI/preprocess/merged_b0_unwarped_vol -t ";
#print "$statement \n";
$statement  = " fslmaths $WORKINGDATAPATH/" .$subj[$i] . "/DTI/preprocess/merged_b0_unwarped_vol0000 ";
$statement .= " -add $WORKINGDATAPATH/" .$subj[$i] . "/DTI/preprocess/merged_b0_unwarped_vol0001 ";
$statement .= " -div 2 $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/nodif.nii.gz ";
#print "$statement \n";
$statement  = " bet $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/nodif.nii.gz ";
$statement .= " $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/nodif_brain ";
$statement .= " -m -f 0.3 -R";
#print "$statement \n";
$statement  = " fast -B -g -t 2 -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/data/nodif_brain ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/data/nodif_brain.nii.gz ";
#print "$statement \n";
$statement  = " mv $WORKINGDATAPATH/" . $subj[$i] . "/DTI/data/nodif_brain_seg_0.nii.gz ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/data/nodif_brain_GM.nii.gz ";
#print "$statement \n";
$statement  = " mv $WORKINGDATAPATH/" . $subj[$i] . "/DTI/data/nodif_brain_seg_1.nii.gz ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/DTI/data/nodif_brain_WM.nii.gz ";
#print "$statement \n";

# eddy
$statement  = " eddy ";
$statement .= " --imain=$WORKINGDATAPATH/" .$subj[$i] . "/DTI/preprocess/merged_b0_AP-PA_dti_trim.nii.gz ";
$statement .= " --mask=$WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/nodif_brain_mask.nii.gz ";
$statement .= " --index=$WORKINGDATAPATH/eddy_index.txt ";
$statement .= " --acqp=$WORKINGDATAPATH/acq_params.txt ";
$statement .= " --topup=$WORKINGDATAPATH/" .$subj[$i] . "/DTI/preprocess/topup ";
$statement .= " --bvecs=$WORKINGDATAPATH/eddy_bvecs ";
$statement .= " --bvals=$WORKINGDATAPATH/eddy_bvals ";
$statement .= " --out=$WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/data_eddy ";
#print "$statement \n";
$statement  = " fslroi ";
$statement .= " $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/data_eddy.nii.gz ";
$statement .= " $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/nodif1.nii.gz ";
$statement .= " 0 1 ";
#print "$statement \n";
$statement  = " fslroi ";
$statement .= " $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/data_eddy.nii.gz ";
$statement .= " $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/nodif2.nii.gz ";
$statement .= " 1 1 ";
#print "$statement \n";
$statement  = " fslmaths $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/nodif1.nii.gz ";
$statement .= " -add $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/nodif2.nii.gz ";
$statement .= " -div 2 $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/nodif.nii.gz ";
#print "$statement \n";
$statement  = " fslroi ";
$statement .= " $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/data_eddy.nii.gz ";
$statement .= " $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/data_dti.nii.gz ";
$statement .= " 2 91 ";
#print "$statement \n";
$statement  = " fslmerge -t $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/data.nii.gz ";
$statement .= " $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/nodif.nii.gz ";
$statement .= " $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/data_dti.nii.gz ";
#print "$statement \n";

# dtifit
$statement  = " dtifit ";
$statement .= " -k $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/data.nii.gz ";
$statement .= " -o $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/data ";
$statement .= " -m $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/nodif_brain_mask.nii.gz ";
$statement .= " -r $WORKINGDATAPATH/bvecs "; 
$statement .= " -b $WORKINGDATAPATH/bvals ";
#print "$statement \n";

# bedpost
$statement  = " cp $WORKINGDATAPATH/bvecs ";
$statement .= " $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/bvecs ";
#print "$statement \n";
$statement  = " cp $WORKINGDATAPATH/bvals ";
$statement .= " $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/bvals ";
#print "$statement \n";
$statement  = " bedpostx $WORKINGDATAPATH/" .$subj[$i] . "/DTI/data/";
#print "$statement \n";

# T1 preprocessing
$statement  = " fslreorient2std $WORKINGDATAPATH/" . $subj[$i] . "/T1/struc_raw.nii.gz ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/T1/struc_raw.nii.gz ";
#print "$statement \n";
$statement  = " bet $WORKINGDATAPATH/" . $subj[$i] . "/T1/struc_raw.nii.gz ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/T1/struc_brain ";
$statement .= " -m -f 0.4 -g -0.1 -B ";
#print "$statement \n";
$statement  = " fast -B -g -o $WORKINGDATAPATH/" . $subj[$i] . "/T1/struc_brain ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/T1/struc_brain.nii.gz ";
#print "$statement \n";
$statement  = " mv $WORKINGDATAPATH/" . $subj[$i] . "/T1/struc_brain_restore.nii.gz ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/T1/struc_brain.nii.gz ";
#print "$statement \n";
$statement  = " mv $WORKINGDATAPATH/" . $subj[$i] . "/T1/struc_brain_seg_1.nii.gz ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/T1/struc_brain_GM.nii.gz ";
#print "$statement \n";
$statement  = " mv $WORKINGDATAPATH/" . $subj[$i] . "/T1/struc_brain_seg_2.nii.gz ";
$statement .= " $WORKINGDATAPATH/" . $subj[$i] . "/T1/struc_brain_WM.nii.gz ";
#print "$statement \n";

## REGISTRATION

$statement  = " mkdir $WORKINGDATAPATH/" . $subj[$i] . "/xfms/ ";
#print "$statement \n";

$statement  = " flirt -dof 12 -in $WORKINGDATAPATH/" . $subj[$i] . "/T1/struc_brain.nii.gz ";
$statement .= " -ref $WORKINGDATAPATH/MNI152_T1_1mm_brain.nii.gz ";
$statement .= " -omat $WORKINGDATAPATH/" . $subj[$i] . "/xfms/struc_12dof_MNI.mat ";
#print "$statement \n";

$statement  = " fnirt --in=$WORKINGDATAPATH/" . $subj[$i] . "/T1/struc_raw.nii.gz ";
$statement .= " --ref=$WORKINGDATAPATH/MNI152_T1_1mm.nii.gz ";
$statement .= " --aff=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/struc_12dof_MNI.mat ";
$statement .= " --cout=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/struc_warp_MNI_warpfield.nii.gz ";
#print "$statement \n";

$statement  = " applywarp --in=$WORKINGDATAPATH/" . $subj[$i] . "/T1/struc_brain.nii.gz ";
$statement .= " --ref=$WORKINGDATAPATH/MNI152_T1_1mm.nii.gz ";
$statement .= " --warp=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/struc_warp_MNI_warpfield.nii.gz ";
$statement .= " --out=$WORKINGDATAPATH/" . $subj[$i] . "/T1/struc_2_MNI.nii.gz ";
#print "$statement \n";

$statement  = " invwarp --warp=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/struc_warp_MNI_warpfield.nii.gz ";
$statement .= " --ref=$WORKINGDATAPATH/" . $subj[$i] . "/T1/struc_brain.nii.gz ";
$statement .= " --out=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/MNI_warp_struc_warpfield.nii.gz ";
#print "$statement \n";

$statement  = " flirt -dof 12 -in $WORKINGDATAPATH/" . $subj[$i] . "/DTI/data/nodif_brain.nii.gz ";
$statement .= " -ref $WORKINGDATAPATH/" . $subj[$i] . "/T1/struc_brain.nii.gz ";
$statement .= " -omat $WORKINGDATAPATH/" . $subj[$i] . "/xfms/nodif_12dof_struc.mat ";
#print "$statement \n";

$statement  = " flirt -in $WORKINGDATAPATH/" . $subj[$i] . "/DTI/data/nodif_brain.nii.gz ";
$statement .= " -ref $WORKINGDATAPATH/" . $subj[$i] . "/T1/struc_brain.nii.gz ";
$statement .= " -applyxfm -init $WORKINGDATAPATH/" . $subj[$i] . "/xfms/nodif_12dof_struc.mat ";
$statement .= " -out $WORKINGDATAPATH/" . $subj[$i] . "/DTI/data/nodif_2_struc.nii.gz ";
#print "$statement \n";

$statement  = " applywarp --in=$WORKINGDATAPATH/" . $subj[$i] . "/DTI/data/nodif_brain.nii.gz ";
$statement .= " --ref=$WORKINGDATAPATH/MNI152_T1_1mm.nii.gz ";
$statement .= " --premat=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/nodif_12dof_struc.mat ";
$statement .= " --warp=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/struc_warp_MNI_warpfield.nii.gz ";
$statement .= " --out=$WORKINGDATAPATH/" . $subj[$i] . "/DTI/data/nodif_2_MNI.nii.gz ";
#print "$statement \n";

$statement  = " convert_xfm ";
$statement .= " -omat $WORKINGDATAPATH/" . $subj[$i] . "/xfms/struc_12dof_nodif.mat ";
$statement .= " -inverse $WORKINGDATAPATH/" . $subj[$i] . "/xfms/nodif_12dof_struc.mat ";
#print "$statement \n";

$statement  = " convertwarp ";
$statement .= " --ref=$WORKINGDATAPATH/MNI152_T1_1mm_brain.nii.gz ";
$statement .= " --premat=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/nodif_12dof_struc.mat ";
$statement .= " --warp1=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/struc_warp_MNI_warpfield.nii.gz ";
$statement .= " --out=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/nodif_12dof_struc_warp_MNI_warpfield.nii.gz ";
print "$statement \n";

$statement  = " convertwarp ";
$statement .= " --ref=$WORKINGDATAPATH/" . $subj[$i] . "/DTI/data/nodif_brain_mask.nii.gz ";
$statement .= " --warp1=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/MNI_warp_struc_warpfield.nii.gz ";
$statement .= " --postmat=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/struc_12dof_nodif.mat ";
$statement .= " --out=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/MNI_warp_struc_12dof_nodif_warpfield.nii.gz ";
print "$statement \n";

$statement  = " probtrackx2 --pd --onewaycondition --omatrix2 ";
$statement .= " -s $WORKINGDATAPATH/" . $subj[$i] . "/DTI/data.bedpostX/merged "; 
$statement .= " -m $WORKINGDATAPATH/" . $subj[$i] . "/DTI/data/nodif_brain_mask.nii.gz ";
$statement .= " -x $WORKINGDATAPATH/ROIs/Human_" . $roi[$r] . "_" . $hemi[$h] . ".nii.gz ";
$statement .= " --target2=$WORKINGDATAPATH/MNI152_T1_1mm_brain_mask_downsample_2.nii.gz ";
$statement .= " -l -c 0.2 -S 2000 --steplength=0.5 -P 5000 --fibthresh=0.1 --randfib=0 ";  # check samples 
$statement .= " --xfm=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/MNI_warp_struc_12dof_nodif_warpfield.nii.gz ";
$statement .= " --invxfm=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/nodif_12dof_struc_warp_MNI_warpfield.nii.gz ";
$statement .= " --forcedir --opd ";
$statement .= " --dir=$OUTPUTDATAPATH/" . $subj[$i] . "_" . $roi[$r] . "_" . $hemi[$h] . "_Segmentation  ";
print "$statement \n";

}

