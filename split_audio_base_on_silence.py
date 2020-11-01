# Import the AudioSegment class for processing audio and the 
# split_on_silence function for separating out silent chunks.
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os 

def append_zeros_for_index(index):
    if index//10 == 0:
        return "0000"+str(index)
    if index//100 == 0:
        return "000"+str(index)
    if index//1000 == 0:
        return "00"+str(index)
    if index//10000 == 0:
        return "0"+str(index)
    return str(index)

# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

def do_splitted(audio_name, save_folder, min_silence_len=250, silence_thresh=-40):
    # Load your audio.
    song = AudioSegment.from_file(audio_name)
    # Split track where the silence is 2 seconds or more and get chunks using 
    # the imported function.
    chunks = split_on_silence (
        # Use the loaded audio.
        song, 
        # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
        min_silence_len = min_silence_len,
        # Consider a chunk silent if it's quieter than -16 dBFS.
        # (You may want to adjust this parameter.)
        silence_thresh = silence_thresh,
        # keep_silence=200
    )

    # Process each chunk with your parameters
    minimum_length=11000
    maximum_length=15000
    temp = None
    i=0
    for chunk in chunks:
        if temp is not None:
            temp = temp + chunk
            if len(temp) > minimum_length:
                chunk = temp
                temp = None
            else:
                continue
        else:
            if len(chunk) < minimum_length:
                temp = chunk
                continue
        if len(chunk) > maximum_length:
            continue
        # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
        silence_chunk = AudioSegment.silent(duration=100)

        # Add the padding chunk to beginning and end of the entire chunk.
        audio_chunk = silence_chunk + chunk + silence_chunk

        # Normalize the entire chunk.
        # normalized_chunk = match_target_amplitude(audio_chunk, -20.0)
        normalized_chunk = audio_chunk
        normalized_chunk = normalized_chunk.set_frame_rate(16000)
        normalized_chunk = normalized_chunk.set_sample_width(2)
        normalized_chunk = normalized_chunk.set_channels(1)
        # # Export the audio chunk with new bitrate.
        print("Exporting chunk{0}.wav.".format(append_zeros_for_index(i)))
        normalized_chunk.export(
            os.path.join(save_folder,"chunk{0}.wav".format(append_zeros_for_index(i))),
            bitrate = "256",
            format = "wav"
        )
        i = i + 1
import sys
if __name__ == "__main__":
    do_splitted(sys.argv[1],"./audio",min_silence_len=150, silence_thresh=-35)