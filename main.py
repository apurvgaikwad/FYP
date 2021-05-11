# Python program implementing Image Steganography
import eel
import getopt, os, sys, math, struct, wave
import time
from datetime import datetime
# PIL module is used to extract
# pixels of image and modify it
from PIL import Image

############################################## IMAGE STEGANOGRAPHY #########################################################
# Convert encoding data into 8-bit binary
# each character converted to 1 byte
# formed using ASCII value of characters
@eel.expose
def generate_data(data):

        # list of binary codes
        # of given data
        newd = []

        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd #returns list of bytes, where each byte is one character

# Pixels are modified according to the
# 8-bit binary data and finally returned
@eel.expose
def modify_pixels(pix, data):

    datalist = generate_data(data)
    lendata = len(datalist) #no. of characters in data
    imdata = iter(pix) #creates an object which can be iterated one element at a time

    for i in range(lendata):

        # Extracting 3 pixels at a time for each character
        # each pixel has 3 RGB values, so 9 values in total
        pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]

        # RGB value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            # if bit of the character byte is 0(even) and rgb value is odd, change rgb value to even.
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1
            # if bit of the character byte is 1(odd) and rgb value is even,
            # change rgb value to odd(handle if rgb value was zero or non-zero)
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1


        # last grb value in every set of 9 rgb values tells us
        # whether to stop or to read further.
        # 0 means keep reading, 1 means the message is over.
        if (i == lendata - 1): # last character
            # if last rgb value is even, change to odd because it is the last character (don't need to keep reading)
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else: # not the last character
            # if last rgb value is even, change to odd because no last character (need to keep reading)
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix) #create list of 9 rgb values to tuple of 9 rgb values
        yield pix[0:3]   #generates the new values pixel by pixel
        yield pix[3:6]
        yield pix[6:9]

