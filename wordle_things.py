from five_letter_words import *
from math import log2

def fb(guess, ans):
	d = {i:i for i in range(5) if guess[i] == ans[i]}
	for i in range(5):
		if i in d:
			continue
		for j in range(5):
			if j in d.values():
				continue
			if guess[i] == ans[j]:
				d[i] = j
	out = ""
	for i in range(5):
		if i not in d:
			out += "_"
			continue
		elif d[i] == i:
			out += "G"
		else:
			out += "Y"
	return out

def fbc(guess, ans):
	f = fb(guess, ans)
	return f.count("G"), f.count("Y")

l = ['CIGAR', 'REBUT', 'SISSY', 'HUMPH', 'AWAKE', 'BLUSH', 'FOCAL', 'EVADE', 'NAVAL', 'SERVE', 'HEATH', 'DWARF', 'MODEL', 'KARMA', 'STINK', 'GRADE', 'QUIET', 'BENCH', 'ABATE', 'FEIGN', 'MAJOR', 'DEATH', 'FRESH', 'CRUST', 'STOOL', 'COLON', 'ABASE', 'MARRY', 'REACT', 'BATTY', 'PRIDE', 'FLOSS', 'HELIX', 'CROAK', 'STAFF', 'PAPER', 'UNFED', 'WHELP', 'TRAWL', 'OUTDO', 'ADOBE', 'CRAZY', 'SOWER', 'REPAY', 'DIGIT', 'CRATE', 'CLUCK', 'SPIKE', 'MIMIC', 'POUND', 'MAXIM', 'LINEN', 'UNMET', 'FLESH', 'BOOBY', 'FORTH', 'FIRST', 'STAND', 'BELLY', 'IVORY', 'SEEDY', 'PRINT', 'YEARN', 'DRAIN', 'BRIBE', 'STOUT', 'PANEL', 'CRASS', 'FLUME', 'OFFAL', 'AGREE', 'ERROR', 'SWIRL', 'ARGUE', 'BLEED', 'DELTA', 'FLICK', 'TOTEM', 'WOOER', 'FRONT', 'SHRUB', 'PARRY', 'BIOME', 'LAPEL', 'START', 'GREET', 'GONER', 'GOLEM', 'LUSTY', 'LOOPY', 'ROUND', 'AUDIT', 'LYING', 'GAMMA', 'LABOR', 'ISLET', 'CIVIC', 'FORGE', 'CORNY', 'MOULT', 'BASIC', 'SALAD', 'AGATE', 'SPICY', 'SPRAY', 'ESSAY', 'FJORD', 'SPEND', 'KEBAB', 'GUILD', 'ABACK', 'MOTOR', 'ALONE', 'HATCH', 'HYPER', 'THUMB', 'DOWRY', 'OUGHT', 'BELCH', 'DUTCH', 'PILOT', 'TWEED', 'COMET', 'JAUNT', 'ENEMA', 'STEED', 'ABYSS', 'GROWL', 'FLING', 'DOZEN', 'BOOZY', 'ERODE', 'WORLD', 'GOUGE', 'CLICK', 'BRIAR', 'GREAT', 'ALTAR', 'PULPY', 'BLURT', 'COAST', 'DUCHY', 'GROIN', 'FIXER', 'GROUP', 'ROGUE', 'BADLY', 'SMART', 'PITHY', 'GAUDY', 'CHILL', 'HERON', 'VODKA', 'FINER', 'SURER', 'RADIO', 'ROUGE', 'PERCH', 'RETCH', 'WROTE', 'CLOCK', 'TILDE', 'STORE', 'PROVE', 'BRING', 'SOLVE', 'CHEAT', 'GRIME', 'EXULT', 'USHER', 'EPOCH', 'TRIAD', 'BREAK', 'RHINO', 'VIRAL', 'CONIC', 'MASSE', 'SONIC', 'VITAL', 'TRACE', 'USING', 'PEACH', 'CHAMP', 'BATON', 'BRAKE', 'PLUCK', 'CRAZE', 'GRIPE', 'WEARY', 'PICKY', 'ACUTE', 'FERRY', 'ASIDE', 'TAPIR', 'TROLL', 'UNIFY', 'REBUS', 'BOOST', 'TRUSS', 'SIEGE', 'TIGER', 'BANAL', 'SLUMP', 'CRANK', 'GORGE', 'QUERY', 'DRINK', 'FAVOR', 'ABBEY', 'TANGY', 'PANIC', 'SOLAR', 'SHIRE', 'PROXY', 'POINT', 'ROBOT', 'PRICK', 'WINCE', 'CRIMP', 'KNOLL', 'SUGAR', 'WHACK', 'MOUNT']
ll = list(set(get_long_list()) | set(get_short_list()))
sl = get_short_list()
ll = [w.upper() for w in ll]
sl = [w.upper() for w in sl]

