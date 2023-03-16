def left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff

#ฟังก์ชั่นการเตรียมข้อความให้มีขนาด 512-bit
def pad_message(message): 
    count = 0
    message = bytearray(message, 'utf-8')
    byte = len(message) * 8
    message.append(0x80)
    while len(message) % 64 != 56:
        message.append(0)
        count += 1
    message += byte.to_bytes(8, byteorder='big')
    return message

def SHA1(message) :
    #ค่าเริ่มต้น
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0
    padded_message = pad_message(message)
    for i in range(0, len(padded_message), 64):
        chunk = padded_message[i:i+64]
        words = [0] * 80
        for j in range(16):
            words[j] = int.from_bytes(chunk[j*4:j*4+4], byteorder='big')
            
        for j in range(16,80):
            words[j] = left_rotate(words[j-3] ^ words[j - 8] ^ words[j -14] ^ words[j - 16],1)
        A = h0
        B = h1
        C = h2
        D = h3
        E = h4

        for j in range(80):
            if j < 20:
                F = (B & C) ^ ((~B) & D)
                K = 0x5A827999 #ค่าคงที่ในแต่ละรอบ
            elif  j < 40:
                F = (B ^ C )^ D
                K = 0x6ED9EBA1
            elif j < 60 :
                F = (B & C) ^ (B & D) ^ (C & D)
                K = 0x8F1BBCDC
            else:
                F = B ^ C ^ D  
                K = 0xCA62C1D6
            temp = left_rotate(A,5) + F + E + K + words[j] & 0xffffffff
            E = D
            D = C
            C = left_rotate(B,30)
            B = A
            A = temp
        h0 = (h0 + A) & 0xffffffff
        h1 = (h1 + B) & 0xffffffff
        h2 = (h2 + C) & 0xffffffff
        h3 = (h3 + D) & 0xffffffff
        h4 = (h4 + E) & 0xffffffff

    return '{:08x}{:08x}{:08x}{:08x}{:08x}'.format(h0, h1, h2, h3, h4)

