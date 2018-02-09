#tabela z pracownikami, ich stanowiskami i pensjami
SELECT 
    p.ID, p.imie, p.nazwisko, ps.stanowisko, sp.pensja
FROM
    Pracownicy AS p
        LEFT JOIN
    Pracownik_Stanowisko AS ps ON p.ID = ps.ID
        LEFT JOIN
    Stanowisko_Pensja AS sp ON ps.stanowisko = sp.stanowisko
ORDER BY sp.pensja DESC , ID ASC;

#inaczej
SELECT 
    p.ID,
    p.imie,
    p.nazwisko,
    ps.stanowisko,
    sp.pensja
    
FROM
    Pracownicy AS p,
	Pracownik_Stanowisko AS ps,
	Stanowisko_Pensja AS sp 
    where p.ID = ps.ID and ps.stanowisko = sp.stanowisko
ORDER BY sp.pensja desc,ID asc;

#teoretyczna wysokość premii wszystkich pracowników
SELECT 
    p.ID, p.imie, p.nazwisko, s.staz, w.premia
FROM
    Pracownicy AS p,
    Staż_w_firmie AS s,
    Wysokość_premii AS w
WHERE
    p.ID = s.ID AND s.staz = w.staz
ORDER BY s.staz ASC , ID ASC;

#pracownicy z przyznanymi premiami
SELECT 
    p.ID, p.imie, p.nazwisko, s.staz, k.kwalifikacja, w.premia
FROM
    Pracownicy AS p,
    Staż_w_firmie AS s,
    Wysokość_premii AS w,
    Kwalifikacja_do_premii AS k
WHERE
    p.ID = s.ID AND s.staz = w.staz
        AND k.ID = p.ID
        AND k.kwalifikacja = 'tak'
ORDER BY s.staz ASC , ID ASC;

#wszyscy pracownicy i ich premie
SELECT 
    p.ID,
    p.imie,
    p.nazwisko,
    s.staz,
    k.kwalifikacja,
    CASE
        WHEN k.kwalifikacja = 'tak' THEN w.premia
        ELSE 0
    END AS 'premia'
FROM
    Pracownicy AS p,
    Staż_w_firmie AS s,
    Wysokość_premii AS w,
    Kwalifikacja_do_premii AS k
WHERE
    p.ID = s.ID AND s.staz = w.staz
        AND k.ID = p.ID
ORDER BY premia DESC , ID DESC;

#zarobki+premia
SELECT 
    p.ID,
    p.imie,
    p.nazwisko,
    ps.stanowisko,
    sp.pensja,
    k.kwalifikacja,
    CASE
        WHEN k.kwalifikacja = 'tak' THEN w.premia
        ELSE 0
    END AS 'premia_przyznana',
    CASE
        WHEN k.kwalifikacja = 'tak' THEN w.premia + sp.pensja
        ELSE sp.pensja
    END AS 'suma'
FROM
    Pracownicy AS p,
    Pracownik_Stanowisko AS ps,
    Stanowisko_Pensja AS sp,
    Staż_w_firmie AS s,
    Wysokość_premii AS w,
    Kwalifikacja_do_premii AS k
WHERE
    p.ID = ps.ID
        AND ps.stanowisko = sp.stanowisko
        AND p.ID = s.ID
        AND s.staz = w.staz
        AND k.ID = p.ID
ORDER BY sp.pensja DESC , ID ASC;

#tworzę pierwszy widok na podstawie tabeli wyżej
create view zarobki as SELECT 
    p.ID,
    p.imie,
    p.nazwisko,
    ps.stanowisko,
    sp.pensja,
    k.kwalifikacja,
    CASE
        WHEN k.kwalifikacja = 'tak' THEN w.premia
        ELSE 0
    END AS 'premia_przyznana',
    CASE
        WHEN k.kwalifikacja = 'tak' THEN w.premia + sp.pensja
        ELSE sp.pensja
    END AS 'suma'
FROM
    Pracownicy AS p,
    Pracownik_Stanowisko AS ps,
    Stanowisko_Pensja AS sp,
    Staż_w_firmie AS s,
    Wysokość_premii AS w,
    Kwalifikacja_do_premii AS k
WHERE
    p.ID = ps.ID
        AND ps.stanowisko = sp.stanowisko
        AND p.ID = s.ID
        AND s.staz = w.staz
        AND k.ID = p.ID
ORDER BY sp.pensja DESC , ID ASC;

select * from zarobki;

