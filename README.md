# anki_ENG-PL
### Skrypt CLI pozwalający na automatyczne tworzenie fiszek z tłumaczeniami wyrazów, przykładami zdań i wymową, w formie transkrypcji fonetycznej i TTS.
\
![image](https://user-images.githubusercontent.com/124788184/236870532-dcd2f2cc-b588-4970-a9c4-f94832610a87.png)

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

