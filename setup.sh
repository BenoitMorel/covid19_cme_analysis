
runs="runs"
results="results"
data="data"
software="software"

echo "Creating directories..."
mkdir -p $runs
mkdir -p $results
mkdir -p $data
mkdir -p $software


echo "Cloning software..."
cd $software
git clone --recursive https://github.com/BenoitMorel/ParGenes.git
git clone --recursive --branch dev https://github.com/ddarriba/modeltest.git 
git clone --recursive https://github.com/amkozlov/raxml-ng.git
git clone --recursive https://github.com/Pas-Kapli/mptp.git

echo "Installing raxml-ng..."
cd raxml-ng
mkdir build && cd build
cmake -DUSE_MPI=ON ..
make -j
cd ../..

echo "Installing modeltest..."
cd modeltest
mkdir build && cd build
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


