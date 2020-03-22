from citation.citation import CitationType, Citation, Person
from citation.citation_parsing import parse_citation, find_known_authors
from citation.field_parsing import parse_citation_fields
from citation.intermediate_citation import IntermediateCitation


def test_parse_citation():
    raw_citation = IntermediateCitation(
        volume=1,
        raw_text='1. Lexikon der islamischen Welt. Klaus Kreiser, Werner Diem, Hans Georg Majer ed. 3 Bde., Stuttgart, 1974 (Urban-Taschenbücher, 200/1-3).'
    )
    parsed_citation = parse_citation(raw_citation)

    assert parsed_citation == IntermediateCitation(
        remaining_text='{{{ title }}}.  {{{ editors }}}   {{{ number_of_volumes }}} '
                       '{{{ location }}} {{{ date_published }}}{{{ series }}}.',
        raw_text='1. Lexikon der islamischen Welt. Klaus Kreiser, Werner Diem, Hans '
                 'Georg Majer ed. 3 Bde., Stuttgart, 1974 (Urban-Taschenbücher, '
                 '200/1-3).',
        series='Urban-Taschenbücher, 200/1-3',
        editors='Klaus Kreiser, Werner Diem, Hans Georg Majer',
        location='Stuttgart',
        number='1',
        number_of_volumes='3',
        title='Lexikon der islamischen Welt',
        date_published='1974',
        type=CitationType.COLLECTION,
        volume=1,
        keywords=[],
    )


def test_parse_collection():
    raw_text = '98. Russian colonial expansion to 1917. Eingeleitet von Sy ed Z. abedin. Michael Rywkin ed. London, 1988, XVΠ+274 S.'
    raw_citation = IntermediateCitation(volume=1, raw_text=raw_text)
    parsed_citation = parse_citation(raw_citation)
    assert parsed_citation == IntermediateCitation(
        volume=1, number='98', type=CitationType.COLLECTION,
        editors='Michael Rywkin',
        remaining_text='Russian colonial expansion to 1917. Eingeleitet von Sy ed Z. abedin.  {{{ editors }}}  London, 1988, XVΠ+274 S.',
        raw_text=raw_text
    )


def test_find_known_authors():
    raw_text = '12. Handžić, Adem Problematika sakupljanja i izdavanja turskih istorij-skih izvora u radu Orijentalnog Instituta. In: POF 20-21.1970/71 (1974).213-221. [Die Problematik der Erfassung und Herausgabe der türkischen historischen Quellen im Rahmen der Arbeiten des Orientalischen Instituts in Sarajevo, Jugoslavien.]'
    raw_citation = IntermediateCitation(volume=1, raw_text=raw_text)
    parsed_citation = parse_citation_fields(parse_citation(raw_citation))
    [parsed_citation] = find_known_authors([parsed_citation], ['Handžić, Adem'])

    assert parsed_citation == Citation(
        volume=1,
        number=12,
        type=CitationType.ARTICLE,
        authors=[Person(last='Handžić', first='Adem', raw='Handžić, Adem')],
        title='Problematika sakupljanja i izdavanja turskih istorij-skih izvora u radu Orijentalnog Instituta',
        comments=[
            'Die Problematik der Erfassung und Herausgabe der türkischen historischen Quellen im Rahmen der Arbeiten des Orientalischen Instituts in Sarajevo, Jugoslavien'
        ],
        reviews=[],
        raw_text=raw_text,
        published_in={'journal': 'POF', 'volumeStart': 20, 'volumeEnd': 21, 'yearStart': 1970, 'yearEnd': 1971,
                      'yearParentheses': 1974, 'pageStart': 213, 'pageEnd': 221, 'type': 'journal',
                      'raw': 'POF 20-21.1970/71 (1974).213-221'}, ta_references=[],
        remaining_text='{{{ authors }}} {{{ title }}} {{{ in }}}'
    )


def test_find_title_before_field_marker():
    raw_text = '1667. ArsenijeviĆ, Lazar-Batalaka     Istorija srpskog ustanka. Vladimir stojancević ed. Beograd, 1979, 1 S.'
    parsed_citation = parse_citation_and_fields(raw_text)
    assert parsed_citation.title == 'Istorija srpskog ustanka'


def test_13_1584():
    raw_text = '1584. Mehrländer, Ursula     Türkische Jugendliche - keine beruflichen Chancen in Deutschland? Bonn, 1983, 228S.'
    parsed_citation = parse_citation_and_fields(raw_text)
    assert parsed_citation.location == 'Bonn'
    assert parsed_citation.date_published == {'year': 1983}
    assert parsed_citation.number_of_pages == '228'
    assert parsed_citation.title == 'Türkische Jugendliche - keine beruflichen Chancen in Deutschland?'
    assert parsed_citation.authors[0].first == 'Ursula'
    assert parsed_citation.authors[0].last == 'Mehrländer'
    assert parsed_citation.fully_parsed()


def parse_citation_and_fields(raw_text):
    raw_citation = IntermediateCitation(volume=1, raw_text=raw_text)
    parsed_citation = parse_citation_fields(parse_citation(raw_citation))
    return parsed_citation



