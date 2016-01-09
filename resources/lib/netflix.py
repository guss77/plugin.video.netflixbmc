__author__ = 'corona'

class urls:
    netflix = "https://www.netflix.com"

    home              = netflix+"/WiHome"
    login             = netflix+"/Login"
    # mylist            = netflix+"/MyList?leid=595&link=seeall"
    mylist            = netflix+"/browse/my-list"
    recent            = netflix+"/WiRecentAdditionsGallery?nRR=releaseDate&nRT=all&pn=1&np=1&actionMethod=json"
    genre             = netflix+"/WiGenre?agid={agid}"
    activity          = netflix+"/WiViewingActivity"
    video_info        = netflix+"/title/{movieid}"
    video_play        = netflix+"/WiPlayer?movieid={movieid}"
    add_to_queue      = netflix+"/AddToQueue?movieid={movieid}&qtype=INSTANT&{encodedAuth}"
    remove_from_queue = netflix+"/QueueDelete?{encodedAuth}&qtype=ED&movieid={movieid}"



