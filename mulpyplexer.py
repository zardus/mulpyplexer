class MP(object):
    def __init__(self, items):
        self.mp_items = items

    @staticmethod
    def _resolve_object(a, n):
        return a if not isinstance(a, MP) else a.mp_items[n]

    def _expand(self, o):
        expanded = [ ]

        for n in range(len(self.mp_items)):
            if isinstance(o, dict):
                e = { k:self._resolve_object(a, n) for (k,a) in o.items() }
            elif isinstance(o, list):
                e = [ self._resolve_object(a, n) for a in o ]
            elif isinstance(o, tuple):
                e = tuple(self._resolve_object(a, n) for a in o)
            else:
                e = self._resolve_object(o, n)

            expanded.append(e)

        return expanded

    def __repr__(self):
        return "<MP with %d items of types %s>" % (len(self.mp_items), '/'.join(frozenset(i.__class__.__name__ for i in self.mp_items)))

    #
    # Plex-throughs!
    #

    def __getattr__(self, k):
        keys = self._expand(k)
        return MP([ getattr(i, k) for i,k in zip(self.mp_items,keys) ])

    def __call__(self, *args, **kwargs):
        expanded_args, expanded_kwargs = self._expand(args), self._expand(kwargs)
        return MP([ i(*a, **k) for i,a,k in zip(self.mp_items,expanded_args,expanded_kwargs) ])

    def __getitem__(self, k):
        keys = self._expand(k)
        return MP([ i[k] for i,k in zip(self.mp_items,keys) ])

    def mp_len(self):
        return [ len(i) for i in self.mp_items ]

    def __dir__(self):
        attrs = frozenset.intersection(*[frozenset(dir(i)) for i in self.mp_items])
        return list(sorted(attrs | { 'mp_items', 'mp_len' } ))

def test():
    class A:
        def __init__(self, i):
            self.i = i

        def add(self, j):
            return A(self.i + (j.i if isinstance(j, A) else j))

        def sub(self, j):
            return A(self.i - (j.i if isinstance(j, A) else j))

        def __repr__(self):
            return "<A %d>" % self.i

        def str(self):
            return str(self.i)

        def __eq__(self, o):
            return self.i == o.i

    one = MP([ A(10), A(20), A(30) ])

    two = one.add(5)
    assert two.mp_items == [ A(15), A(25), A(35) ]

    three = two.sub(10)
    assert three.mp_items == [ A(5), A(15), A(25) ]

    four = three.add(one)
    assert four.mp_items == [ A(15), A(35), A(55) ]

    five = four.str()
    assert five.mp_items == [ "15", "35", "55" ]

    six = four.i
    assert six.mp_items == [ 15, 35, 55 ]

if __name__ == '__main__':
    test()
