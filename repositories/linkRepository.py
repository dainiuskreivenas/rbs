class LinkRepository:
    def __init__(self, neuronRepository, connectionsService, baseService, propertyService, relationshipService):
        self.__neuronRepository = neuronRepository
        self.__connectionsService = connectionsService
        self.__baseService = baseService
        self.__propertyService = propertyService
        self.__relationshipService = relationshipService
        self.__links = {}

    def addOrGetLink(self, linkTo, unit, linkType):
        # get or add link to group
        if(linkTo in self.__links):
            linkGroup = self.__links[linkTo]
        else:
            linkGroup = {}
            self.__links[linkTo] = linkGroup
        
        # get or add link type group
        if(linkType in linkGroup):
            linkGroup = linkGroup[linkType]
        else:
            linkGroup[linkType] = {}
            linkGroup = linkGroup[linkType]

        if(unit in linkGroup):
            return linkGroup[unit]
        else:
            ca = self.__neuronRepository.addCA()
            linkGroup[unit] = ca

            if(linkTo == "base"):
                amCA = self.__baseService.caFromUnit(unit)
            elif(linkTo == "property"):
                amCA = self.__propertyService.caFromUnit(unit)
            elif(linkTo == "relationship"):
                amCA = self.__relationshipService.caFromUnit(unit)
            
            if(linkType == "correlate"):
                self.__connectionsService.connectCorrelatedLink(ca, amCA)
            elif(linkType == "query"):
                self.__connectionsService.connectQueryableLink(ca, amCA)
            elif(linkType == "stimulate"):
                self.__connectionsService.connectStimulatedLink(ca, amCA)
            else:
                raise Exception("Invalid Link Type: {}. Supported values: correlate, query and stimulate.".format(linkType))

            return ca

    def get(self):
        return self.__links.copy()
