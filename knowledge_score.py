# Expert System RS Hasan Sadikin
# II4042 Kecerdasan Buatan untuk Bisnis

# 18219006 Marcelino Feihan
# 18219014 Zarfa Naida Pratista
# 18219058 Afif Fahreza

# Expert system dibuat menggunakan library python Experta yang terinspirasi dari CLIPS
# https://experta.readthedocs.io/en/latest/
# install pake pip install experta

# Knowledge
# Gejala COVID-19:
# - Batuk kering 65 (35 untuk batuk dahak)
# - Sesak napas 35
# - Demam/Riwayat demam 45
# - Pilek 40
# - Lemas 25
# Idenya nanti harus input gejala yang diambil dari https://covid19.go.id/peta-sebaran.
# Knowledge engine nanti ngecek terus hitung scorenya

from experta import *
from experta.watchers import FACTS


class CovidScoreCheck(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.SCORE = 0

    @DefFacts()
    def _declare_initial_fact(self, suhu, batuk, dahak, pilek, sesak, lemas):
        yield Fact(suhu=suhu)
        yield Fact(batuk=batuk)
        yield Fact(dahak=dahak)
        yield Fact(pilek=pilek)
        yield Fact(sesak=sesak)
        yield Fact(lemas=lemas)
        yield Fact(demam="n")
        yield Fact(tesdemam=False)
        yield Fact(tesbatuk=False)
        yield Fact(tespilek=False)
        yield Fact(tessesak=False)
        yield Fact(teslemas=False)

    @Rule(Fact(demam="n"),
          Fact(tesdemam=False),
          Fact(suhu=MATCH.suhu),
          TEST(lambda suhu: suhu > 37.5))
    def cek_demam(self):
        self.SCORE += 45
        self.modify(self.facts[6], demam="y")
        self.retract(self.facts[7])
        # print(self.facts)
        # print(self.SCORE)

    @Rule(Fact(demam="n"),
          Fact(tesdemam=False),
          Fact(suhu=MATCH.suhu),
          TEST(lambda suhu: suhu <= 37.5))
    def cek_demam_f(self):
        self.retract(self.facts[7])

    @Rule(Fact(tesbatuk=False),
          Fact(batuk="y"),
          Fact(dahak="n"))
    def cek_batuk(self):
        self.SCORE += 65
        self.retract(self.facts[8])

    @Rule(Fact(tesbatuk=False),
          Fact(batuk="y"),
          Fact(dahak="y"))
    def cek_dahak(self):
        self.SCORE += 35
        self.retract(self.facts[8])

    @Rule(Fact(tesbatuk=False),
          Fact(batuk="n"),
          Fact(dahak="n"))
    def cek_batuk_f(self):
        self.retract(self.facts[8])

    @Rule(Fact(tespilek=False),
          Fact(pilek="y"))
    def cek_pilek(self):
        self.SCORE += 40
        self.retract(self.facts[9])
        # print(self.facts)
        # print(self.SCORE)

    @Rule(Fact(tespilek=False),
          Fact(pilek="n"))
    def cek_pilek_f(self):
        self.retract(self.facts[9])

    @Rule(Fact(tessesak=False),
          Fact(sesak="y"))
    def cek_sesak(self):
        self.SCORE += 35
        self.retract(self.facts[10])

    @Rule(Fact(tessesak=False),
          Fact(sesak="n"))
    def cek_sesak_f(self):
        self.retract(self.facts[10])

    @Rule(Fact(teslemas=False),
          Fact(lemas="y"))
    def cek_lemas(self):
        self.SCORE += 25
        self.retract(self.facts[11])

    @Rule(Fact(teslemas=False),
          Fact(lemas="n"))
    def cek_lemas_f(self):
        self.retract(self.facts[11])
