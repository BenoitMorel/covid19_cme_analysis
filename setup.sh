# Install all dependencies for the pipeline

software="software"

echo "Cloning software..."
mkdir -p $software
cd $software
git clone --recursive https://github.com/BenoitMorel/ParGenes.git
git clone --recursive --branch dev https://github.com/ddarriba/modeltest.git 
git clone --recursive https://github.com/amkozlov/raxml-ng.git
git clone --recursive https://github.com/Pas-Kapli/mptp.git
git clone --recursive https://github.com/Pbdas/epa-ng.git
git clone https://github.com/lczech/genesis.git

install_raxmlng() {
  echo "Installing raxml-ng..."
  cd raxml-ng
  mkdir -p build && cd build
  cmake -DUSE_MPI=ON ..
  make -j
  cd ../..
}

install_modeltest() {
  echo "Installing modeltest..."
  cd modeltest
  mkdir -p build && cd build
  cmake -DUSE_MPI=ON ..
  make -j
  cd ../..
}

install_pargenes() {
  echo "Installing pargenes..."
  cd ParGenes
  ./install.sh 40
  cd ..
}

install_mptp() {
  echo "Installing mptp..."
  cd mptp 
  ./autogen.sh
  ./configure
  make
  cd ..
}

install_epa() {
  echo "Installing epa-ng..."
  cd epa-ng
  make -j
  cd ..
}

install_genesis() {
  echo "Installing genesis..."
  cd genesis/apps
  ln -s ../../../scripts/*.cpp .
  cd ..
  make -j
  make update -j
  cd ..
}

install_iqtree() {
  echo "Installing IQtree..."
  wget https://github.com/Cibiv/IQ-TREE/releases/download/v1.6.12/iqtree-1.6.12-Linux.tar.gz
  tar -xzf iqtree-1.6.12-Linux.tar.gz
  mv iqtree-1.6.12-Linux iqtree
  rm iqtree-1.6.12-Linux.tar.gz
}

install_raxmlng
install_modeltest
install_pargenes
install_mptp
install_epa
install_genesis
install_iqtree


echo "Finished"
