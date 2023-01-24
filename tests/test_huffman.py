from random import randrange
from pyzandro.huffman import huffencode, huffdecode

def test_huffman_realworld():
    rawdata = b'\x06S\x13\xf1\x92\x19\x7f\xff\xf3t\xb5\xac\xb6L67N\xf6L\xae6\xf7t5w\xfdyO\x17\xda\xd5\x1f\xb4?\xab\xde\xdc\xf3\xd3\xd3\xe3\xa3\x90\xf2\x95_\xa4\xc6\x1c\xf1\x9f\x96\xbf\x96\x9e\xe6\xae\xd5\x9ffs\x91\x90\x8a\xd4\xf8\x9bG\x83\x99\xf2@\xcb\x11\x19-\xb7xO\xe7t|\xf88%qD\xe6\x16\xff\xb7\xaap\xe1\xc2pD\xe6\x16\x8f\x7f\xb5\xa5\xc7.\x8e\xb4\xb6\xa9\xfdki\x95aU\x1c\x91\xb9\xc5oh\xdaj\xecjK\x8f]\x1cimS;\xd9\xd2*\xc3\xaa8"s\x8b\xb7\xc8\xa36l\x18\x83\xd4\xef\xdaM\\M[\x8d\xb5\xf8\xbb\x9e[ZeX\x15Gdn\xf1\x1b\xc6\x8c]m\xe9\xb1\x8b#\xadmj\xbbZZeX\x15Gdn\xf1\xcd\xcd\xeb\xdc\xf05\xcd\x13i\xecjK\x8f]\x1cimS;\xd9\xd2*\xc3\xaa\xc6#\x8dj4\x17)\xfe\xc8\x88H\x9b\x9cH!5j\x0cRy"5\xb6\xb4\xca\xb0*\x8e\xc8\xdc\xe2\x9b\x9by\x8d:\x12i\xc4\xd8\xd5\x96\x1e\xbb8\xd2\xda\xa6v\xb2\xa5U\x86U\x11\x89[\xf0\xe0\xb8\xfc\xf8X\xdc\x82\x07\xc75\xd9\x12\x99\x93\x9b\xa4N\x9d&\x15N&%IRv\xe4Hc\xd7FjDJ\\$i7\xc9\xb9x\xec\xa8\x11c\xd6FB2jj\xa4Fu\x90\xa4\xdd$rc\xd3\xc5yF5FR\x1aI\xdaM&6;j\xea\xc6QS\x91R2q\x93dR\xca\n\x9c\xb8\xab\x93$qC#I\x92\x94F\x92v\x92M\xb3\x02'
    
    expected = b'w]V\x00\x864\xc8c1.3.2-r2023-01-14 01:35:53 -0500 on Linux 5.4.0-135-generic\x00\xff?\x19:QC:DE NA FFA\x00\x00\x00QCDE43\x00\x14\x14\x07QCDEv3.0_beta_4.pk3\x00QCDEmaps3.0_beta_2.pk3\x00QCDE_CommunityMaps_v17.pk3\x00QCDEmus3.0_beta_1.pk3\x00QCDE--HDFaces3.0_beta_2.pk3\x00GeorgeExleyAnnouncer.pk3\x00QCDE--Voxels3.0_beta_2.pk3\x00\x03\x00\x00DOOM II\x00DOOM2.WAD\x00\x00\x00\x02\x022\x00\x14\x00\n\x00\x00\x00\x00\x00\x00\x00\x04Western\x00\t\x00\x00\x00\x00\x01\nAbsolutePower\x00\x0f\x00\x00\x00\x00\x01\nCrabcore\x00\x08\x00\x00\x00\x00\x01\nShowdown\x00\x1e\x00D\x00\x00\x00\n\x00\x00\x06\x80A\x82\x00\x02\x00\x00\x00\x00D|\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x01\x03\x04\x05\x06'
    
    decoded = huffdecode(rawdata)
    assert decoded == expected

def roundtrip(data):
    return huffdecode(huffencode(data)) == data

def test_huffman_roundtrip():
    for idx in range(100):
        random_data = bytes([randrange(1,256) for _ in range(10*idx)])
        assert roundtrip(random_data), f"huffman roundtrip failed for {repr(random_data)}"
