Make a selection of 150 magnitude (height).

    zoom_starsom = [s for s in starsom if 150 <= s.X2d < (150 + 150*math.sqrt(2)) and 150 <= s.Y2d < 300]
    
Offset them:

    for star in zoom_starsom:
        star.X2d -= 150
        star.Y2d -= 150
        
Gives these stats:

    Mean:	0.528675303392
    Median:	0.259453017648
    StdDev:	1.10351291833
    
    Histogram:
    
                 0.0 : **************************************************
                 0.1 : *********************************************
                 0.2 : *************************
                 0.3 : ************************
                 0.4 : *******************
                 0.5 : ***********
                 0.6 : ********
                 0.7 : ******
                 0.8 : *****
                 0.9 : ***

