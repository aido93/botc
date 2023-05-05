#!/usr/bin/env python3

import sys
import math

N=int(sys.argv[1])
baronPresents=(sys.argv[2] == 'true')

if N<7:
    print("script is not ready yet")
    sys.exit(1)

# Initial setup
playersCount = {
                                         # N 7 8 9 10 11 12 13 14 15
    'citizen':  5 + 2 * ((N - 7) // 3),  #   5 5 5 7  7  7  9  9  9
    'outcast':  (N - 7) % 3,             #   0 1 2 0  1  2  0  1  2
    'henchman': 1 + (N - 7) // 3         #   1 1 1 2  2  2  3  3  3
}

bads = 1 + playersCount['henchman']

if baronPresents:
    playersCount['citizen'] -= 2
    playersCount['outcast'] += 2

henchmen = ['poisoner', 'spy', 'harlot', 'baron']
outcasts = ['butler', 'drunker', 'recluse', 'saint']

# probability that specific henchman card is in the game
henchmanProbability = playersCount['henchman']/len(henchmen)
# probability that specific outcast card is in the game
outcastProbability = playersCount['outcast']/len(outcasts)

def personInitialUncertainty():
    return bads/(N-1)

def personInitialConfidence():
    return 1 - personInitialUncertainty()

def pairInitialUncertainty():
    return bads/(N-1) + bads/(N-2) - bads/(N-1)*bads/(N-2)

def pairInitialConfidence():
    return 1 - pairInitialUncertainty()

## Person
#print(f"Initial confidence  that arbitrary person is good: {round(personInitialConfidence() * 100)}%")
#print(f"Initial uncertainty that arbitrary person is good: {round(personInitialUncertainty() * 100)}%\n")

## Pair
#print(f"Initial confidence  that arbitrary pair is good: {round(pairInitialConfidence() * 100)}%")
#print(f"Initial uncertainty that arbitrary pair is good: {round(pairInitialUncertainty() * 100)}%")

### POISONED OR DRUNKER ###
def isPoisoned():
    # probability that specific role is Drunker in fact
    # For example, 7 citizens and 1 drunker
    drunkerProbability = outcastProbability / (playersCount['citizen']+1)
    # Poisoner does not poison the Demon or henchmen
    poisoned = 1 / (N - bads)
    # It can be only if poisoner in the game
    poisoned *= henchmanProbability 
    # Poisoner cannot poison drunker twice
    p = poisoned + drunkerProbability - poisoned*drunkerProbability
    return p

#print(f"Is specific person poisoned: {round(isPoisoned() * 100)}%\n")

# Each variant is possible by any reason
def pairApriorProbability(badsInThePair):
    if badsInThePair == 2:
        return bads/(N-1) * (bads-1)/(N-2)
    elif badsInThePair == 1:
        return 2 * bads/(N-1) * (N - bads - 1)/(N-2)
    elif badsInThePair == 0:
        return (N - bads - 1)/(N-1) * (N - bads - 2)/(N-2)
    else:
        raise Exception("Imposible number of bads")

# So it's time for the Bayes theorem!
# https://ru.wikipedia.org/wiki/%D0%A2%D0%B5%D0%BE%D1%80%D0%B5%D0%BC%D0%B0_%D0%91%D0%B0%D0%B9%D0%B5%D1%81%D0%B0
#   A    - any but specific pair type (for example, hypotese: 'role received 2 good players')
#   B    - role receives this pair by game rules
# P(A)   - aprior probability of A (distinct for '2 good' and for '1 good - 1 bad' and '2 bad' )
# P(B)   - aprior probability of B
# P(B|A) - conditional probability that this pair is shown to a specific role.
# P(A|B) - aposterior probability that role says the truth about the pair (Need to find)
# P(A|B) = P(A) * P(B|A)/P(B)

def bayes(role, badsCount):
    pb = role.PBA(0)*pairApriorProbability(0)+role.PBA(1)*pairApriorProbability(1)+role.PBA(2)*pairApriorProbability(2)
    pAB = (role.PBA(badsCount) / pb) * pairApriorProbability(badsCount)
    return pAB

always = 1
print("Probability this count of red cards has been shown to any role by any reason:")
class Aprior:
    def PBA(self, badsCount):
        return always

class Washer:
    def PBA(self, badsCount):
        poisoned = isPoisoned()
        if badsCount == 0:
            # Always if not poisoned
            p = (1 - poisoned) * always
            # And if poisoned and selected two outcasts
            p += poisoned * playersCount['outcast']/(N-1) * (playersCount['outcast']-1)/(N-2)
            return p
        elif badsCount == 1:
            # Always if not poisoned
            p = (1 - poisoned) * always
            # And if poisoned and selected 1 bad and 1 outcast
            p += poisoned * 2 * playersCount['outcast']/(N-1) * bads/(N-2)
            return p
        elif badsCount == 2:
            # Always if poisoned
            p = poisoned * always
            # And if not poisoned and spy is in the game and washer selects spy and any other red
            p += (1-poisoned)*henchmanProbability * 1/(N-1) * (bads-1)/(N-2)
            return p

class Librarian:
    def PBA(self, badsCount):
        poisoned = isPoisoned()
        if badsCount == 0:
            # Always if not poisoned
            p = (1-poisoned) * always
            # And if poisoned and selected two citizens (No outcast between them)
            p += poisoned * playersCount['citizen']/(N-1)*(playersCount['citizen']-1)/(N-2)
            return p
        elif badsCount == 1:
            # Always if not poisoned
            p = (1-poisoned) * always
            # And if poisoned and selected one citizen and one bad (No outcast between them)
            p += poisoned * playersCount['citizen']/(N-1)*bads/(N-2)
            return p
        elif badsCount == 2:
            # Always if poisoned
            p = poisoned * always
            # And if not poisoned and selected one spy and any other bad
            p += (1-poisoned) * henchmanProbability * 1/(N-1) * (bads-1)/(N-2)
            return p

class Detective:
    def PBA(self, badsCount):
        poisoned = isPoisoned()
        if badsCount == 0:
            # Always if poisoned
            p = poisoned * always
            # And not poisoned but recluse is in the game and he selects it and any other good player
            p += (1-poisoned) * outcastProbability * 1/(N-1) * (N-bads-2)/(N-2)
            return p
        elif badsCount == 1:
            return always
        elif badsCount == 2:
            return always

print("\n==========")
print("First night")
print("==========")
objs = [Aprior(), Washer(), Librarian(), Detective()]
for obj in objs:
    print("\n"+obj.__class__.__name__)
    p0 = bayes(obj, 0)
    print(f"0 - {round(p0*100)}%")
    p1 = bayes(obj, 1)
    print(f"1 - {round(p1*100)}%")
    p2 = bayes(obj, 2)
    print(f"2 - {round(p2*100)}%")
    print("===TOTAL===")
    print(f"2 - {round((p0+p1+p2) * 100)}%")

# FortuneTeller has different behaviour
# A - selected (not)daemon pair
# B - storyteller says Yes/No
class FortuneTeller:
    def PA(self, hypothesis):
        # If there are no Fake Daemon and not poisoned
        if hypothesis:
            # Probability to select real daemon using 2 cards
            return 2/(N-1)
        else:
            # Probability not to find real daemon using 2 cards
            return 1-2/(N-1)
    def PBA(self, answer, hypothesis):
        # Probability that storyteller says Yes/No when receives pair to check
        # Divide good variants from bad variants
        poisoned = isPoisoned()
        daemon = N-2
        fakeDaemon = N-3
        if hypothesis:
            p = (1-poisoned) * (1-outcastProbability) * daemon/(daemon+fakeDaemon)
            p += (1-poisoned) * outcastProbability * daemon/(daemon+2*fakeDaemon)
        else:
            p = (1-poisoned) * (1-outcastProbability) * fakeDaemon/(daemon+fakeDaemon)
            p += (1-poisoned) * outcastProbability * 2*fakeDaemon/(daemon+2*fakeDaemon)
            p += poisoned
        if not answer:
            p = 1-p
        return p
    def PB(self, answer):
        return self.PA(False)*self.PBA(answer, False)+self.PA(True)*self.PBA(answer, True)
    def Bayes(self, answer, hypothesis):
        return self.PA(hypothesis) * self.PBA(answer, hypothesis)/self.PB(answer)

ft = FortuneTeller()
print("\nProbability that FortuneTeller found daemon if storyteller said:")

print("Aprior:")
p0 = ft.PA(False)
print(f"False - {round(p0*100)}%")
p1 = ft.PA(True)
print(f"True  - {round(p1*100)}%")

print("Aposterior:")

pb = ft.PB(False)
print(f"PB False  - {round(pb*100)}%")
pb = ft.PB(True)
print(f"PB True  - {round(pb*100)}%")

print("If storyteller says NO:")
p0 = ft.Bayes(False, False)
print(f"No daemon - {round(p0*100)}%")
p1 = ft.Bayes(False, True)
print(f"Daemon - {round(p1*100)}%")

print("If storyteller says YES:")
p2 = ft.Bayes(True, False)
print(f"No daemon - {round(p2*100)}%")
p3 = ft.Bayes(True, True)
print(f"Daemon - {round(p3*100)}%")
