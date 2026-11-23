#BMP
import numpy as np
import cv2 as cv
import struct

def MakeImage(W,H,C=3):
    img=np.zeros((W,H,C),dtype=np.uint8)
def PaintImage(W,H):
    x=np.arange(W)
    y=np.arange(H)
    X,Y=np.meshgrid(x,y)
    Xn=X/max(W-1,1)
    Yn=Y/max(H-1,1)

    R=255*Xn
    G=255*Yn
    B=127.5+127.5*np.sin(2*np.pi*Xn)

    img=np.stack((R,G,B),axis=2)
    img=np.clip(img,0,255).astype(np.uint8)
    return img
# RGB in 1b= (0,0,0) (1,0,0) (0,1,0) (0,0,1) (1,1,0) (1,0,1) (0,1,1) (1,1,1)
def PaintImageDynamic(W, H, dtype=np.uint8):
    x = np.arange(W)
    y = np.arange(H)
    X, Y = np.meshgrid(x, y)
    Xn = X / max(W - 1, 1)
    Yn = Y / max(H - 1, 1)

    # Determine max value based on data type
    if np.issubdtype(dtype, np.floating):
        max_val = 1.0
    elif np.issubdtype(dtype, np.integer):
        max_val = np.iinfo(dtype).max  # 255 for uint8, 65535 for uint16
    else:
        raise ValueError("Unsupported dtype")

    R = max_val * Xn
    G = max_val * Yn
    B = (max_val / 2.0) + (max_val / 2.0) * np.sin(2 * np.pi * Xn)

    img = np.stack((R, G, B), axis=2)
    img = np.clip(img, 0, max_val).astype(dtype)
    return img
# First 14 bits of a file indicate that this one is a BMP file
# Next 40 bites indiciate size and color of the iamge
# Little Endian
# Padding: BMP must be multiple of 4, if this one is not this is made one by addying bits up until
# reaching the closest multiple of 4
# Swap RGB positions (Make so is store as BGR)
def BMP_File(filename,img):
    if img.dtype != np.uint8:
        raise ValueError("Image must be uint8")
    
    H, W, C = img.shape
    if C != 3:
        raise ValueError("Image must have 3 color channels (RGB)")

    BGR=img[::-1, :, ::-1]
    Rbits=W*3
    padding=(4-(Rbits%4))%4
    padded_row=Rbits+padding

    PDS=padded_row*H
    file_size=54+PDS # 14-byte file header + 40-byte DIB header
    file_header = struct.pack(
        "<2sIHHI",
        b"BM",          # Signature
        file_size,      # Total file size in bytes
        0,              # Reserved 1
        0,              # Reserved 2
        54              # Offset to start of pixel data
    )

    # 4. Build 40-byte BITMAPINFOHEADER
    dib_header = struct.pack(
        "<IiiHHIIiiII",
        40,                 # DIB header size
        W,                  # Image width
        H,                  # Image height (positive = bottom-up)
        1,                  # Color planes (must be 1)
        24,                 # Bits per pixel (24-bit RGB)
        0,                  # Compression (0 = BI_RGB, uncompressed)
        PDS,    # Size of raw bitmap data
        2835,               # Horizontal resolution (72 DPI in pixels/meter)
        2835,               # Vertical resolution (72 DPI in pixels/meter)
        0,                  # Colors in color table (0 = default)
        0                   # Important color count (0 = all)
    )

    # 5. Pad rows if necessary and write binary file
    if padding > 0:
        pad_bytes = np.zeros((H, padding), dtype=np.uint8)
        raw_rows = np.hstack((BGR.reshape(H, Rbits), pad_bytes))
    else:
        raw_rows = BGR

    with open(filename, "wb") as f:
        f.write(file_header)
        f.write(dib_header)
        f.write(raw_rows.tobytes())

factor=2
def ReSize(img,f=2):
    imgN=img[::f,::f,:]
    return imgN
def ColorRe(img):
    rQ=(img[:,:,0]>>5)*36
    gQ=(img[:,:,1]>>5)*36
    bQ=(img[:,:,2]>>6)*85
    return rQ,gQ,bQ
def BMP_conversion(img,f=2):
    I=ReSize(img,f)
    R,G,B=ColorRe(I)
    img_final = np.dstack((R, G, B)).astype(np.uint8)
    return img_final
