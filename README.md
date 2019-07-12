# subtomogram_averaging

```console
sbatch \
    --gres=lscratch:2 \
    --cpus-per-task=4 \
    --mem=4g \
    --time=1440 \
    submit_peet.sh \
        --initMOTL=3 \
        --dPhi='\{-180:10:180,-30:5:30,-15:3:15,-7.5:1:7.5\}' \
        --dTheta='\{0:1:0,-30:5:30,-15:3:15,-7.5:1:7.5\}' \
        --dPsi='\{0:1:0,-30:5:30,-15:3:15,-7.5:1:7.5\}' \
        --searchRadius='\{[8],[4],[4],[2]\}' \
        --lowCutoff='\{[0,0.05],[0,0.05],[0,0.05],[0,0.05]\}' \
        --hiCutoff='\{[1.0,0.05],[1.0,0.05],[1.0,0.05],[1.0,0.05]\}' \
        --refThreshold='\{4,4,4,4\}' \
        --duplicateShiftTolerance='[NaN,NaN,NaN,NaN]' \
        --duplicateAngularTolerance='[NaN,NaN,NaN,NaN]' \
        --reference='[1,38]' \
        --szVol='[20,20,20]' \
        --alignedBaseName="\'aligned\'" \
        --lstThresholds='[25:25:100,107]' \
        --refFlagAllTom=0 \
        --lstFlagAllTom=0 \
        --particlePerCPU=1 \
        --sampleSphere="\'full\'" \
        --sampleInterval=20 \
        --maskType="\'sphere\'" \
        --outsideMaskRadius=25 \
        161114_full_nucleus.nrrd \
        161114_G_1.fcsv \
        161114_G_2.fcsv \
        161114_R_1.fcsv \
        161114_R_2.fcsv \
        161114_Y_1.fcsv \
        161114_Y_2.fcsv
```
