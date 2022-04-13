#For extracting WAV files out of packed files...

from tkinter.filedialog import askopenfilename
import re

with open(askopenfilename(), 'rb') as data:
 
    # Per WAV specification, every WAV file starts with the file signature RIFF.
    # the next 4 bytes are the size of the rest of the file (in little endian) in bytes, 
    # which is rounded up to the nearest number divisible by 8. 
    offsets = [m.start() for m in re.finditer(b'RIFF....', data.read())]

    for n in range(len(offsets)):
        data.seek(0)
        data.read(offsets[n])
        with open(str(n) + '.wav', 'wb') as f:
            header = data.read(8)
            f.write(header)
            size = int.from_bytes(header[4:], byteorder='little') 
            size += ( 8 - (size % 8) )
            f.write(data.read(size))
            print("Saved " + str(n) + ".wav")

    print("Done!")