def tc(guess):
	tg, ty = 0, 0
	for w in sl:
		g, y = fbc(guess, w)
		tg += g
		ty += y
	return tg, ty

def narrow(conds, lyst=sl):
    out = []
    for w in lyst:
        good = True
        for guess, feedback in conds:
            if fb(guess, w) != feedback:
                good = False
                break
        if good:
            out.append(w)
    return out

def fb_buckets(guess, lyst=sl):
    out = {}
    for w in lyst:
        fbs = fb(guess, w)
        if fbs not in out:
            out[fbs] = []
        out[fbs].append(w)
    return out

def exp_remaining(guess, words, show=False, func=lambda x:x, fracs=False):
    fb_buckets = {}
    for word in words:
        feedback = fb(guess, word)
        fb_buckets[feedback] = fb_buckets.get(feedback, 0) + 1
    if fracs:
        t = sum(v*func(v/len(words)) for v in fb_buckets.values())
    else:
        t = sum(v*func(v) for v in fb_buckets.values())
    if show:
        for k in sorted(fb_buckets.keys(), key=lambda k:fb_buckets[k]):
            print(k, fb_buckets[k])
    return 0 if not words else t/len(words)

def min_exp(words, func=lambda x:x, fracs=False, show=False):
    best_words, best_exp = [], len(words)+1
    c = 0
    scores = {}
    for guess in ll:
        c += 1
        exp = exp_remaining(guess, words, func=func, fracs=fracs)
        if exp < best_exp:
            best_words = [guess]
            best_exp = exp
        elif exp == best_exp:
            best_words.append(guess)
        if show and c%(len(ll)//100) == 0:
            print(c//(len(ll)//100), end=" ")
        scores[guess] = exp
    return best_words, best_exp, scores

def opt_second_guesses(initial):
    feedbacks = ["G____", "_G___", "__G__", "___G_", "____G",
                 "Y____", "_Y___", "__Y__", "___Y_", "____Y",
                 "_____"]
    print("Optimal second guesses for " + initial)
    for feedback in feedbacks:
        nl = narrow([(initial, feedback)])
        opt_words, opt_exp = min_exp(nl)
        opt_exp = max(opt_exp, 1)
        print(feedback, len(nl), opt_words, round(opt_exp, 2), round(len(nl)/opt_exp, 2))

def iterated_max(words,func=lambda x:x, fracs=False,top=20, c=1, feedbacks=[]):
    print("round {}. {} words remain. guesses so far: {}".format(c, len(words), feedbacks))
    if len(words)==1:
        return words[0], c
    if c==7:
        return "bad", 7
    elif len(words)<6:
        return words + ["yfio"], c+1
    _, __, scores = min_exp(words, func, fracs, True)
    top_words = sorted(scores.keys(), key=scores.get)[:top]
    print("Round {} done. Top words: {}".format(c, top_words))
    bw, be = "", 7
    for word in top_words:
        if words==sl:
            print("Running for {}".format(word))
        buckets = fb_buckets(word, words)
        exp_score = 0
        for fb_string, narrowed in buckets.items():
            bfu, cc = iterated_max(narrowed, func, fracs, min(top, max(len(narrowed)//10,1)), c+1, feedbacks+[(word, fb_string)])
            exp_score += len(narrowed)/len(words)*cc
        if exp_score < be:
            bw = word
            be = exp_score
    return bw, be
            

def minimax(words, guesses=ll):
    if len(words)==1:
        return words[0], 1
    bw, bs = "", len(words)
    for guess in guesses:
        buckets = fb_buckets(guess, words)
        if len(buckets) == 1:
            continue
        weights = {fbs:len(buckets[fbs])/len(words) for fbs in buckets}
        scores = {}
        for fbs in weights:
            new_words = narrow([(guess, fbs)], words)
            _, score = minimax(new_words)
            scores[fbs] = score
        exp_score = sum([weights[fbs]*scores[fbs] for fbs in weights])
        if exp_score < bs:
            bs = exp_score
            bw = guess
    return bw, bs
