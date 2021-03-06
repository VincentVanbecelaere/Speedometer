import button
import LCD
import datetime
import time
import dbconn

tijden_sessie = []


deel_sessie = []
deel_sessies = []

parameter1 = 0
parameter2 = 0


start_sessie = 0
einde_sessie = 0

huidige_afstand = 0.000
total_distance = 0
stop = 0

tijden_sessie.clear()
deel_sessies.clear()

time.sleep(4)


def opslaan_deelsessies(start, stop, total_distance):


    global huidige_afstand

    afgelegde_afstand = total_distance - huidige_afstand

    print(total_distance)
    print(huidige_afstand)
    print(afgelegde_afstand)

    deel_sessies.append([start, stop, afgelegde_afstand])

    huidige_afstand = total_distance




def write_deelsessies():

    db = dbconn.DbConnection()

    sql1 = ('SELECT ID from Sessie ORDER BY ID DESC LIMIT 1')

    SessieID = db.query(sql1)

    for deelsessie in deel_sessies:

        sql2 = (
            'INSERT INTO Deelsessie (Begintijd, Eindtijd, Afstand, SessieID) '
            'VALUES ( %(new_begin)s, %(new_einde)s, %(new_afstand)s ,%(new_SessieID)s );'
        )



        params2 = {
            'new_begin': deelsessie[0],
            'new_einde': deelsessie[1],
            'new_afstand': deelsessie[2],
            'new_SessieID': SessieID[0][0]
        }

        db.execute(sql2, params2)

    deel_sessies.clear()

def write_sessie():
    db = dbconn.DbConnection()

    sql1 = ('SELECT ID from SnelheidsmeterGebruiker ORDER BY ID DESC LIMIT 1')

    snelheidsmeterGebruikerID = db.query(sql1)

    print(snelheidsmeterGebruikerID)

    sql2 = (
        'INSERT INTO Sessie (Begin, Einde, SnelheidsmeterGebruikerID) '
        'VALUES ( %(new_begin)s, %(new_einde)s, %(new_SnelheidsmeterGebruikerID)s );'
    )

    params2 = {
        'new_begin': tijden_sessie[0],
        'new_einde': tijden_sessie[1],
        'new_SnelheidsmeterGebruikerID': snelheidsmeterGebruikerID[0][0]
    }

    db.execute(sql2, params2)

    tijden_sessie.clear()



db = dbconn.DbConnection()
sql1 = ('select Voornaam from Gebruiker ORDER BY ID DESC LIMIT 1')
result1 = db.query(sql1)
voornaam = result1[0][0]

sql2 = ('select DiameterWiel from Gebruiker order by id desc limit 1')
result2 = db.query(sql2)
diameter = result2[0][0]




while True:


    wissel = button.wissel

    if wissel == 0:


        LCD.write('Begin een sessie,','{0}'.format(voornaam), '', 'Diameter wiel: {0}'.format(diameter))
        time.sleep(2)

    if wissel == 1:

        if(parameter1 == 0):
                global start

                start_sessie = datetime.datetime.now()
                start = datetime.datetime.now().strftime('%H:%M:%S')
                start_sessie_voor_lijst = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                tijden_sessie.append(start_sessie_voor_lijst)

        parameter1 += 0.000000000000000000000001

        start_sessie_minutes = int(str(start_sessie)[14:16])

        start = start_sessie.strftime('%H:%M:%S')

        nu = datetime.datetime.now()
        nu_minutes = int(str(nu)[14:16])
        print("----minutes---")
        print(nu_minutes)
        print(start_sessie_minutes)

        stop = datetime.datetime.now().strftime('%H:%M:%S')

        time.sleep(1)

        import HallSensor

        total_distance = HallSensor.totale_afstand




        if((nu_minutes == start_sessie_minutes + 1) or (nu_minutes == start_sessie_minutes - 59)):

              opslaan_deelsessies(start,stop, total_distance)
              print('test')
              parameter2 +=1

        if(parameter2 > 0):

            start_sessie = nu
            parameter2=0


        snelheid = 0
        totale_afstand = 0

        snelheid = '{0} km/u'.format(HallSensor.snelheid)

        totale_afstand = '{0} km'.format(HallSensor.totale_afstand)


        LCD.write('----SPEEDOMETER-----', snelheid, totale_afstand, time.ctime(int(time.time())))
        time.sleep(1)


    if wissel == 2:
        einde_sessie = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tijden_sessie.append(einde_sessie)

        LCD.write('Einde sessie', '', '', '')

        time.sleep(2)

        write_sessie()

        time.sleep(2)

        write_deelsessies()
        time.sleep(2)
        HallSensor.reset()
        huidige_afstand = 0
        parameter1 = 0
        button.wissel = 0