@eel.expose
def insert_data(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modify_pixels(newimg.getdata(), data): #getdata() Returns the contents of this image as a sequence object containing pixel values. The sequence object is flattened, so that values for line one follow directly after the values of line zero, and so on.
                                                 # modify_pixels returns the modified pixels
        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

# Hide data into image
@eel.expose
def hide(img, file_to_read, new_img_name):

    try:
        start_time = time.time()
        now1 = datetime.now()
        current_time1 = now1.strftime("%H:%M:%S")

        image = Image.open(img, 'r')
        data = open(file_to_read, "r").read()
        newimg = image.copy()
        insert_data(newimg, data)

        #save new img file
        newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
        success_msg = "success"
        print("success")
        end_time = time.time()
        total = end_time - start_time
        now2 = datetime.now()
        current_time2 = now2.strftime("%H:%M:%S")


        print("Start Time =", current_time1)
        #print("Time started: ", start_time)

        print("End Time =", current_time2)
        #print("Time ended: ", end_time)
        print("Time required to hide message inside " + str(img) + " was: " + str(total))

        return success_msg

    except:
        success_msg = "failure"
        print("failure")
        return success_msg


# Extract the data from the image
@eel.expose
def extract(img, new_file_name):

    try:
        start_time = time.time()
        now1 = datetime.now()
        current_time1 = now1.strftime("%H:%M:%S")
        image = Image.open(img, 'r')



        data = ''
        imgdata = iter(image.getdata())

        # get the list of 3 pixels at a time(9 rgb values)
        while (True):
            RGBs = [value for value in imgdata.__next__()[:3] +
                                    imgdata.__next__()[:3] +
                                    imgdata.__next__()[:3]]

            # string of binary data
            binstr = ''

            # for the first 8 rgb values
            # if value is even, add 0 into string of binary data
            # if value is odd, add 1 into string of binary data
            for i in RGBs[:8]:
                if (i % 2 == 0):
                    binstr += '0'
                else:
                    binstr += '1'

            data += chr(int(binstr, 2))
            last_chars = new_file_name[-3:]
            if (last_chars == "txt"):

                if (RGBs[-1] % 2 != 0): # if 9th rgb value is odd (no more data to decode), then can return
                    f = open(new_file_name, "w", encoding="utf-8")
                    f.write(data)
                    f.close()
                    end_time = time.time()
                    total = end_time - start_time
                    now2 = datetime.now()
                    current_time2 = now2.strftime("%H:%M:%S")

                    print("Start Time =", current_time1)
                    # print("Time started: ", start_time)

                    print("End Time =", current_time2)
                    # print("Time ended: ", end_time)
                    print("Time required to extract message from " + str(img) + " was: " + str(total))
                    success_msg = "success"
                    return success_msg
                    #return None
            else:
                raise Exception("not a text file")
    except:
        success_msg = "failure"
        print("failure")
        return success_msg


############################################## AUDIO STEGANOGRAPHY #########################################################
@eel.expose
def prepare(sound_file, num_lsb):
    global sound, params, n_frames, n_samples, fmt, mask, smallest_byte
    number_lsb = num_lsb
    sound = wave.open(sound_file, "r")

    params = sound.getparams()  # Returns a namedtuple() (nchannels, sampwidth, framerate, nframes, comptype, compname), equivalent to output of the get*() methods.
    num_channels = sound.getnchannels()  # Returns number of audio channels (1 for mono, 2 for stereo).
    sample_width = sound.getsampwidth()  # Returns sample width in bytes.
    n_frames = sound.getnframes()  # Returns number of audio frames.
    n_samples = n_frames * num_channels

    if (sample_width == 1):  # if samples are unsigned 8-bit integers
        fmt = "{}B".format(n_samples)
        # Used to set the least significant bits of an integer to 0
        mask = (1 << 8) - (1 << number_lsb)
        # The least possible value for a sample in the sound file is actually
        # zero, but we don't skip any samples for 8 bit depth wav files.
        smallest_byte = -(1 << 8)
    elif (sample_width == 2):  # samples are signed 16-bit integers
        fmt = "{}h".format(n_samples)
        # Used to set the least significant bits of an integer to zero
        mask = (1 << 15) - (1 << number_lsb)
        # The least possible value for a sample in the sound file
        smallest_byte = -(1 << 15)
    else:
        # Python's wave module doesn't support higher sample widths
        raise ValueError("File has an unsupported bit-depth")


@eel.expose
def hide_data(sound_file, text_file, output_path, num_lsb):
    try:
        global sound, params, n_frames, n_samples, fmt, mask, smallest_byte
        start_time = time.time()
        now1 = datetime.now()
        current_time1 = now1.strftime("%H:%M:%S")
        prepare(sound_file, num_lsb)
        # We can hide up to num_lsb bits in each sample of the sound file
        max_bytes_to_hide = (n_samples * num_lsb) // 8
        filesize = os.stat(text_file).st_size

        if (filesize > max_bytes_to_hide):
            required_LSBs = math.ceil(filesize * 8 / n_samples)
            raise ValueError("Input file too large to hide, "
                             "requires {} LSBs, using {}"
                             .format(required_LSBs, num_lsb))

        print("Using {} B out of {} B".format(filesize, max_bytes_to_hide))

        # Put all the samples from the sound file into a list
        raw_data = list(struct.unpack(fmt, sound.readframes(n_frames)))
        sound.close()

        input_data = memoryview(open(text_file, "rb").read())

        # The number of bits we've processed from the input file
        data_index = 0
        sound_index = 0

        # values will hold the altered sound data
        values = []
        buffer = 0
        buffer_length = 0
        done = False

        while (not done):
            while (buffer_length < num_lsb and data_index // 8 < len(input_data)):
                # If we don't have enough data in the buffer, add the
                # rest of the next byte from the file to it.
                buffer += (input_data[data_index // 8] >> (data_index % 8)
                           ) << buffer_length
                bits_added = 8 - (data_index % 8)
                buffer_length += bits_added
                data_index += bits_added

            # Retrieve the next num_lsb bits from the buffer for use later
            current_data = buffer % (1 << num_lsb)
            buffer >>= num_lsb
            buffer_length -= num_lsb

            while (sound_index < len(raw_data) and
                   raw_data[sound_index] == smallest_byte):
                # If the next sample from the sound file is the smallest possible
                # value, we skip it. Changing the LSB of such a value could cause
                # an overflow and drastically change the sample in the output.
                values.append(struct.pack(fmt[-1], raw_data[sound_index]))
                sound_index += 1

            if (sound_index < len(raw_data)):
                current_sample = raw_data[sound_index]
                sound_index += 1

                sign = 1
                if (current_sample < 0):
                    # We alter the LSBs of the absolute value of the sample to
                    # avoid problems with two's complement. This also avoids
                    # changing a sample to the smallest possible value, which we
                    # would skip when attempting to recover data.
                    current_sample = -current_sample
                    sign = -1

                # Bitwise AND with mask turns the least significant bits
                # of audio sample to 0. Bitwise OR with message bit replaces
                # these least significant bits with the corresponding message bit of data.
                altered_sample = sign * ((current_sample & mask) | current_data)

                values.append(struct.pack(fmt[-1], altered_sample))

            if (data_index // 8 >= len(input_data) and buffer_length <= 0):
                done = True

        while (sound_index < len(raw_data)):
            # At this point, there's no more data to hide. So we append the rest of
            # the samples from the original sound file.
            values.append(struct.pack(fmt[-1], raw_data[sound_index]))
            sound_index += 1

        last_chars = output_path[-3:]
        if (last_chars == "wav"):

            sound_steg = wave.open(output_path, "w")
            sound_steg.setparams(params)
            sound_steg.writeframes(b"".join(values))
            sound_steg.close()
            print("Data hidden over {} audio file".format(output_path))
            end_time = time.time()
            total = end_time - start_time
            now2 = datetime.now()
            current_time2 = now2.strftime("%H:%M:%S")

            print("Start Time =", current_time1)
            # print("Time started: ", start_time)

            print("End Time =", current_time2)
            # print("Time ended: ", end_time)
            print("Time required to hide message in " + str(sound_file) + " was: " + str(total))
            success_msg = "success"
            return success_msg
        else:
            raise Exception("not a wav file")
    except:
        success_msg = "failure"
        print("failure")
        return success_msg


@eel.expose
def extract_data(new_sound_file, new_text_file, num_lsb, bytes_used):

    try:

        # Recover data from the file at new_sound_file to the file at output_path
        global sound, n_frames, n_samples, fmt, smallest_byte
        start_time = time.time()
        now1 = datetime.now()
        current_time1 = now1.strftime("%H:%M:%S")
        prepare(new_sound_file, num_lsb)

        # Put all the samples from the sound file into a list
        raw_data = list(struct.unpack(fmt, sound.readframes(n_frames)))

        # Used to extract the least significant bits of an integer
        mask = (1 << num_lsb) - 1

        last_chars = new_text_file[-3:]
        if (last_chars == "txt"):
            output_file = open(new_text_file, "wb+")

            data = bytearray()
            sound_index = 0
            buffer = 0
            buffer_length = 0
            sound.close()

            while (bytes_used > 0):

                next_sample = raw_data[sound_index]
                if (next_sample != smallest_byte):
                    # Since we skipped samples with the minimum possible value when
                    # hiding data, we do the same here.

                    # Bitwise AND with mask returns the least significant bits
                    # of audio sample.
                    buffer += (abs(next_sample) & mask) << buffer_length
                    buffer_length += num_lsb
                sound_index += 1

                while (buffer_length >= 8 and bytes_used > 0):
                    # If we have more than a byte in the buffer, add it to data
                    # and decrement the number of bytes left to recover.
                    current_data = buffer % (1 << 8)
                    buffer >>= 8
                    buffer_length -= 8
                    data += struct.pack('1B', current_data)
                    bytes_used -= 1

            output_file.write(bytes(data))
            output_file.close()
            print("Data recovered to {} text file".format(new_text_file))
            end_time = time.time()
            total = end_time - start_time
            now2 = datetime.now()
            current_time2 = now2.strftime("%H:%M:%S")

            print("Start Time =", current_time1)
            # print("Time started: ", start_time)

            print("End Time =", current_time2)
            # print("Time ended: ", end_time)
            print("Time required to extract message from " + str(new_sound_file) + " was: " + str(total))
            success_msg = "success"
            return success_msg
        else:
            raise Exception("not a text file")
    except:
        success_msg = "failure"
        print("failure")
        return success_msg


eel.init('front-end')
eel.start('home.html', size=(1000, 620))


