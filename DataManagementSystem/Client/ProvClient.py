""" Class that contains client access to the Provenance DB handler. """

__RCSID__ = "$Id$"

# # from DIRAC
from DIRAC.Core.Base.Client import Client


class ProvClient(Client):
    """
    Exposes the available functions
    in the DataManagementSystem/ProvenanceManagerHandler
    """

    def __init__(self, url=None, **kwargs):
        """ Simple constructor """
        Client.__init__(self, **kwargs)
        res = self.serverURL = \
            'DataManagement/ProvenanceManager' if not url else url

    def addActivity(self, row):
        """ Asks for adding an Activity """
        res = row.toJSON()
        rowJSON = res['Value']
        rpcClient = self._getRPC()
        print rowJSON
        return rpcClient.addActivity(rowJSON)

    def addDatasetEntity(self, row):
        """ Asks for adding a DatasetEntity """
        res = row.toJSON()
        rowJSON = res['Value']
        rpcClient = self._getRPC()
        print rowJSON
        return rpcClient.addDatasetEntity(rowJSON)

    def addValueEntity(self, row):
        """ Asks for adding a ValueEntity """
        res = row.toJSON()
        rowJSON = res['Value']
        rpcClient = self._getRPC()
        print rowJSON
        return rpcClient.addValueEntity(rowJSON)

    def addUsed(self, row):
        """ Asks for adding a Used relation """
        res = row.toJSON()
        rowJSON = res['Value']
        rpcClient = self._getRPC()
        print rowJSON
        return rpcClient.addUsed(rowJSON)

    def addWasGeneratedBy(self, row):
        """ Asks for adding a WasGeneratedBy relation """
        res = row.toJSON()
        rowJSON = res['Value']
        rpcClient = self._getRPC()
        print rowJSON
        return rpcClient.addWasGeneratedBy(rowJSON)

    def addAgent(self, row):
        """ Asks for adding an Agent """
        res = row.toJSON()
        rowJSON = res['Value']
        rpcClient = self._getRPC()
        print rowJSON
        return rpcClient.addAgent(rowJSON)

    def addWasAttributedTo(self, row):
        """ Asks for adding a WasAttributedTo relation """
        res = row.toJSON()
        rowJSON = res['Value']
        rpcClient = self._getRPC()
        print rowJSON
        return rpcClient.addWasAttributedTo(rowJSON)

    def addWasAssociatedWith(self, row):
        """ Asks for adding a WasAssociatedWith relation """
        res = row.toJSON()
        rowJSON = res['Value']
        rpcClient = self._getRPC()
        print rowJSON
        return rpcClient.addWasAssociatedWith(rowJSON)

    def addActivityDescription(self, row):
        """ Asks for adding an ActivityDescription """
        res = row.toJSON()
        rowJSON = res['Value']
        rpcClient = self._getRPC()
        print rowJSON
        return rpcClient.addActivityDescription(rowJSON)

    def addDatasetDescription(self, row):
        """ Asks for adding a DatasetDescription """
        res = row.toJSON()
        rowJSON = res['Value']
        rpcClient = self._getRPC()
        print rowJSON
        return rpcClient.addDatasetDescription(rowJSON)

    def addUsageDescription(self, row):
        """ Asks for adding a UsageDescription relation """
        res = row.toJSON()
        rowJSON = res['Value']
        rpcClient = self._getRPC()
        print rowJSON
        return rpcClient.addUsageDescription(rowJSON)

    def addGenerationDescription(self, row):
        """ Asks for adding a GenerationDescription relation """
        res = row.toJSON()
        rowJSON = res['Value']
        rpcClient = self._getRPC()
        print rowJSON
        return rpcClient.addGenerationDescription(rowJSON)

    def addValueDescription(self, row):
        """ Asks for adding an ValueDescription """
        res = row.toJSON()
        rowJSON = res['Value']
        rpcClient = self._getRPC()
        print rowJSON
        return rpcClient.addValueDescription(rowJSON)

    def addWasConfiguredBy(self, row):
        """ Asks for adding a WasConfiguredBy relation """
        res = row.toJSON()
        rowJSON = res['Value']
        rpcClient = self._getRPC()
        print rowJSON
        return rpcClient.addWasConfiguredBy(rowJSON)

    def addParameter(self, row):
        """ Asks for adding a Parameter """
        res = row.toJSON()
        rowJSON = res['Value']
        rpcClient = self._getRPC()
        print rowJSON
        return rpcClient.addParameter(rowJSON)

    def addConfigFile(self, row):
        """ Asks for adding a ConfigFile """
        res = row.toJSON()
        rowJSON = res['Value']
        rpcClient = self._getRPC()
        print rowJSON
        return rpcClient.addConfigFile(rowJSON)

    def addParameterDescription(self, row):
        """ Asks for adding a ParameterDescription """
        res = row.toJSON()
        rowJSON = res['Value']
        rpcClient = self._getRPC()
        print rowJSON
        return rpcClient.addParameterDescription(rowJSON)

    def addConfigFileDescription(self, row):
        """ Asks for adding a ConfigFileDescription """
        res = row.toJSON()
        rowJSON = res['Value']
        rpcClient = self._getRPC()
        print rowJSON
        return rpcClient.addConfigFileDescription(rowJSON)

    def getAgents(self):
        """ Asks for getting Agents"""
        rpcClient = self._getRPC()
        return rpcClient.getAgents()

    def getAgentKey(self, agent_id):
        """ Asks for getting Agent internal_key"""
        rpcClient = self._getRPC()
        return rpcClient.getAgentKey(agent_id)

    def getUsageDescription(self, activityDescription_id, role):
        """ Asks for getting UsageDescription internal_key"""
        rpcClient = self._getRPC()
        return rpcClient.getUsageDescription(activityDescription_id, role)

    def getParameterDescription(self, activityDescription_id, parameter_name):
        """ Asks for getting ParameterDescription internal_key"""
        rpcClient = self._getRPC()
        return rpcClient.getParameterDescription(activityDescription_id,
                                                 parameter_name)

    def getConfigFileDescription(self, activityDescription_id,
                                 configFile_name):
        """ Asks for getting ConfigFileDescription internal_key"""
        rpcClient = self._getRPC()
        return rpcClient.getConfigFileDescription(activityDescription_id,
                                                  configFile_name)

    def getActvityDescriptionKey(self, activityDescription_name,
                                 activityDescription_version):
        """ Asks for getting ActivityDescription internal_key"""
        rpcClient = self._getRPC()
        return rpcClient.getActivityDescriptionKey(activityDescription_name,
                                                   activityDescription_version)
