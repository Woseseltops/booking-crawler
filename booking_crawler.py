import urllib.request

def get(url):
    """Acts like Mozilla Firefox asks for a page""";
    
    r = urllib.request.Request(url,headers={'User-agent':'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'});    
    return str(urllib.request.urlopen(r).read());

def get_text_between(text,border_left,border_right):

    return text.split(border_left)[1].split(border_right)[0];

class City():

    def __init__(self,name):

        self.name = name;
        self.id = self._get_city_id();

    def _get_city_id(self):
        """Transforms a city name to a booking.com city id""";

        searchpage = get('http://www.booking.com/searchresults.html?src=index&nflt=&error_url=http%3A%2F%2Fwww.booking.com%2Findex.en-gb.html%3Fsid%3Debf463cfc313cfe4089c1cef5d42de23%3Bdcid%3D1%3B&dcid=1&lang=en-gb&sid=ebf463cfc313cfe4089c1cef5d42de23&si=ai%2Cco%2Cci%2Cre%2Cdi&dest_type_filter=all&ss='+self.name+'&checkin_monthday=0&checkin_year_month=0&checkout_monthday=0&checkout_year_month=0&idf=on&org_nr_rooms=1&org_nr_adults=2&org_nr_children=0');
        raw_id = searchpage.split('city=-')[1][:7];
        return raw_id.split(';')[0];

    def get_hotels(self):
        """Returns a list of hotel objects for this city""";

        searchpage = get('http://www.booking.com/searchresults.en-gb.html?sid=ebf463cfc313cfe4089c1cef5d42de23;dcid=1;class_interval=1;csflt=%7B%7D;dtdisc=0;idf=1;inac=0;interval_of_time=undef;offset=0;redirected_from_city=0;redirected_from_landmark=0;remth=0;review_score_group=empty;score_min=0;si=ai%2Cco%2Cci%2Cre%2Cdi;src=index;ss_all=0;;city=-'+self.id+';origin=disamb;srhash=1563581011;srpos=1');

        hotelcodes = searchpage.split('class="hotel_name_link url')[1:];

        hotels = [];

        for i in hotelcodes:
            code = get_text_between(i,'href="/hotel/','.en-gb.html?');
            country,name = code.split('/');            

            try:
                hotels.append(Hotel(name,self,country));
            except:
                print('Hotelcreation failed');
        return hotels;

class Hotel():

    def __init__(self,name,city,country):

        self.name = name;
        self.city = city;
        self.country = country;
        self.stars = self._get_stars();

    def _get_stars(self):

        hotelpage = get('http://www.booking.com/hotel/'+self.country+'/'+self.name+'.html');
        actual_page = hotelpage.split('hp_hotel_name')[1];

        try:
            stars = int(get_text_between(actual_page,'title="','-star hotel"'))
        except ValueError: #Sometimes the stars are estimated
            stars = 0;

        return stars;

    def get_reviews(self,lang):
        """Returns a list of comment objects for this hotel""";

        offset = -25;
        reviews = [];

        while True:
            offset += 25;
            print(offset,self.name,lang);

            try:
                hotelpage = get('http://www.booking.com/reviewlist.'+lang+'.html?cc1='+self.country+';pagename='+self.name+';offset='+str(offset));
            except urllib.error.HTTPError:
                break;
    
            if 'review_tr' not in hotelpage:
                break;

            reviewcodes = hotelpage.split('review_tr')[1:];

            def filter_out_comment(text,classname):

                try:
                    text = text.split(classname)[1];
                except IndexError:
                    return None;

                text = get_text_between(text,'">','</p>');

                return text.replace('\n','   ');

            for i in reviewcodes:
                comment_good = filter_out_comment(i,'comments_good');
                comment_bad = filter_out_comment(i,'comments_bad');

                poster = i.split('cell_user_name')[1];
                poster = get_text_between(poster,'">','</div>')[2:-2].strip();

                poster_type = get_text_between(i,'<div class="cell_user_profile">','</div>');

                try:
                    poster_city = get_text_between(i,'<span class="locality" style="text-transform: capitalize">','</span');
                except IndexError:
                    poster_city = '';
                    
                poster_country = get_text_between(i,'<span class="country-name">','</span>');
                date = get_text_between(i,'<span class="cell_user_date">','</span>');
                rating = get_text_between(i,'<span>','</span>');
              
                reviews.append(Review(comment_good,comment_bad,poster,poster_type,poster_city + ', ' + poster_country,rating,date,self,lang));

        return reviews;

class Review():

    def __init__(self,comment_good,comment_bad,poster,poster_type,poster_location,rating,date,hotel,lang):

        self.comment_good = iso_to_utf(comment_good);
        self.comment_bad = iso_to_utf(comment_bad);
        self.poster = iso_to_utf(poster);
        self.poster_type = iso_to_utf(poster_type);
        self.poster_location = iso_to_utf(poster_location);
        self.rating = float(rating);
        self.date = date;
        self.lang = lang;
        self.hotel = hotel;

def count_words(text):

    try:
        return (len(text.split()));
    except AttributeError: #Can handle None values
        return 0;

def iso_to_utf(text):

    try:
        return text.encode('iso-8859-1').decode();
    except AttributeError: #Can handle None values
        return text;
