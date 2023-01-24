from pyzandro.server import parse_response

def test_process_duel():
    d3 = b'w]V\x00z\x0c\xccc1.3.2-r2023-01-14 01:35:53 -0500 on Linux 5.10.0-19-amd64\x00\x89\x00\x18\x00QC:DE \xe2\x98\xaf Duel\x00QCCM03\x00\x05\x00\x00\x03klau\x00\x00\x00\x17\x00\x01\x00\x03Nooboot\x00\xfe\xff,\x00\x00\x00\x02\x1chBacco\x1cmbax\x1c-\x00\x03\x00-\x00\x00\x00\x02'
    r = parse_response(d3)
    assert len(r['players']) == 3
    assert r['players'][0]['team'] is None
    
    
def test_process_team_game():
    d4 = b'w]V\x00A\x12\xccc1.3.2-r2023-01-14 01:35:53 -0500 (TSPGv26) on Linux 5.15.0-56-generic\x00\x89\x00\x18\x00[EB] QC:DE Team Deathmatch\x00QCDE30\x00\x04\x00\x00\x03Jacob Singer\x00\x07\x00\x00\x00\x00\x01\x00\x07Inquisitor\x00\n\x00\x00\x00\x00\x01\x01\x07Die Apotheke\x00\x04\x00\x00\x00\x00\x01\x00\x07'
    r = parse_response(d4)
    assert r['mapname'] == 'QCDE30'
    assert r['players'][0]['team'] == 0
    assert r['players'][0]['bot'] == 1
    assert r['name_nocolor'] == '[EB] QC:DE Team Deathmatch'
