from scrapy import Field, Item

class Vacancy(Item):

    database = 'Vacancy'

    # Collections in database 'Intern' / 'Fulltime' / 'Other'
    collections = Field()
    
    # In database time
    createdAt = Field()
    
    # Last available date
    lastSeenDate = Field()

    # ---- Above no need to fill
    #
    publishedAt = Field()

    # !!MUST
    title = Field()

    # !!MUST
    employer = Field()

    # Region of the program
    region = Field()

    # Cities of the program
    cities = Field()

    # !!MUST Job Description
    jd = Field()

    #
    links = Field()

    # Send resume etc to this email
    email = Field()

    # program type
    pType = Field()

    # Length
    pLength = Field()

    # Education Level
    education = Field()


    # business Unit
    businessUnit = Field()

    #
    otherKeyInfo = Field()

