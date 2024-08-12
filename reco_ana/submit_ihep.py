import os
import sys
import sample

### ### ### ### ### ### 
# usage: python submit_ihep.py run_name process_name
# run_name : a name of this run
# process_name : name of the process [see sample_dict in sampleconfig.py]
# analysis type : type (such as bbmm 4b not --bbmm)
### ### ### ### ### ### 

### ### ### ### ### ### 
# user inputs #
### ### ### ### ### ### 
runname = sys.argv[1]
procname = sys.argv[2]
nfileperjob = 10
### ### ### ### ### ### 
# end of user inputs #
### ### ### ### ### ### 

#
filelist,sampleID = sample.getfilelist(procname)
print('Total nb of files to process:{}'.format(len(filelist)))
n = nfileperjob
ifilelist = range(len(filelist))
ifilechunks = [ifilelist[i:i + n] for i in range(0, len(ifilelist), n)]
print('Break the whole list of files into {0} chunks with {1} files per job'.format(len(ifilechunks),n))
#
rootdir = os.getcwd()
jobdir = '{0}/job/'.format(rootdir)
#
_filectr = 0
for i in range(len(ifilechunks)):
  _ifiles = ifilechunks[i]
  ifiles = []
  for _d in _ifiles:
    ifiles.append( str(_d) )

#     hep_sub -g atlas -o run_m${m}_w${width}.out -e run_m${m}_w${width}.err -l run_m${m}_w${width}.log subbatch.sh -argu $TestArea $install_script $myoutdir $mytag $m $myinputfile $width -mem

  _jobid = '{0:06d}'.format(i)
  _jobdir = '{0}/{1}-{2}-{3}'.format(jobdir,runname,procname,_jobid)
  if os.path.exists(_jobdir):
    print('{0} exists. Please clean them! EXIT'.format(_jobdir))
    exit(1)
  _cmd = 'hep_sub eachjob.sh -o job/out.{3}-{4}-{5} -e job/err.{3}-{4}-{5} -argu {0} {1} {2} {6}'.format( _jobdir, procname, ','.join(ifiles), runname, procname, _jobid, rootdir )

  print('submitting job for {0} ... ... ...'.format(_jobdir))
  print('processing file indices:', ifiles)
  print(_cmd)

  os.system('mkdir -p {0}'.format(_jobdir))
  os.system(_cmd)

  _filectr += len(ifiles)

print('The above submissions expect to process {0} files'.format(_filectr))
