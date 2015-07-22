""" Prod3 MC Script to create a Transformation
         prod3.py JB, LA 2015
"""

from DIRAC.Core.Base import Script
Script.setUsageMessage( '\n'.join( [ __doc__.split( '\n' )[1],
                                     'Usage:',
                                     '  %s array_layout site particle pointing_dir zenith_angle nShower' % Script.scriptName,
                                     'Arguments:',
                                     '  array_layout: hex or square',
                                     '  site: Paranal, Aar, Armazones_2K',
                                     '  particle: gamma, proton, electron',
                                     '  pointing_dir: North or South',
                                     '  zenith_agle: 20',
                                     '  nShower: from 5 to 25000',
                                     '\ne.g: %s hex Paranal gamma South 20 5'% Script.scriptName,
                                     ] ) )

Script.parseCommandLine()

import DIRAC
from DIRAC.TransformationSystem.Client.Transformation import Transformation
from DIRAC.Core.Workflow.Parameter import Parameter
from CTADIRAC.Interfaces.API.Prod3MCJob import Prod3MCJob
from DIRAC.Interfaces.API.Dirac import Dirac

def submitTS( job ):
  """ Create a transformation executing the job workflow  """
  # ## send jobs to Lyon
  #job.setDestination( 'LCG.IN2P3-CC.fr' )

  ### Temporary fix to initialize JOB_ID and PRODUCTION_ID #######
  job.workflow.addParameter( Parameter( "JOB_ID", "000000", "string", "", "", True, False, "Temporary fix" ) )
  job.workflow.addParameter( Parameter( "PRODUCTION_ID", "000000", "string", "", "", True, False, "Temporary fix" ) )

  t = Transformation()
  # t.setTransformationName( "Prod3Exemple" )  # This must be unique. If not set it's asked in the prompt
  t.setType( "MCSimulation" )
  t.setDescription( "MC prod3 example" )
  t.setLongDescription( "corsika-simtel production" )  # mandatory
  t.setBody ( job.workflow.toXML() )

  res = t.addTransformation()  # Transformation is created here

  if not res['OK']:
    print res['Message']
    DIRAC.exit( -1 )

  t.setStatus( "Active" )
  t.setAgentType( "Automatic" )
  
  return res

def submitWMS( job ):
  """ Submit the job locally or to the WMS  """
# job.setDestination( 'LCG.IN2P3-CC.fr' )
  dirac = Dirac()
  res = dirac.submit( job, "local" )
# res = dirac.submit( job )

  Script.gLogger.notice( 'Submission Result: ', res )
  return res

#########################################################

def runProd3( args = None ):
  """ Simple wrapper to create a Prod3MCJob and setup parameters
      from positional arguments given on the command line.
      
      Parameters:
      args -- a list of 6 strings corresponding to job arguments
              array_layout site particle pointing_dir zenith_angle nShower             
  """
  # get arguments
  layout = args[0]
  site = args[1]
  particle = args[2]
  pointing = args[3]
  zenith = args[4]
  nShower= args[5]
  mode = 'TS'
  if len( args ) == 7:
    mode = args[6]
  
    ### Main Script ###
  job = Prod3MCJob()

  # override for testing
  job.setName('Prod3Test_%s'%particle)
  
  # package and version
  job.setPackage('corsika_simhessarray')
  job.setVersion('2015-07-21')

  # layout, site, particle, pointing direction, zenith angle
  # hex,  Paranal,  gamma, South,  20
  job.setArrayLayout(layout)
  job.setSite(site)
  job.setParticle(particle)
  job.setPointingDir(pointing)
  job.setZenithAngle( zenith )

  # 5 is enough for testing
  job.setNShower(nShower)

  # set run number:
  job.setRunNumber( 00000003 )

  job.setOutputSandbox( ['*Log.txt'] )

  # add the sequence of executables
  job.setupWorkflow()

  # debug
  Script.gLogger.info( job.workflow )
  
  if mode == 'TS':
    # set run number: JOB_ID variable left for dynamic resolution during the Job. It corresponds to the Task_ID
    job.setRunNumber( '@{JOB_ID}' )
    res = submitTS( job )
  elif mode == 'WMS':
    res = submitWMS( job )
  else:
    Script.showHelp()
    
  return res

#########################################################
if __name__ == '__main__':

  args = Script.getPositionalArgs()
  if ( len( args ) not in [6,7] ):
    Script.showHelp()
  try:
    res = runProd3( args )
    if not res['OK']:
      DIRAC.gLogger.error ( res['Message'] )
      DIRAC.exit( -1 )
    else:
      DIRAC.gLogger.notice( 'Done' )
  except Exception:
    DIRAC.gLogger.exception()
    DIRAC.exit( -1 )
