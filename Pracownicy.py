# -*- coding:utf-8 -*-
import pymysql

class Pracownicy:
    def __init__(self):
        while(True):
            quit = input('Podaj numer polecenia: 1.Zaloguj, 2.Wyjdź ')
            if(quit == '2'):
                break
            self.connString()
            dostep = self.login()
            if(dostep.upper() == 'A'):
                print('Witaj! Właśnie zalogowałeś się do bazy danych jako administrator. Z tego poziomu masz dostęp do podglądu i modyfikacji wszystkich tabel w bazie.\n')
                while(True):
                    dec = input('Podaj numer polecenia: 1.Podgląd danych, 2.Usunięcie danych, 3.Wprowadzenie danych, 4.Wylogowanie ')
                    if(dec == '1'):
                        self.select()
                    elif(dec == '2'):
                        self.delete()
                    elif(dec == '3'):
                        self.insert()
                    elif(dec == '4'):
                        self.connClose()
                        break
                    else:
                        print('Niepoprawny wybór!')
            elif(dostep.upper() == 'U'):
                print('Witaj! Właśnie zalogowałeś się do bazy danych jako użytkownik. Masz teraz możliwość podglądu wszystkich swoich danych.\n')
                while(True):
                    dec = input('1.Podgląd danych, 2.Wylogowanie')
                    if(dec == '1'):
                        self.select_limited()
                    elif(dec == '2'):
                        self.connClose()
                        break
                    else:
                        print('Niepoprawny wybór!')               
            else:
                print('Błąd logowania!')
  
    def login(self):
        global login
        login = input('Podaj login: ')
        global haslo 
        haslo = input('Podaj hasło: ')
        self.c.execute('SELECT dostep FROM Logowanie WHERE login=%s AND haslo=%s', (login, haslo))
        try:
            dostep = self.c.fetchall()[0][0]
        except:
            dostep = '0'
        return dostep
    def connString(self):
        self.conn = pymysql.connect('localhost','''serwer''','''hasło''','Pracownicy', charset='utf8')
        self.c = self.conn.cursor()
    def select(self):
        while(True):
            dec = input('Podaj numer polecenia: 1.Wszystkie tabele w bazie, 2. Konkretna tabela, 3. Gotowe zestawienie 4. Wyjście')
            if(dec == '1'):
                self.c.execute('SHOW TABLES;')
                for i,row in enumerate(self.c.fetchall()):
                    print('%i. %-15s' % (i+1, row[0]))
            
            elif(dec == '2'):
                nazwa = input('Wpisz nazwę tabeli: ')
                try:
                    tabela = 'SELECT * FROM '+ str(nazwa)
                    self.c.execute(tabela)
                    for row in self.c.fetchall():
                        for val in row:
                            print('%-20s' % val, end='')
                        print('')
                except:
                    print("Niepoprawna nazwa tabeli!")
            elif(dec == '3'):
                zest = input('Podaj numer zestawienia: 1.Zarobki 2.Organizacja 3.Statystyki 4.Historia 5.Wykształcenie i pensje ')
                
                if(zest=='1'):
                    self.c.execute('SELECT * FROM zarobki;')
                    print('%-3s %-15s %-15s %-20s %-10s %-5s %-15s %-10s' % ('ID', 'Imię', 'Nazwisko', 'Stanowisko', 'Pensja', 'Kwal.', 'Premia wypł.', 'Suma'))
                    print('-'*95)
                    for row in self.c.fetchall():
                        print('%-3s %-15s %-15s %-20s %-10s %-5s %-15s %-10s' % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
                elif(zest=='2'):
                    self.c.execute('SELECT * FROM organizacja;')
                    print('%-20s %-10s %-12s %-15s' % ('Dział', 'Budżet', 'Liczba Prac.', 'Dyrektor'))
                    print('-'*57)                    
                    for row in self.c.fetchall():
                        print('%-20s %-10s %-12s %-15s' % (row[0], row[1], row[2], row[3]))
                elif(zest=='3'):
                    self.c.execute('SELECT * FROM statystyki;')
                    print('%-20s %-10s %-12s %-12s %-10s %-11s %-11s' % ('Dział', 'Budżet', 'Liczba Prac.', 'Budżet/Prac.', 'Śr. Pensja', 'Suma Pensji', 'Suma/Budżet'))
                    print('-'*86)                    
                    for row in self.c.fetchall():
                        print('%-20s %-10s %-12s %-12s %-10s %-11s %-11s' % (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
                elif(zest=='4'):
                    self.c.execute('SELECT * FROM historia;')
                    print('%-10s %-15s %-17s %-10s %-10s' % ('Imię', 'Nazwisko', 'Poprz. Pracodawca', 'Lata Dośw.', 'Pensja'))
                    print('-'*62)                    
                    for row in self.c.fetchall():
                        print('%-10s %-15s %-17s %-10s %-10s' % (row[0], row[1], row[2], row[3], row[4]))
                elif(zest=='5'):
                    self.c.execute('SELECT * FROM tytul_a_pensja;')
                    print('%-10s %-10s %-10s' % ('Tytuł', 'Liczebność', 'Śr. Pensja'))
                    print('-'*30)                       
                    for row in self.c.fetchall():
                        print('%-10s %-10s %-10s' % (row[0], row[1], row[2]))
                else:
                    print('Niepoprawny numer!')
            elif(dec=='4'):
                break
            else:
                print('Niepoprawny wybór!')
    
    def select_limited(self):
        while(True):
            dec2 = input('Podaj numer polecenia: 1.Dane osobowe, 2. Stanowisko, pensja i premia, 3. Wykształcenie 4. Historia zatrudnienia 5. Wyjście')
            findID='SELECT id FROM logowanie WHERE login ='+'\''+str(login)+'\''
            self.c.execute(findID)
            id=self.c.fetchall()[0][0]            
            if(dec2=='1'):
                dane='SELECT * FROM pracownicy WHERE id='+'\''+str(id)+'\''
                self.c.execute(dane)
                print('%-3s %-15s %-15s %-15s %-15s' % ('ID', 'Imię', 'Nazwisko', 'PESEL', 'Data Ur.'))
                print('-'*63)                
                for row in self.c.fetchall():
                    print('%-3s %-15s %-15s %-15s %-15s' % (row[0], row[1], row[2], row[3], row[4]))
            elif(dec2=='2'):
                dane='SELECT * FROM zarobki WHERE id='+'\''+str(id)+'\''
                self.c.execute(dane)
                print('%-3s %-15s %-15s %-20s %-10s %-5s %-15s %-10s' % ('ID', 'Imię', 'Nazwisko', 'Stanowisko', 'Pensja', 'Kwal.', 'Premia wypł.', 'Suma'))
                print('-'*95)                
                for row in self.c.fetchall():
                    print('%-3s %-15s %-15s %-20s %-10s %-5s %-15s %-10s' % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            elif(dec2=='3'):
                dane='SELECT * FROM wykształcenie WHERE id='+'\''+str(id)+'\''
                self.c.execute(dane)
                print('%-3s %-15s %-15s %-15s %-15s' % ('ID', 'Uczelnia', 'Data Rozp.', 'Data Zak.', 'Tytuł'))
                print('-'*63)                 
                for row in self.c.fetchall():
                    print('%-3s %-15s %-15s %-15s %-15s' % (row[0], row[1], row[2], row[3], row[4]))
            elif(dec2=='4'):
                dane='SELECT * FROM historia_zatrudnienia WHERE id='+'\''+str(id)+'\''
                self.c.execute(dane)
                print('%-3s %-20s %-15s %-15s' % ('ID', 'Poprz. Pracodawca', 'Data Zatr.', 'Data Odejścia'))
                print('-'*53)
                for row in self.c.fetchall():
                    print('%-3s %-20s %-15s %-15s' % (row[0], row[1], row[2], row[3]))
            elif(dec2=='5'):
                break
            else:
                print('Niepoprawny numer!')
            
    def delete(self):
        while(True):
            dec3 = input('Podaj numer polecenia: 1.Usunięcie rekordów, 2. Wyjście')
            if(dec3=='1'):
                nazwa_us = str(input('Podaj tabelę do usunięcia rekordów: '))
                if(nazwa_us.upper() == "DZIAL"):
                    try:    
                        tabela_us = 'SELECT * FROM '+ str(nazwa_us)
                        print('Tabela obecnie:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                           
                        dzial_us = input('"Dzial" rekordu do usunięcia: ')
                        usuniecie = ('DELETE FROM '+ str(nazwa_us)+ ' WHERE Dzial= '+ '\''+str(dzial_us))+ '\''
                        self.c.execute(usuniecie)
                        self.conn.commit()
                        print('Tabela po usunięciu:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')   
                    except:
                        print('Niepoprawny dział!')
                elif(nazwa_us.upper() == "DYREKTORZY"):
                    try:    
                        tabela_us = 'SELECT * FROM '+ str(nazwa_us)
                        print('Tabela obecnie:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                               
                        dyr_us = input('"Dyrektor" rekordu do usunięcia: ')
                        usuniecie = ('DELETE FROM '+ str(nazwa_us)+ ' WHERE Dyrektor= '+ '\''+str(dyr_us))+ '\''
                        self.c.execute(usuniecie)
                        self.conn.commit()
                        print('Tabela po usunięciu:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                
                    except:
                        print('Niepoprawny dyrektor!')   
                elif(nazwa_us.upper() == "STANOWISKO_PENSJA"):
                    try:    
                        tabela_us = 'SELECT * FROM '+ str(nazwa_us)
                        print('Tabela obecnie:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                               
                        stan_us = input('"Stanowisko" rekordu do usunięcia: ')
                        usuniecie = ('DELETE FROM '+ str(nazwa_us)+ ' WHERE stanowisko= '+ '\''+str(stan_us))+ '\''
                        self.c.execute(usuniecie)
                        self.conn.commit()
                        print('Tabela po usunięciu:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')              
                    except:
                        print('Niepoprawne stanowisko!')
                elif(nazwa_us.upper() == "WYSOKOŚĆ_PREMII"):
                    try:    
                        tabela_us = 'SELECT * FROM '+ str(nazwa_us)
                        print('Tabela obecnie:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                               
                        staz_us = int(input('"Staż" rekordu do usunięcia: '))
                        usuniecie = ('DELETE FROM '+ str(nazwa_us)+ ' WHERE staz= '+ str(staz_us))
                        self.c.execute(usuniecie)
                        self.conn.commit()
                        print('Tabela po usunięciu:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                
                    except:
                        print('Niepoprawny staż!')
                elif(nazwa_us.upper() == "PRACOWNICY" or nazwa_us.upper() == "PRACOWNIK_DZIAL" or nazwa_us.upper() == "PRACOWNIK_STANOWISKO" or nazwa_us.upper() == "KWALIFIKACJA_DO_PREMII" or nazwa_us.upper() == "STAŻ_W_FIRMIE" or nazwa_us.upper() == "WYKSZTAŁCENIE" or nazwa_us.upper() == "HISTORIA_ZATRUDNIENIA" or nazwa_us.upper() == "LOGOWANIE"):
                    try:    
                        tabela_us = 'SELECT * FROM '+ str(nazwa_us)
                        print('Tabela obecnie:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                               
                        id = int(input('"ID" rekordu do usunięcia: '))
                        usuniecie = ('DELETE FROM '+ str(nazwa_us)+ ' WHERE id= '+str(id))
                        self.c.execute(usuniecie)
                        self.conn.commit()
                        print('Tabela po usunięciu:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')
                    except:
                        print('Podano błędny id!')
                else:
                    print('Niepoprawna nazwa tabeli!')
            elif(dec3=='2'):
                break
            else:
                print('Niepoprawny numer!')
   
    def insert(self):
        while(True):
            dec3 = input('Podaj numer polecenia: 1. Wprowadzenie danych, 2. Wyjście')
            if(dec3=='1'):
                nazwa_us = str(input('Podaj tabelę do wstawienia rekordów: '))
                if(nazwa_us.upper() == "DZIAL"):
                    try:    
                        tabela_us = 'SELECT * FROM '+ str(nazwa_us)
                        print('Tabela obecnie:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                           
                        dzial = input('Podaj dział(IT, sprzedaż, administracja albo obsługa klienta): ')
                        budzet = float(input('Podaj budżet: '))
                        liczba_prac = int(input('Podaj liczbę pracowników: '))
                        self.c.execute('insert into DZIAL values (%s, %s, %s);', (dzial,budzet,liczba_prac))
                        self.conn.commit()
                        print('Tabela po dodaniu:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                
                    except:
                        print('Niepoprawne dane!')
            
                elif(nazwa_us.upper() == "DYREKTORZY"):
                    try:    
                        tabela_us = 'SELECT * FROM '+ str(nazwa_us)
                        print('Tabela obecnie:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                           
                        dyrektor = input('Podaj dyrektora: ')
                        dzial = input('Podaj dział(IT, sprzedaż, administracja albo obsługa klienta): ')
                        self.c.execute('insert into DYREKTORZY values (%s, %s);', (dyrektor,dzial))
                        self.conn.commit()
                        print('Tabela po dodaniu:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                
                    except:
                        print('Niepoprawne dane!')
                        
                elif(nazwa_us.upper() == "STANOWISKO_PENSJA"):
                    try:    
                        tabela_us = 'SELECT * FROM '+ str(nazwa_us)
                        print('Tabela obecnie:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                           
                        stanowisko = input('Podaj stanowisko(specjalista,st. specjalista lub menedżer): ')
                        pensja = float(input('Podaj pensję: '))
                        self.c.execute('insert into STANOWISKO_PENSJA values (%s, %s);', (id,pensja))
                        self.conn.commit()
                        print('Tabela po dodaniu:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                
                    except:
                        print('Niepoprawne dane!')
                elif(nazwa_us.upper() == "WYSOKOŚĆ_PREMII"):
                    try:    
                        tabela_us = 'SELECT * FROM '+ str(nazwa_us)
                        print('Tabela obecnie:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                           
                        staz = int(input('Podaj staż: '))
                        premia = float(input('Podaj premię: '))
                        self.c.execute('insert into WYSOKOŚĆ_PREMII values (%s, %s);', (staz,premia))
                        self.conn.commit()
                        print('Tabela po dodaniu:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                
                    except:
                        print('Niepoprawne dane!')
                elif(nazwa_us.upper() == "PRACOWNICY"):
                    try:    
                        tabela_us = 'SELECT * FROM '+ str(nazwa_us)
                        print('Tabela obecnie:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                           
                        id = int(input('Podaj ID: '))
                        imie = input('Podaj imię: ')
                        nazwisko = input('Podaj nazwisko: ')
                        pesel = input('Podaj pesel: ')
                        data_ur = input('Podaj datę urodzenia(rrrr-mm-dd): ')
                        self.c.execute('insert into PRACOWNICY values (%s, %s, %s, %s, %s);', (id,imie,nazwisko,pesel,data_ur))
                        self.conn.commit()
                        print('Tabela po dodaniu:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                
                    except:
                        print('Niepoprawne dane!')               
                elif(nazwa_us.upper() == "PRACOWNIK_DZIAL"):
                    try:    
                        tabela_us = 'SELECT * FROM '+ str(nazwa_us)
                        print('Tabela obecnie:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                           
                        id = int(input('Podaj ID: '))
                        dzial = input('Podaj dział(IT, sprzedaż, administracja albo obsługa klienta): ')
                        self.c.execute('insert into PRACOWNIK_DZIAL values (%s, %s);', (id,dzial))
                        self.conn.commit()
                        print('Tabela po dodaniu:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                
                    except:
                        print('Niepoprawne dane!')   
                elif(nazwa_us.upper() == "PRACOWNIK_STANOWISKO"):
                    try:    
                        tabela_us = 'SELECT * FROM '+ str(nazwa_us)
                        print('Tabela obecnie:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                           
                        id = int(input('Podaj ID: '))
                        stanowisko = input('Podaj stanowisko(specjalista,st. specjalista lub menedżer): ')
                        self.c.execute('insert into PRACOWNIK_STANOWISKO values (%s, %s);', (id,stanowisko))
                        self.conn.commit()
                        print('Tabela po dodaniu:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                
                    except:
                        print('Niepoprawne dane!')
                elif(nazwa_us.upper() == "KWALIFIKACJA_DO_PREMII"):
                    try:    
                        tabela_us = 'SELECT * FROM '+ str(nazwa_us)
                        print('Tabela obecnie:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                           
                        id = int(input('Podaj ID: '))
                        kwalifikacja = input('Podaj kwalifikację(tak lub nie): ')
                        self.c.execute('insert into KWALIFIKACJA_DO_PREMII values (%s, %s);', (id,kwalifikacja))
                        self.conn.commit()
                        print('Tabela po dodaniu:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                
                    except:
                        print('Niepoprawne dane!')
                elif(nazwa_us.upper() == "STAŻ_W_FIRMIE"):
                    try:    
                        tabela_us = 'SELECT * FROM '+ str(nazwa_us)
                        print('Tabela obecnie:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                           
                        id = int(input('Podaj ID: '))
                        staz = int(input('Podaj staż: '))
                        self.c.execute('insert into STAŻ_W_FIRMIE values (%s, %s);', (id,staz))
                        self.conn.commit()
                        print('Tabela po dodaniu:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                
                    except:
                        print('Niepoprawne dane!')
                elif(nazwa_us.upper() == "WYKSZTAŁCENIE"):
                    try:    
                        tabela_us = 'SELECT * FROM '+ str(nazwa_us)
                        print('Tabela obecnie:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                           
                        id = int(input('Podaj ID: '))
                        uczelnia = input('Podaj uczelnię: ')
                        data_rozp = input('Podaj datę rozpoczęcia nauki(rrrr-mm-dd): ')
                        data_zak = input('Podaj datę zakończenia nauki(rrrr-mm-dd): ')
                        tytuł = input('Podaj tytuł(licencjat, inżynier, magister lub doktor): ')
                        self.c.execute('insert into WYKSZTAŁCENIE values (%s, %s, %s, %s, %s);', (id,uczelnia,data_rozp,data_zak,tytuł))
                        self.conn.commit()
                        print('Tabela po dodaniu:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                
                    except:
                        print('Niepoprawne dane!')
                elif(nazwa_us.upper() == "HISTORIA_ZATRUDNIENIA"):
                    try:    
                        tabela_us = 'SELECT * FROM '+ str(nazwa_us)
                        print('Tabela obecnie:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                           
                        id = int(input('Podaj ID: '))
                        poprz_pracodawca = input('Podaj poprzedniego pracodawcę: ')
                        data_zatrudnienia = input('Podaj datę zatrudnienia: ')
                        data_odejscia = input('Podaj datę odejścia: ')
                        self.c.execute('insert into HISTORIA_ZATRUDNIENIA values (%s, %s, %s, %s);', (id,poprz_pracodawca,data_zatrudnienia,data_odejscia))
                        self.conn.commit()
                        print('Tabela po dodaniu:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                
                    except:
                        print('Niepoprawne dane!')
                elif(nazwa_us.upper() == "LOGOWANIE"):
                    try:    
                        tabela_us = 'SELECT * FROM '+ str(nazwa_us)
                        print('Tabela obecnie:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                           
                        id = int(input('Podaj ID: '))
                        login = input('Podaj login: ')
                        haslo = input('Podaj hasło: ')
                        dostep = input('Podaj dostęp: ')
                        self.c.execute('insert into LOGOWANIE values (%s, %s, %s, %s);', (id,login,haslo,dostep))
                        self.conn.commit()
                        print('Tabela po dodaniu:')
                        self.c.execute(tabela_us)
                        for row in self.c.fetchall():
                            for val in row:
                                print('%-20s' % val, end='')
                            print('')                
                    except:
                        print('Niepoprawne dane!')
                else:
                    print('Niepoprawna nazwa tabeli!')
            elif(dec3=='2'):
                break
            else:
                print('Niepoprawny numer!')
    def connClose(self):
        self.conn.close()

db = Pracownicy()