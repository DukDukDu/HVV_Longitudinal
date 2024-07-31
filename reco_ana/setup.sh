if [[ $HOSTNAME == *"ihep.ac.cn"* ]]; then

  echo "IHEP setup"
  # my delphes was compiled with this version of root
  #source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.20.06/x86_64-centos7-gcc48-opt/bin/thisroot.sh
  #export PATH=/afs/ihep.ac.cn/users/s/sunxh/publicfs/chain/Delphes-3.4.2/:$PATH
  #export LD_LIBRARY_PATH=/afs/ihep.ac.cn/users/s/sunxh/publicfs/chain/Delphes-3.4.2/:$LD_LIBRARY_PATH
  #export CPATH=/afs/ihep.ac.cn/users/s/sunxh/publicfs/chain/Delphes-3.4.2/external/:$CPATH
  #
  export PATH=/publicfs/cms/user/mingxuanzhang/simulation_software/Delphes-3.5.0/:$PATH
  export LD_LIBRARY_PATH=/publicfs/cms/user/mingxuanzhang/simulation_software/Delphes-3.5.0/:/publicfs/cms/user/mingxuanzhang/simulation_software/Pythia8/lib/:$LD_LIBRARY_PATH
  export CPATH=/publicfs/cms/user/mingxuanzhang/simulation_software/Delphes-3.5.0/external/:$CPATH

else

  echo "PKU setup"
  # defaul now: pku machines
  source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.20.06/x86_64-centos7-gcc48-opt/bin/thisroot.sh
  export PATH=/home/pku/sunxh/chain/Delphes-3.5.0/:$PATH
  export LD_LIBRARY_PATH=/home/pku/sunxh/chain/Delphes-3.5.0/:/home/pku/sunxh/chain/Delphes-3.5.0/PYTHIA8/lib/:$LD_LIBRARY_PATH
  export CPATH=/home/pku/sunxh/chain/Delphes-3.5.0/external/:$CPATH

fi

