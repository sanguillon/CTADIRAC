"""
  Adapted job class to run tests in Prod3b conditions
  Wrapper on the Job class to handle Prod3 MC
  Paranal simulation with baseline layout, using zstd compression
  for simtel output files
			JB, March 2020
"""

__RCSID__ = "$Id$"
# generic imports
import json
import collections
# DIRAC imports
import DIRAC
# Base class
from Prod3MCPipeBaselineJob import Prod3MCPipeBaselineJob


class Prod3MCPipeBaselineJobC7(Prod3MCPipeBaselineJob):
  """ Job extension class for Prod3 MC NSB simulations,
      takes care of running corsika piped into simtel
      3 output files are created
      Most code is inherited from the Prod3MCPipeBaselineJob class
  """
  def __init__(self, cpuTime=259200):
    """ Constructor takes almosst everything from base class

    Keyword arguments:
    cpuTime -- max cpu time allowed for the job
    """
    Prod3MCPipeBaselineJob.__init__(self, cpuTime)
    self.package='corsika_simtelarray'
    self.version='2019-09-03'
    self.compiler='gcc48_default'


  def setupWorkflow(self, debug=False):
    """ Override the base class job workflow to adapt to NSB test simulations
        All parameters shall have been defined before that method is called.
    """
    # step 1 - debug only
    iStep = 1
    if debug:
        lsStep = self.setExecutable( '/bin/ls -alhtr', logFile = 'LS_Init_Log.txt' )
        lsStep['Value']['name']='Step%i_LS_Init'%iStep
        lsStep['Value']['descr_short']='list files in working directory'
        iStep+=1

        envStep = self.setExecutable( '/bin/env', logFile = 'Env_Log.txt' )
        envStep['Value']['name']='Step%i_Env'%iStep
        envStep['Value']['descr_short']='Dump environment'
        iStep+=1

    # step 2
    swStep = self.setExecutable( 'cta-prod-setup-software',
                              arguments='-p %s -v %s -a simulations -g %s'% (self.package, self.version, self.compiler),\
                              logFile='SetupSoftware_Log.txt')
    swStep['Value']['name'] = 'Step%i_SetupSoftware' % iStep
    swStep['Value']['descr_short'] = 'Setup software'
    iStep+=1

    # step 3
    if self.cta_site == 'Paranal':
        prod_script='./dirac_prod3_paranal_baseline'
    elif self.cta_site == 'LaPalma':
        prod_script='./dirac_prod3_lapalma_baseline'
    else:
        DIRAC.gLogger.error('Unknown site: %s'%self.cta_site)
        DIRAC.gLogger.error('No shell script associated')
        DIRAC.exit(-1)

    if 'gcc83' in self.compiler:
        prod_exe = './dirac_singularity_run'
        prod_args = '%s --start_run %s --run %s %s %s %s %s' % ( prod_script, self.start_run_number, self.run_number, \
                                           self.cta_site, self.particle, self.pointing_dir, self.zenith_angle )
    else:
        prod_exe = prod_script
        prod_args = '--start_run %s --run %s %s %s %s %s' % ( self.start_run_number, self.run_number, \
                                           self.cta_site, self.particle, self.pointing_dir, self.zenith_angle )

    csStep = self.setExecutable( prod_exe, arguments = prod_args, logFile='CorsikaSimtel_Log.txt')
    csStep['Value']['name']='Step%i_CorsikaSimtel'%iStep
    csStep['Value']['descr_short']='Run Corsika piped into simtel'
    iStep+=1

    # step 4 verify merged data
    mgvStep = self.setExecutable( 'cta-prod3-verifysteps', \
                              arguments = "generic %0d 100 '%s/Data/*.zst'"%\
                                          (self.N_output_files, self.inputpath),\
                              logFile='Verify_Simtel_Log.txt')
    mgvStep['Value']['name']='Step%i_VerifySimtel'%iStep
    mgvStep['Value']['descr_short'] = 'Verify simtel files'
    iStep += 1

    # step 5 - debug only
    if debug:
        lsStep=self.setExecutable('/bin/ls -Ralhtr',logFile='LS_End_Log.txt')
        lsStep['Value']['name']='Step%i_LS_End'%iStep
        lsStep['Value']['descr_short']='list files in working directory and sub-directory'
        iStep += 1

    # step 6
    # meta data
    # ## the order of the metadata dictionary is important, since it's used to build the directory structure
    metadata = collections.OrderedDict()
    metadata['array_layout'] = self.array_layout
    metadata['site'] = self.cta_site
    metadata['particle'] = self.particle
    if self.pointing_dir == 'North':
      metadata['phiP'] = 180
    if self.pointing_dir == 'South':
      metadata['phiP'] = 0
    metadata['thetaP'] = float( self.zenith_angle )
    metadata[self.program_category+'_prog'] = 'simtel'
    metadata[self.program_category+'_prog_version'] = self.version
    metadata['data_level'] = self.output_data_level
    metadata['configuration_id'] = self.configuration_id
    mdjson = json.dumps( metadata )

    # meta data field
    metadatafield = {'array_layout':'VARCHAR(128)', 'site':'VARCHAR(128)',
                     'particle':'VARCHAR(128)', 'phiP':'float',
                     'thetaP': 'float',
		             self.program_category+'_prog':'VARCHAR(128)',
		             self.program_category+'_prog_version':'VARCHAR(128)',
                     'data_level': 'int', 'configuration_id': 'int'}
    mdfieldjson = json.dumps( metadatafield )

    # register Data
    ## file meta data
    #filemetadata = {'runNumber': self.run_number, 'nsb':1}
    filemetadata = {'runNumber': self.run_number}
    file_md_json = json.dumps(filemetadata)
    outputpattern = './Data/sim_telarray/*/*/Data/*baseline*.simtel.zst'
    dmStep = self.setExecutable('../CTADIRAC/Core/scripts/cta-analysis-managedata.py',
                              arguments = "'%s' '%s' '%s' %s '%s' %s %s '%s'" %\
                              (mdjson, mdfieldjson, file_md_json, self.basepath,
                               outputpattern, self.package, self.program_category, self.catalogs),
                              logFile = 'Data_DataManagement_Log.txt')
    dmStep['Value']['name'] = 'Step%i_DataManagement_1' % iStep
    dmStep['Value']['descr_short'] = 'Save data files to SE and register them in DFC'
    iStep += 1
    ## log file
    outputpattern = './Data/sim_telarray/*/*/Log/*baseline*.log.gz'
    dmStep = self.setExecutable('../CTADIRAC/Core/scripts/cta-analysis-managedata.py',
                              arguments = "'%s' '%s' '%s' %s '%s' %s %s '%s' Log" % \
                              (mdjson, mdfieldjson, file_md_json, self.basepath,
                               outputpattern, self.package, self.program_category, self.catalogs),
                              logFile = 'Log_DataManagement_Log.txt')
    dmStep['Value']['name'] = 'Step%i_Log_DataManagement' % iStep
    dmStep['Value']['descr_short'] = 'Save log files to SE and register them in DFC'
    iStep += 1
    ## histogram
    outputpattern = './Data/sim_telarray/*/*/Histograms/*baseline*.hdata.gz'
    dmStep = self.setExecutable('../CTADIRAC/Core/scripts/cta-analysis-managedata.py',
                              arguments = "'%s' '%s' '%s' %s '%s' %s %s '%s' Histograms" % \
                              (mdjson, mdfieldjson, file_md_json, self.basepath,
                               outputpattern, self.package, self.program_category, self.catalogs),
                              logFile = 'Histo_DataManagement_Log.txt')
    dmStep['Value']['name'] = 'Step%i_Histo_DataManagement' % iStep
    dmStep['Value']['descr_short'] = 'Save hitograms files to SE and register them in DFC'
    iStep += 1

    # Number of showers is passed via an environment variable
    self.setExecutionEnv( {'NSHOW'        : '%s' % self.nShower} )