def test_does_not_crash():
    citations = [
        '337. Özkirimli, Atillâ   Nedim. [Istanbul, 1974],  175 S. [Der Dichter Nedīm, ca. 1681-1730.]',
        "301. Yotjnous, Emre   Poèmes. Guzine Dino—Marc Delouze trs. Paris, 1973, 41 S.",
        "863. Nye, Roger P.   The military in Turkish politics, 1960-1973. Diss., Washington University, 1974, 302 S. (UM 74-22,540). Abstract in: DAI 35.4.1974-1975.2358-A.",
        "222. Süleyman the Magnificent and his age [s.TA 22 - 23.293]. Rez. György domokos, 110.4.1997.814.",
        "9. Dërfer, G.    0 sostojanii tjurkologii v Federativnoj Respublike Germanii. In: ST 1974.6.98-109. [Die Turkologie in der Bundesrepublik Deutschland.]",
        "1272. DEVECI, Hasan A.    Cyprus yesterday, today — what next? London, 1976, 1 + 60 S. (Cyprus Turkish Association, 2).",
        "660. Kramer, Gerhard F.—McGrew, Roderick E.  Potemkin, the Porte, and the road to Tsargrad. The Shumla negotiations, 1789-1790. In: CASS 8.4.1974.467-487.",
        "1226. Pollo, St. - Pulaha, S.     Akte të Rilindjes kombëtare shqiptare 1878-1912 [s. TA 5.1496, 6.1621].",
        '1018. PlNON, Pierre       Les villes du pont vues par le Père de Jerphanion.      e g Tokat, Amasya, Sivas. In: TA 25.240.859-865.                                      CO Ό',
        '3. Biographisches Lexikon zur Geschichte Südosteuropas. Mathias Bernath und Felix v. Schroeder ed., Gerda Bartl (Red.). Bd. 1, Α-F. München, 1974, XV+557 S. (Südosteuropäische Arbeiten, 75). Rez. Gerhard Stadler, Donauraum 19.3.-4.1974.209. — Johann Weidlein, SODV 23.3.1974.218.',
        '701. Brouček, Peter-LEiτscH, Walter-VocELKA, Karl—Wimmer, Jan-Wój-cıκ, Zbigniew Der Sieg bei Wien 1683. Wien-Warszawa, 1983, 187 S. 70 Abb., 4 Schlachtpläne, 1 Faltplan.',
        '117. Leningrad, 2.-4. VI. 1969: III Tjurkologičeskaja konferencija. 3. Turkologische Konferenz; die Referate sind abgedruckt in TA 1.89. Bericht: V.G.Guzev,N. A.Dulina,L. Ju.Tuguševa, TA 1.89.403-412.',
        '879. ALLAMANI,   E.-PANAYOTOPOULOU, Κ.      ΊΙ   συμμαχική  εντολή για τήν κατάληψη της Σμύρνης και ή δραστηριοποίηση της ελληνικής ηγεσίας. In: ΤΑ 7.160.119-172 [The Allied decision concerning the Greek mandate on the occupation of Smyrna.]',
        '291. Fourtis, Georgios N. Στρατıωτıκòv fλλη vo-τoυpκıκòv λεξıκóv. 2 Bde. Athenai, 1977. [Militärisches Fachwörterbuch Griechisch-Türkisch.]',
        '16. Kononov, Α. N. Nekotorye itogi razvitija sovetskoj tjurkologii i zadaci Sovetskogo komiteta tjurkologov. In: ST 1974.2.3-12. [Einige Ergebnisse der Entwicklung der sowjetischen Turkologie und die Aufgaben des Sowjetischen Komitee der Turkologen.]',
        '1. Lexikon der islamischen Welt. Klaus Kreiser, Werner Diem, Hans Georg Majer ed. 3 Bde., Stuttgart, 1974 (Urban-Taschenbücher, 200/1-3).',
        '200. Ramazanov, K. T. Türk dillärinin ğänub-ğarb ġrupunda ġoša sözlär (jemäk-ičmäk adları). ADI 1974.2.51-60. [Wortpaare in den südwestlichen Turksprachen: Speisen und Getränke. Russ. Res.]',
        '2392. Johnson,   C.   D.      Regular   disharmony   in   Kirghiz.   In: TA 10.274.8^-99.',
        '954. Ebied, R. Y.—M. J. L. Young. A list of Ottoman governors of Aleppo, A. H. 1002-1168. In: AION 34.1.1974.103-108.',
        '191. Ljubljana (Laibach), 4.-5. XII. 1975: Jugoslovenska orijentalistika i nesvrstani svijet [Die jugoslavische Orientalistik und die blockfreie Welt].',
        '3. Biographisches Lexikon zur Geschichte Südosteuropas [s. TA 1.3, 2.3, 3.3].',
    ]
    for raw_citation in citations:
        parsed_citation = parse_citation(IntermediateCitation(volume=1, raw_text=raw_citation))
        assert parsed_citation.number.isdigit()
        assert parsed_citation.raw_text == raw_citation
        assert isinstance(parsed_citation, IntermediateCitation)
