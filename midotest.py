import mido
import numpy as np
# filename = 'William Tell GRP \'97.mid'
filename = 'Down Home GRP \'97.mid'
mid = mido.MidiFile(filename, clip=True)
print(f'the length of the data is {len(mid.tracks[0])}')

def find_bpm():
    for i in range(0, len(mid.tracks[0])):
        if mid.tracks[0][i].type == 'set_tempo':
            return mido.tempo2bpm(mid.tracks[0][i].tempo)



def show_music_time():
    return mid.length

print(f'The bpm is {find_bpm()}')
print(f'The time of the music is {show_music_time()} s')

def show_channel_0():
    for i in range(0, len(mid.tracks[0])):
        # if mid.tracks[0][i].type == 'set_tempo':
        if mid.tracks[0][i].type == 'note_on':
            if mid.tracks[0][i].channel==0:
                print(mid.tracks[0][i], mid.tracks[0][i].type)
    # if i.type == 'set_tempo':
    # print(i)

# data  = mid.tracks
# d = np.array(data)
# for m in mid.tracks[0][:60]:
