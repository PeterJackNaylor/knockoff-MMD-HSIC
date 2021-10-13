echo "DATASET,AM,alpha,n_1,d,normalise,kernel,k0,fdr,features" >mnist_full.csv

for AM in DC TR pearson_correlation HSIC MMD PC
do
    python ../../src/model/knock-off.py --d 100 --xy Xy_mnist.npz --t $AM --n_1 0.3 --param "DATASET=mnist_full" --kernel gaussian
    tail -n +2 fdr.csv >>mnist_full.csv
done
