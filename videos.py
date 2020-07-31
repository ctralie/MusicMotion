import json
import subprocess

FOLDER = "CounterpointVideos"

def load_clip_list():
    """
    Return a list of all clips with their descrptions
    Returns
    -------
    list of dict: All of the video info
        Dict has the keys
        {
            video: string
                path to video file,
            start: string
                Mins:Secs start time
            end: string
                Mins:Secs end time
            description: string
                Description
        }
    """
    all_clips = []
    data = json.load(open("{}/clips.json".format(FOLDER), "r"))
    for d in data:
        filename = "{}/{}".format(FOLDER, d['video'])
        clips = d['clips']
        for c in clips:
            c['video'] = filename
        all_clips += clips
    return all_clips

def split_videos():
    """
    Split up the videos according to highlighted regions
    """
    all_clips = load_clip_list()
    for i, clip in enumerate(all_clips):
        filename = clip['video']
        smin, ssec = clip['start'].split(":")
        start = int(smin)*60 + int(ssec)
        emin, esec = clip['end'].split(":")
        end = int(emin)*60 + int(esec)
        cmd = ["ffmpeg", "-i", filename, "-ss", "{}".format(start), "-t", "{}".format(end-start), "-qscale", "1", "{}/{}.avi".format(FOLDER, i)]
        print("Extracting video {}".format(i))
        print(cmd, "\n\n")
        subprocess.call(cmd)

split_videos()