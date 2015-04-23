from distutils.core import setup

setup(
    name='mulpyplexer',
    description='A module that multiplexes interactions with lists of python objects.',
    long_description='''
Mulpyplexer is a piece of code that can multiplex interactions with lists of python objects.
It's easier to show you:

    import mulpyplexer

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

    one = mulpyplexer.MP([ A(10), A(20), A(30) ])

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
''',
    author='Yan Shoshitaishvili',
    author_email='yans@yancomm.net',
    maintainer='Yan Shoshitaishvili',
    maintainer_email='yans@yancomm.net',
    version='0.03',
    license='GPL',
    py_modules=['mulpyplexer']
)
