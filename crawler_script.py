import booking_crawler as b

cities = open('cities.txt').readlines();

#Do this task for multiple languages in a separate file
for language in ['nl','fr','de','es','en']:

    o = open('output_'+language+'.txt','w',1);
    o.write('Review number\tLanguage\tHotel\tHotel stars\tHotel city\tHotel country\tReviewer\tReviewer location\tReviewer type\tPositive\tNegative\tRating\n');

    #Go through all the cities in the list
    for city in cities:
        city = b.City(city.strip());
        hotels = city.get_hotels();

        #Go through all hotels in the city
        for hotel in hotels:

            #Only 3 star hotels
            if hotel.stars == 3:
        
                reviews = hotel.get_reviews(language);
                
                for n,r in enumerate(reviews):

                    #Only very specific reviews
                    if (r.rating > 9.8 or r.rating < 5) and \
                        (b.count_words(r.comment_good) > 25 or b.count_words(r.comment_bad) > 25):
                            o.write(str(n+1)+'\t'+language+'\t'+r.hotel.name+'\t'+str(r.hotel.stars)+'\t'+r.hotel.city.name+'\t'+r.hotel.country+'\t'+r.poster+'\t'+r.poster_location+'\t'+r.poster_type+'\t'+str(r.comment_good)+'\t'+str(r.comment_bad)+'\t'+str(r.rating)+'\n');
                    else:
                        continue;
            else:
                print('Wrong stars')
                continue;
