def get_options():
    # Define brands
    brands = [
        ['BUD CHELADA','Bud Chelada'],
        ['BUD LIGHT','Bud Light'],
        ['BUD LIGHT LIME','Bud Light Lime'],
        ['BUD LIGHT PLATINUM','Bud Light Platinum'],
        ['BUD LIGHT RITA','Bud Light Rita'],
        ['BUDWEISER','Budweiser']
    ]

    # Define sizes
    sizes = [
        ['BUD CHELADA','15/25','Package Beer'],
        ['BUD CHELADA','24/12','Package Beer'],
        ['BUD CHELADA','24/8','Package Beer'],
        ['BUD CHELADA','48/8','Package Beer'],
        ['BUD LIGHT','15/25','Package Beer'],
        ['BUD LIGHT','18/12','Package Beer'],
        ['BUD LIGHT','20/12','Package Beer'],
        ['BUD LIGHT','20/16','Package Beer'],
        ['BUD LIGHT','24/12','Package Beer'],
        ['BUD LIGHT LIME','15/22','Package Beer'],
        ['BUD LIGHT LIME','15/25','Package Beer'],
        ['BUD LIGHT LIME','18/12','Package Beer'],
        ['BUD LIGHT LIME','24/12','Package Beer'],
        ['BUD LIGHT PLATINUM','15/22','Package Beer'],
        ['BUD LIGHT PLATINUM','15/25','Package Beer'],
        ['BUD LIGHT PLATINUM','18/12','Package Beer'],
        ['BUD LIGHT PLATINUM','24/12','Package Beer'],
        ['BUD LIGHT RITA','15/25','Package Beer'],
        ['BUD LIGHT RITA','24/8','Package Beer'],
        ['BUDWEISER','15/25','Package Beer'],
        ['BUDWEISER','18/12','Package Beer'],
        ['BUDWEISER','20/12','Package Beer'],
        ['BUDWEISER','20/16','Package Beer'],
        ['BUDWEISER','24/12','Package Beer'],
    ]

    # Define months
    months = [
        [0,'January'],
        [1,'February'],
        [2,'March'],
        [3,'April'],
        [4,'May'],
        [5,'June'],
        [6,'July'],
        [7,'August'],
        [8,'September'],
        [9,'October'],
        [10,'November'],
        [11,'December']
    ]

    # Return data
    return {
        'brands': brands,
        'sizes': sizes,
        'months': months
    }