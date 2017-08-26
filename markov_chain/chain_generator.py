import random
import operator
import bisect
import json

# Python3 compatibility
try: # pragma: no cover
    basestring
except NameError: # pragma: no cover
    basestring = str

BEGIN = "___BEGIN__"
END = "___END__"

def accumulate(iterable, func=operator.add):
    it = iter(iterable)
    total = next(it)
    yield total
    for element in it:
        total = func(total, element)
        yield total

class Chain(object):
    def __init__(self, corpus, state_size, model=None):
        # `corpus`: A list of lists, where each outer list is a run
        # of the process (e.g., a single sentence), and each inner list
        # contains the steps (e.g., words) in the run. If you want to simulate
        # an infinite process, you can come very close by passing just one, very
        # long run.
        #
        # `state_size`: An integer indicating the number of items the model
        # uses to represent its state. For text generation, 2 or 3 are typical.

        self.state_size = state_size
        self.model = model or self.build(corpus, self.state_size)
        self.precompute_begin_state()

    def build(self, corpus, state_size):
        if (type(corpus) != list) or (type(corpus[0]) != list):
            raise Exception("`corpus` must be list of lists")

        # Using a DefaultDict here would be a lot more convenient, however the memory
        # usage is far higher.
        model = {}

        for run in corpus:
            items = ([ BEGIN ] * state_size) + run + [ END ]
            for i in range(len(run) + 1):
                state = tuple(items[i:i+state_size])
                follow = items[i+state_size]
                if state not in model:
                    model[state] = {}

                if follow not in model[state]:
                    model[state][follow] = 0

                model[state][follow] += 1
        return model

    def precompute_begin_state(self):
        begin_state = tuple([ BEGIN ] * self.state_size)
        choices, weights = zip(*self.model[begin_state].items())
        cumdist = list(accumulate(weights))
        self.begin_cumdist = cumdist
        self.begin_choices = choices

    def move(self, state):
        if state == tuple([ BEGIN ] * self.state_size):
            choices = self.begin_choices
            cumdist = self.begin_cumdist
        else:
            choices, weights = zip(*self.model[state].items())
            cumdist = list(accumulate(weights))
        r = random.random() * cumdist[-1]
        selection = choices[bisect.bisect(cumdist, r)]
        return selection

    def gen(self, init_state=None):
        state = init_state or (BEGIN,) * self.state_size
        while True:
            next_word = self.move(state)
            if next_word == END: break
            yield next_word
            state = tuple(state[1:]) + (next_word,)

    def walk(self, init_state=None):
        return list(self.gen(init_state))

    def to_json(self):
        return json.dumps(list(self.model.items()))

    @classmethod
    def from_json(cls, json_thing):

        if isinstance(json_thing, basestring):
            obj = json.loads(json_thing)
        else:
            obj = json_thing

        if isinstance(obj, list):
            rehydrated = dict((tuple(item[0]), item[1]) for item in obj)
        elif isinstance(obj, dict):
            rehydrated = obj
        else:
            raise ValueError("Object should be dict or list")

        state_size = len(list(rehydrated.keys())[0])

        inst = cls(None, state_size, rehydrated)
        return inst