#pracownicy, ich działy + liczebnosc i zwierzchnicy
SELECT 
    p.ID,
    p.imie,
    p.nazwisko,
    pd.dzial,
    d.liczba_pracownikow,
    dyr.dyrektor
FROM
    Pracownicy AS p,
    Pracownik_Dzial AS pd,
    Dzial AS d,
    Dyrektorzy AS dyr
WHERE
    p.ID = pd.ID AND pd.dzial = d.dzial
        AND d.dzial = dyr.dzial
ORDER BY liczba_pracownikow DESC , d.dzial DESC , ID ASC;

#dział,budżet, liczebność i dyrektor
SELECT distinct
    d.dzial,
    d.budzet,
    d.liczba_pracownikow,
    dyr.dyrektor
FROM
    Dzial AS d,
    Dyrektorzy AS dyr
WHERE
    d.dzial = dyr.dzial
ORDER BY liczba_pracownikow DESC , d.dzial DESC;

#tworzę drugi widok
CREATE VIEW organizacja AS
    SELECT DISTINCT
        d.dzial, d.budzet, d.liczba_pracownikow, dyr.dyrektor
    FROM
        Dzial AS d,
        Dyrektorzy AS dyr
    WHERE
        d.dzial = dyr.dzial
    ORDER BY liczba_pracownikow DESC , d.dzial DESC;
    
select * from organizacja;

#jw + budżet w przeliczeniu na pracownika
SELECT distinct
    d.dzial,
    d.budzet,
    d.liczba_pracownikow,
    dyr.dyrektor,
    (d.budzet/d.liczba_pracownikow) as 'budzet na pracownika'
FROM
    Dzial AS d,
    Dyrektorzy AS dyr
WHERE
    d.dzial = dyr.dzial
ORDER BY liczba_pracownikow DESC , d.dzial DESC;

#grupowanie po działach + srednia i suma pensji w dziale
SELECT 
    d.dzial,
    d.budzet,
    d.liczba_pracownikow,
    dyr.dyrektor,
    (d.budzet / d.liczba_pracownikow) AS 'budzet na pracownika',
    AVG(sp.pensja) AS 'srednia pensja',
    SUM(sp.pensja) AS 'suma pensji'
FROM
    Dzial AS d,
    Pracownik_Dzial AS pd,
    Dyrektorzy AS dyr,
    Pracownicy AS p,
    Pracownik_Stanowisko AS ps,
    Stanowisko_Pensja AS sp
WHERE
    d.dzial = dyr.dzial
        AND pd.dzial = d.dzial
        AND p.ID = pd.ID
        AND p.ID = ps.ID
        AND ps.stanowisko = sp.stanowisko
GROUP BY d.dzial
ORDER BY liczba_pracownikow DESC , d.dzial DESC;

#jw - dyrektor + suma pensji/budzet 
SELECT 
    d.dzial,
    d.budzet,
    d.liczba_pracownikow,
    ROUND((d.budzet / d.liczba_pracownikow), 2) AS 'budzet na pracownika',
    ROUND(AVG(sp.pensja), 2) AS 'srednia pensja',
    SUM(sp.pensja) AS 'suma pensji',
    ROUND(SUM(sp.pensja) / d.budzet, 2) AS 'udział pensji w budżecie'
FROM
    Dzial AS d,
    Pracownik_Dzial AS pd,
    Pracownicy AS p,
    Pracownik_Stanowisko AS ps,
    Stanowisko_Pensja AS sp
WHERE
    pd.dzial = d.dzial AND p.ID = pd.ID
        AND p.ID = ps.ID
        AND ps.stanowisko = sp.stanowisko
GROUP BY d.dzial
ORDER BY budzet DESC , liczba_pracownikow DESC;

#widok na podstawie powyższego

CREATE VIEW statystyki AS
    SELECT 
    d.dzial,
    d.budzet,
    d.liczba_pracownikow,
    ROUND((d.budzet / d.liczba_pracownikow), 2) AS 'budzet na pracownika',
    ROUND(AVG(sp.pensja), 2) AS 'srednia pensja',
    SUM(sp.pensja) AS 'suma pensji',
    ROUND(SUM(sp.pensja) / d.budzet, 2) AS 'udział pensji w budżecie'
FROM
    Dzial AS d,
    Pracownik_Dzial AS pd,
    Pracownicy AS p,
    Pracownik_Stanowisko AS ps,
    Stanowisko_Pensja AS sp
WHERE
    pd.dzial = d.dzial AND p.ID = pd.ID
        AND p.ID = ps.ID
        AND ps.stanowisko = sp.stanowisko
GROUP BY d.dzial
ORDER BY budzet DESC , liczba_pracownikow DESC;

