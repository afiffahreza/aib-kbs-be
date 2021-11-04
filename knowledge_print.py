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
    @DefFacts()
    def _initial_fact(self):
        yield Fact(score=0)
        yield Fact(demam="n")
        yield Fact(batuk_dahak="n")
        yield Fact(pilek="n")
        yield Fact(tanyapilek=False)
        yield Fact(tanyabatuk=False)
        yield Fact(batuk="n")
        yield Fact(tanyadahak=False)
        yield Fact(tanyasesak=False)
        yield Fact(tanyalemas=False)
        yield Fact(sesak="n")
        yield Fact(lemas="n")

    @Rule(NOT(Fact(suhu=W())))
    def tanya_suhu(self):
        self.declare(
            Fact(suhu=float(input("Berapa suhu tubuh anda saat ini? "))))

    @Rule(NOT(Fact(riwayat_suhu=W())))
    def tanya_riwayat_suhu(self):
        self.declare(Fact(riwayat_suhu=float(input(
            "Berapa suhu tubuh tertinggi anda 48 jam terakhir? "))))

    @Rule(Fact(demam="n"),
          Fact(suhu=MATCH.suhu),
          Fact(riwayat_suhu=MATCH.riwayat_suhu),
          OR(TEST(lambda suhu: suhu > 37.5),
             TEST(lambda riwayat_suhu: riwayat_suhu > 37.5)))
    def cek_demam(self):
        self.modify(self.facts[2], demam="y")

    @Rule(Fact(tanyapilek=W()))
    def tanya_pilek(self):
        self.modify(self.facts[4], pilek=input(
            "Apakah anda mengalami pilek dalam 48 jam terakhir? (y/n) "))
        self.retract(self.facts[5])

    @Rule(Fact(tanyabatuk=W()))
    def tanya_batuk(self):
        self.modify(self.facts[7], batuk=input(
            "Apakah anda mengalami batuk dalam 48 jam terakhir? (y/n) "))
        self.retract(self.facts[6])

    @Rule(Fact(tanyadahak=W()),
          Fact(batuk="y"))
    def tanya_dahak(self):
        self.modify(self.facts[3], batuk=input(
            "Apakah batuk anda berlendir? (y/n) "))
        self.retract(self.facts[8])

    @Rule(Fact(tanyasesak=W()))
    def tanya_sesak(self):
        self.modify(self.facts[11], sesak=input(
            "Apakah anda mengalami sesak napas dalam 48 jam terakhir? (y/n) "))
        self.retract(self.facts[9])

    @Rule(Fact(tanyalemas=W()))
    def tanya_lemas(self):
        self.modify(self.facts[12], lemas=input(
            "Apakah anda merasa lemas dalam 48 jam terakhir? (y/n) "))
        self.retract(self.facts[10])

    @Rule(Fact(batuk_dahak='n'),
          Fact(batuk='y'),
          Fact(pilek="y"),
          Fact(demam="y"),
          Fact(lemas="y"),
          Fact(sesak="y"))
    def print_covid(self):
        print("Anda berkemungkinan tinggi covid")
        print(self.facts)

    @Rule(NOT(AND(Fact(batuk_dahak='n'),
          Fact(pilek="y"),
          Fact(batuk='y'),
          Fact(demam="y"),
          Fact(lemas="y"),
          Fact(sesak="y"))))
    def print_tidak_covid(self):
        print("Anda berkemungkinan rendah covid")
        print(self.facts)


engine = CovidCheck()
engine.reset()
engine.run()
