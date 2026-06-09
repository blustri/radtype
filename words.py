from wonderwords import RandomWord
def generate(n):
    rw = RandomWord()
    words = rw.random_words(n)
    return words

def wordsPerMinute(timeInMinutes, correctWords):
    wpmResult = (correctWords/5)/timeInMinutes
    return wpmResult

def rawWPM(timeInMinutes, totalKeysPressed):
    rwpmResult = (totalKeysPressed/5)/timeInMinutes
    return rwpmResult