select * from statystyki;

#historia zatrudnienia pracownikow

SELECT 
    p.ID, p.imie, p.nazwisko, h.*
FROM
    Pracownicy AS p,
    Historia_zatrudnienia AS h
WHERE
    p.ID = h.ID
ORDER BY p.ID ASC;

#jw + staż u byłego pracodawcy

SELECT 
    p.imie,
    p.nazwisko,
    h.*,
    (YEAR(h.data_odejscia) - YEAR(h.data_zatrudnienia)) AS doswiadczenie
FROM
    Pracownicy AS p,
    Historia_zatrudnienia AS h
WHERE
    p.ID = h.ID
ORDER BY p.ID ASC;

#ilu pracowników przyszło od poszczególnych pracodawców

SELECT 
    h.poprz_pracodawca, COUNT(*) AS pracownicy
FROM
    Pracownicy AS p,
    Historia_zatrudnienia AS h
WHERE
    p.ID = h.ID
GROUP BY h.poprz_pracodawca
ORDER BY COUNT(*) DESC;

#ilu pracowników z doswiadczeniem powyżej 3lat przyszło od poszczególnych pracodawców

SELECT 
    h.poprz_pracodawca, COUNT(*) AS pracownicy
FROM
    Pracownicy AS p,
    Historia_zatrudnienia AS h
WHERE
    p.ID = h.ID
        AND (YEAR(h.data_odejscia) - YEAR(h.data_zatrudnienia)) > 3
GROUP BY h.poprz_pracodawca
ORDER BY COUNT(*) DESC;

#pracodawcy, od których przyszło więcej niż 5 "doświadczonych" pracowników
SELECT 
    h.poprz_pracodawca, COUNT(*) AS pracownicy
FROM
    Pracownicy AS p,
    Historia_zatrudnienia AS h
WHERE
    p.ID = h.ID
        AND (YEAR(h.data_odejscia) - YEAR(h.data_zatrudnienia)) > 3
GROUP BY h.poprz_pracodawca
HAVING pracownicy > 5
ORDER BY COUNT(*) DESC;

#pracownicy,doswiadczenie i pensje + tworzę widok
create view historia as
SELECT 
    p.imie,
    p.nazwisko,
    h.poprz_pracodawca,
    (YEAR(h.data_odejscia) - YEAR(h.data_zatrudnienia)) AS doswiadczenie,
    sp.pensja
FROM
    Pracownicy AS p,
    Historia_zatrudnienia AS h,
    Pracownik_Stanowisko AS ps,
    Stanowisko_Pensja AS sp
WHERE
    p.ID = h.ID AND p.ID = ps.ID
        AND ps.stanowisko = sp.stanowisko
ORDER BY doswiadczenie DESC , sp.pensja DESC;

select * from historia;

#pracownicy i wykształcenie

SELECT 
    p.imie, p.nazwisko, w.*
FROM
    Pracownicy AS p,
    Wykształcenie AS w
WHERE
    p.ID = w.ID
ORDER BY p.ID ASC;

#liczba pracownikow z poszczególnymi tytulami

SELECT 
    tytul, COUNT(*)
FROM
    Pracownicy AS p,
    Wykształcenie AS w
WHERE
    p.ID = w.ID
GROUP BY tytul
ORDER BY p.ID ASC;

#jw + srednia pensja => widok

CREATE VIEW tytul_a_pensja AS
    SELECT 
        tytul, COUNT(*), ROUND(AVG(sp.pensja), 2)
    FROM
        Pracownicy AS p,
        Wykształcenie AS w,
        Pracownik_Stanowisko AS ps,
        Stanowisko_Pensja AS sp
    WHERE
        p.ID = w.ID AND p.ID = ps.ID
            AND ps.stanowisko = sp.stanowisko
    GROUP BY tytul
    ORDER BY ROUND(AVG(sp.pensja), 2) DESC;

SELECT 
    *
FROM
    tytul_a_pensja;
    
/*tworzę trigger, który po dodaniu nowego pracownika do tabeli Pracownik_Dzial zwiększa o jeden liczbę pracowników
dla danego działu w tabeli Dzial*/

delimiter $$
create trigger aktualizacja_liczby_prac
after insert on Pracownik_Dzial 
for each row 
begin
update Dzial set liczba_pracownikow = liczba_pracownikow + 1 where dzial=new.dzial; 
end;
$$

#sprawdzenie

show triggers;

select * from organizacja;

insert into Pracownik_Dzial values (31,'IT');

select * from organizacja;

