# anki_ENG-PL
### Skrypt CLI pozwalający na automatyczne tworzenie fiszek z tłumaczeniami wyrazów, przykładami zdań i wymową, w formie transkrypcji fonetycznej i TTS.
\
Do tłumaczenia wyrazów jest używany słownik [diki.pl](https://diki.pl) i [Bab.la](https://bab.la).\
Przykłady zdań są wzięte ze słownika [Bab.la](https://bab.la).\
A wymowa zostaje wygenerowana przez amerykański Google TTS.

## Obsługa
```
pip install requirements.txt
```

Przygotuj dokument tekstowy z wyrazami do przetłumaczenia (każdy w kolejnej linii), a następnie uruchom skrypt:

```
python anki.py words.txt
```

