echo "DATASET,AM,alpha,n_1,d,normalise,kernel,k0,fdr,features" >brca_cds.csv
echo "AM,feature,wj" >wjs_brca_cds.csv

for AM in TR HSIC MMD
do
    python ../../src/model/knock-off.py --d 100 --xy Xy_brca_cds.npz --t $AM --n_1 0.3 --param "DATASET=brca_cds" --kernel gaussian
    tail -n +2 fdr.csv >>brca_cds.csv
    tail -n +2 wjs.csv >>wjs_brca_cds.csv
done
