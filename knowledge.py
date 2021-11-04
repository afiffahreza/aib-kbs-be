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
# - Batuk kering
# - Sesak napas
# - Demam/Riwayat demam
# - Pilek
# - Lemas
# Idenya nanti harus input gejala yang diambil dari https://covid19.go.id/peta-sebaran.
# Knowledge engine nanti ngecek kalo semua gejalanya terpenuhi berarti covid

from experta import *


class CovidCheck(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.COVID = False

    @DefFacts()
    def _declare_initial_fact(self, suhu, batuk, dahak, pilek, sesak, lemas):
        yield Fact(suhu=suhu)
        yield Fact(batuk=batuk)
        yield Fact(dahak=dahak)
        yield Fact(pilek=pilek)
        yield Fact(sesak=sesak)
        yield Fact(lemas=lemas)
        yield Fact(tesdemam=False)
        yield Fact(demam="n")

    @Rule(Fact(demam="n"),
          Fact(tesdemam=False),
          Fact(suhu=MATCH.suhu),
          TEST(lambda suhu: suhu > 37.5))
    def cek_demam(self):
        print(self.facts)
        self.modify(self.facts[7], demam="y")
        self.retract(self.facts[6])

    @Rule(Fact(dahak='n'),
          Fact(batuk='y'),
          Fact(pilek="y"),
          Fact(demam="y"),
          Fact(lemas="y"),
          Fact(sesak="y"))
    def print_covid(self):
        self.COVID = True
        # print("Anda berkemungkinan tinggi covid")
        # print(self.facts)

    @Rule(NOT(AND(Fact(dahak='n'),
          Fact(pilek="y"),
          Fact(batuk='y'),
          Fact(demam="y"),
          Fact(lemas="y"),
          Fact(sesak="y"))))
    def print_tidak_covid(self):
        self.COVID = False
        # print("Anda berkemungkinan rendah covid")
        # print(self.facts)
