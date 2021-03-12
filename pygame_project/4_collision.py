import pysftp
from base64 import decodebytes
import paramiko
import os
import sys
import pymssql
import time

today = time.strftime('%Y%m%d', time.localtime(time.time()))
# today = '20200705'

if not (os.path.isdir(today)):
    os.mkdir(os.path.join(today))  # 오늘 날짜의 폴더 생성

host = '210.122.73.203'  # 호스트명만 입력. sftp:// 는 필요하지 않다.
port = 8022  # int 값으로 sftp 서버의 포트 번호를 입력
username = 'kdnavien'  # 서버 유저명
password = 'kdnavien!234'  # 유저 비밀번호

hostkeys = None
cnopts = pysftp.CnOpts()

# 접속을 시도하는 호스트에 대한 호스트키 정보가 존재하는지 확인
# 존재하지 않으면 cnopts.hostkeys를 None으로 설정해줌으로써 첫 접속을 가능하게 함
if cnopts.hostkeys.lookup(host) == None:
    print("Hostkey for " + host + " doesn't exist")
    hostkeys = cnopts.hostkeys  # 혹시 모르니 다른 호스트키 정보들 백업
    cnopts.hostkeys = None

# 첫 접속이 성공하면, 호스트에 대한 호스트키 정보를 서버에 저장.
# 두번째 접속부터는 호스트키를 확인하며 접속하게 됨.

with pysftp.Connection(
        host,
        port=port,
        username=username,
        password=password,
        cnopts=cnopts) as sftp:
    # 접속이 완료된 후 이 부분이 호스트키를 저장하는 부분
    # 처음 접속 할 때만 실행되는 코드
    if hostkeys != None:
        print("New Host. Caching hostkey for " + host)

    sftp.chdir('/DOWN')  # 작업 디렉토리로 이동

    os.chdir(today)  # 오늘 날짜의 폴더로 이동

    tKDNVA = 'KDNVA' + str(today)
    tKDNVR = 'KDNVR' + str(today)

    sftp.get('KDNVA' + today, preserve_mtime=True)  # 파일 전송
    sftp.get('KDNVR' + today, preserve_mtime=True)

    print(sftp.listdir('/'))

    # 모든 작업이 끝나면 접속 종료
    sftp.close()

try:
    conn = pymssql.connect(host=r"192.168.35.155", user='cms', password='cms', database='CMS',
                           charset='utf8')
    # Connection 으로부터 Cursor 생성
    cursor = conn.cursor()

    kdnva = open(tKDNVA)
    line1 = kdnva.readline()

    while line1:
        # SQL문 실행
        cursor.execute("insert into TCMCenterASCost(VAL1, REGDATE, GUBUN) values(%s, getdate(), 'KDNVA')", line1)
        conn.commit()
        line1 = kdnva.readline()

    kdnvr = open(tKDNVR)
    line2 = kdnvr.readline()
    SERLKEY = 100

    while line2:
        if line2.startswith('T'):
            cursor.execute(
                "insert into TCMCenterASCost(VAL1, REGDATE, GUBUN, SERLKEY) values(%s, getdate(), 'KDNVR', %s)",
                (line2, today + str(SERLKEY)))
            conn.commit()
            SERLKEY += 1
            line2 = kdnvr.readline()
        elif line2.startswith('S'):
            line2 = kdnvr.readline()
        elif line2.startswith('E'):
            line2 = kdnvr.readline()
        else:
            cursor.execute(
                "insert into TCMCenterASCost(VAL1, REGDATE, GUBUN, SERLKEY) values(%s, getdate(), 'KDNVR', %s)",
                (line2, today + str(SERLKEY)))
            conn.commit()
            line2 = kdnvr.readline()

        # SQL문 실행
        # cursor.execute("insert into TCMCenterASCost(VAL1, REGDATE, GUBUN) values(%s, getdate(), 'KDNVR')", line2)
        # conn.commit()
        # line2 = kdnvr.readline()
    cursor.execute("exec SCMCenterASCostGetKCP_BATCH")
    conn.commit()
    conn.close()
    print('success')

except Exception as e:
    print('예외잖아요', e)