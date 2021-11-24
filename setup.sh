#!/bin/bash
runs="runs"
results="results"
data="data"
software="software"

echo -n "Detecting supported SIMD instruction set... "
simd=""
if grep -q avx2 /proc/cpuinfo; then
    simd="AVX2"
elif grep -q avx /proc/cpuinfo; then
    simd="AVX"
elif grep -q sse /proc/cpuinfo; then
    simd="SSE"
fi
echo "$simd"

echo -n "Detecting number of (physical) CPU cores... "
ncores=$(lscpu --parse=Core,Socket | grep --invert-match "^#" | sort --unique | wc --lines)
echo "$ncores"

echo "Cloning software..."
mkdir -p $software
cd $software

install_raxmlng() {
  git clone --recursive https://github.com/amkozlov/raxml-ng.git
  echo "Installing raxml-ng..."
  cd raxml-ng
  git checkout addc2a8b6ec0215daf77b2a22b43b400b8c2103d
  git submodule update --recursive
  mkdir -p build && cd build
  cmake -DUSE_MPI=ON ..
  make -j
  cd ../..
}

install_raxml() {
    git clone https://github.com/stamatak/standard-RAxML.git
    echo "Installing raxml..."
    cd standard-RAxML/
    make -j "$ncores" -f "Makefile.$simd.PTHREADS.gcc"
    mv "raxmlHPC-PTHREADS-$simd" "raxml"
    cd ..
}

install_modeltest() {
  git clone --recursive --branch dev https://github.com/ddarriba/modeltest.git
  echo "Installing modeltest..."
  cd modeltest
  mkdir -p build && cd build
  cmake -DUSE_MPI=ON ..
  make -j
  cd ../..
}

install_pargenes() {
  git clone --recursive https://github.com/BenoitMorel/ParGenes.git
  echo "Installing pargenes..."
  cd ParGenes
  ./install.sh 40
  cd ..
}

install_mptp() {
  git clone --recursive https://github.com/Pas-Kapli/mptp.git
  echo "Installing mptp..."
  cd mptp
  ./autogen.sh
  ./configure
  make
  cd ..
}

install_epa() {
  git clone --recursive https://github.com/Pbdas/epa-ng.git
  echo "Installing epa-ng..."
  cd epa-ng
  git checkout tags/v0.3.7
  make -j
  cd ..
}

install_papara() {
  echo "Installing papara..."
  mkdir papara
  cd papara
  wget https://cme.h-its.org/exelixis/resource/download/software/papara_nt-2.5-static_x86_64.tar.gz
  tar xzf papara_nt-2.5-static_x86_64.tar.gz
  ln -s papara_static_x86_64 papara
  cd -
}

install_genesis() {
  git clone --recursive https://github.com/lczech/genesis.git
  cd genesis
  git checkout e71a89704a87634ea84c1d15e80bafac234e0824
  echo "Installing genesis..."
  cd apps
  ln -s ../../../scripts/*.cpp .
  cd ..
  make -j 8
  make update -j 8
  cd ..
}

install_gappa() {
  git clone --recursive https://github.com/lczech/gappa.git
  echo "Installing gappa..."
  cd gappa
  git checkout tags/v0.6.0
  make -j
  cd ..
}

install_iqtree() {
  echo "Installing IQtree..."
  wget https://github.com/Cibiv/IQ-TREE/releases/download/v1.6.12/iqtree-1.6.12-Linux.tar.gz
  tar -xzf iqtree-1.6.12-Linux.tar.gz
  mv iqtree-1.6.12-Linux iqtree
  rm iqtree-1.6.12-Linux.tar.gz
}

install_root_digger(){
  echo "Installing RootDigger..."
  git clone --recursive https://github.com/computations/root_digger.git
  pushd root_digger
  make mpi -j
  popd
}

install_mafft() {
  echo "Installing mafft..."
  wget https://mafft.cbrc.jp/alignment/software/mafft-7.450-linux.tgz
  tar -xzf mafft-7.450-linux.tgz
  mv mafft-linux64 mafft
  rm mafft-7.450-linux.tgz
}

install_hmmer() {
  echo "Installing hmmer..."
  wget http://eddylab.org/software/hmmer/hmmer.tar.gz
  tar -xzf hmmer.tar.gz
  mv hmmer-* hmmer
  rm hmmer.tar.gz
  cd hmmer
  ./configure
  make -j
  cd -
}

install_raxmlng
install_raxml
install_modeltest
install_pargenes
install_mptp
install_epa
install_papara
install_genesis
install_gappa
install_iqtree
install_root_digger
install_mafft
install_hmmer


echo "Finished"
