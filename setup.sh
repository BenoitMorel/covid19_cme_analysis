
runs="runs"
results="results"
data="data"
software="software"



echo "Cloning software..."
mkdir -p $software
cd $software
git clone --recursive https://github.com/BenoitMorel/ParGenes.git
git clone --recursive --branch dev https://github.com/ddarriba/modeltest.git 
git clone --recursive https://github.com/amkozlov/raxml-ng.git
git clone --recursive https://github.com/Pas-Kapli/mptp.git
git clone --recursive https://github.com/Pbdas/epa-ng.git

echo "Installing raxml-ng..."
cd raxml-ng
mkdir -p build && cd build
cmake -DUSE_MPI=ON ..
make -j
cd ../..

echo "Installing modeltest..."
cd modeltest
mkdir -p build && cd build
cmake -DUSE_MPI=ON ..
make -j
cd ../..

echo "Installing pargenes..."
cd ParGenes
./install.sh
cd ..

echo "Installing mptp..."
cd mptp 
./autogen.sh
./configure
make
cd ..

echo "Installing epa-ng..."
cd epa-ng
make -j
cd ..
