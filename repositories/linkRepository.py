class LinkRepository:
    def __init__(self, neuronRepository, connectionsService, association):
        self.neuronRepository = neuronRepository
        self.connectionsService = connectionsService
        self.association = association
        self.links = {}

    def addOrGetLink(self, linkTo, unit, linkType):
        # get or add link to group
        if(linkTo in self.links):
            linkGroup = self.links[linkTo]
        else:
            linkGroup = {}
            self.links[linkTo] = linkGroup
        
        # get or add link type group
        if(linkType in linkGroup):
            linkGroup = linkGroup[linkType]
        else:
            linkGroup[linkType] = {}
            linkGroup = linkGroup[linkType]

        if(unit in linkGroup):
            return linkGroup[unit]
        else:
            ca = self.neuronRepository.addCA()
            linkGroup[unit] = ca
            amCA = self.association.caFromUnit(unit)
            
            if(linkType == "correlate"):
                self.connectionsService.connectCorrelatedLink(ca, amCA)
            elif(linkType == "query"):
                self.connectionsService.connectQueryableLink(ca, amCA)
            elif(linkType == "stimulate"):
                self.connectionsService.connectStimulatedLink(ca, amCA)
            else:
                raise Exception("Invalid Link Type: {}. Supported values: correlate, query and stimulate.".format(linkType))

            return ca

    def get(self):
        return self.links.copy()