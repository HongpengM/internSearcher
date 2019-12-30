from scrapy import Field, Item

class Vacancy(Item):

    database = 'Vacancy'

    # In database time
    createdAt = Field()
    
    # Last available date
    lastADate = Field()

    # ---- Above no need to fill
    #
    publishedAt = Field()

    #
    title = Field()

    #
    employer = Field()

    # Region of the program
    region = Field()

    # Cities of the program
    cities = Field()

    # Job Description
    jd = Field()

    #
    links = Field()

    # Send resume etc to this email
    email = Field()

    # program type
    pType = Field()

    # Length
    pLength = Field()

    #
    otherKeyInfo = Field()

