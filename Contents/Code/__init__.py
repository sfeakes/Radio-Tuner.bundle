#############
##
#############
TITLE    = 'Radio Tuner'
ART      = 'art-default.jpg'
ICON     = 'icon-default.png'
PREFIX   = '/music/radiotuner'

####################################################################################################

# This function is initially called by the PMS framework to initialize the plugin. This includes
# setting up the Plugin static instance along with the displayed artwork.
def Start():
    # Initialize the plugin
    Plugin.AddViewGroup('rt_view_group', viewMode = 'list', mediaType = 'items')

    # Setup the artwork associated with the plugin
    ObjectContainer.title1 = TITLE
    ObjectContainer.art = R(ART)
    ObjectContainer.view_group = 'rt_view_group'

    TrackObject.thumb = R(ICON)
    DirectoryObject.thumb = R(ICON)

####################################################################################################

@handler(PREFIX, TITLE)
def MainMenu():

    oc = ObjectContainer()

    i=1

    while Prefs['url'+str(i)] and Prefs['title'+str(i)] :
        oc.add(CreateTrackObject(url=Prefs['url'+str(i)], title=Prefs['title'+str(i)], fmt=Prefs['type'+str(i)]))
        i += 1

    return oc


####################################################################################################
def CreateTrackObject(url, title, fmt, include_container=False, includeBandwidths=False):
      
	# choose container and codec to use for the supplied format
    if fmt == 'mp3':
        container = Container.MP3
        audio_codec = AudioCodec.MP3
    elif fmt == 'aac':
        container = Container.MP4
        audio_codec = AudioCodec.AAC
#    elif fmt == 'hls':
#        # This needs some more work, should use PartObject(key=HTTPLiveStreamURL(url))
#        protocol = 'hls'
#        container = 'mpegts'
#        # video_codec = VideoCodec.H264
#        # audio_codec = AudioCodec.AAC
    elif fmt == '.flac':
        container = Container.FLAC
        audio_codec = AudioCodec.FLAC
    elif fmt == '.ogg':
        container = Container.OGG
        audio_codec = AudioCodec.OGG
    else:
        container = Container.MP3
        audio_codec = AudioCodec.MP3

    track_object = TrackObject(
        key=Callback(CreateTrackObject, url=url, title=title, fmt=fmt, include_container=True, includeBandwidths=False),
        rating_key=url,
        title=title,
        thumb=R(ICON),
        items=[
            MediaObject(
                parts=[
                    PartObject(key=url)
                ],
                container=container,
                audio_codec=audio_codec,
                audio_channels=2
            )
        ]
    )

    if include_container:
        return ObjectContainer(objects=[track_object])
    else:
        return track_object


####################################################################################################
#def PlayAudio(url, **kwargs):
	
#	return Redirect(url)