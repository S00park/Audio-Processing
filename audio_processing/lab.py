# No Imports Allowed!

def backwards(sound):
    sample = sound['samples'].copy()
    sound_rev = sample[::-1]
    return {'rate': sound['rate'], 'samples':sound_rev}

    

def mix(sound1, sound2, p):
    sound1samp = sound1['samples'].copy()
    sound2samp = sound2['samples'].copy()
    mixedSamples = []
    if sound1['rate']==sound2['rate']:
        newSound1 = [item * p for item in sound1['samples']]
        newSound2 = [item * (1-p) for item in sound2['samples']]
        rate = sound1['rate']
        zip_lists = zip(newSound1, newSound2) 
        for item1, item2 in zip_lists: #simultaneously loop through each list
            mixedSamples.append(item1 + item2)
        newMix =  {'rate': rate, 'samples': mixedSamples}
        return newMix
    else:
        pass


def echo(sound, num_echoes, delay, scale):
   
    #first for loop for exponent based on num_echoes+1
    #second for loop based on sample delay
    samples = sound['samples'].copy()
    sample_delay = round(delay*sound['rate'])
    sampleLen = len(samples)
    totalLen = sampleLen + sample_delay*num_echoes

    output = [0]*totalLen

    for i in range(num_echoes+1):
        index = 0
        for j in range(i*sample_delay, i*sample_delay+sampleLen):
            output[j] += (sound['samples'][index]*(scale**i))
            index+=1
    return {'rate':sound['rate'], 'samples':output}


def pan(sound):
    newRight = []
    newLeft = []
    N = len(sound['right'])
    for i in range(N):
        newRight.append(sound['right'][i]*(i/(N-1)))
        newLeft.append(sound['left'][i]*(1-(i/(N-1))))
    return {'rate': sound['rate'], 'left': newLeft, 'right': newRight}


def remove_vocals(sound):
    mono = []
    for i in range(len(sound['left'])):
        left = sound['left'][i]
        right = sound['right'][i]
        diff = left-right
        mono.append(diff)

    return {'rate':sound['rate'], 'samples':mono}


# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds

import io
import wave
import struct


def load_wav(filename, stereo=False):
    """
    Given the filename of a WAV file, load the data from that file and return a
    Python dictionary representing that sound
    """
    f = wave.open(filename, "r")
    chan, bd, sr, count, _, _ = f.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    out = {"rate": sr}

    if stereo:
        left = []
        right = []
        for i in range(count):
            frame = f.readframes(1)
            if chan == 2:
                left.append(struct.unpack("<h", frame[:2])[0])
                right.append(struct.unpack("<h", frame[2:])[0])
            else:
                datum = struct.unpack("<h", frame)[0]
                left.append(datum)
                right.append(datum)

        out["left"] = [i / (2**15) for i in left]
        out["right"] = [i / (2**15) for i in right]
    else:
        samples = []
        for i in range(count):
            frame = f.readframes(1)
            if chan == 2:
                left = struct.unpack("<h", frame[:2])[0]
                right = struct.unpack("<h", frame[2:])[0]
                samples.append((left + right) / 2)
            else:
                datum = struct.unpack("<h", frame)[0]
                samples.append(datum)

        out["samples"] = [i / (2**15) for i in samples]

    return out


def write_wav(sound, filename):
    """
    Given a dictionary representing a sound, and a filename, convert the given
    sound into WAV format and save it as a file with the given filename (which
    can then be opened by most audio players)
    """
    outfile = wave.open(filename, "w")

    if "samples" in sound:
        # mono file
        outfile.setparams((1, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = [int(max(-1, min(1, v)) * (2**15 - 1)) for v in sound["samples"]]
    else:
        # stereo
        outfile.setparams((2, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = []
        for l, r in zip(sound["left"], sound["right"]):
            l = int(max(-1, min(1, l)) * (2**15 - 1))
            r = int(max(-1, min(1, r)) * (2**15 - 1))
            out.append(l)
            out.append(r)

    outfile.writeframes(b"".join(struct.pack("<h", frame) for frame in out))
    outfile.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/meow.wav, rather than just as meow.wav, to account for the sound
    # files being in a different directory than this file)
    #meow = load_wav("sounds/meow.wav")


    # write_wav(backwards(meow), 'meow_reversed.wav')
