from cx_Freeze import setup, Executable

buildOptions = dict(packages=['pickle', 'os', 'sys', 'PyQt5'],
                    excludes=[],
                    includes=[],
                    include_files=['src/data/bigram-freq-dist/bigramFreqDist.pkl',
                                   'src/data/bigram-prob-dist/bigramProbDist.pkl'])

import sys

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('src/app.py', base=base)
]

setup(
    name='Kneser-Ney Word Prediction',
    version='1.0',
    description='PyQt application to demonstrate the Kneser-Ney smoothing ' +
                'algorithm for bigram/word prediction.',
    options=dict(build_exe=buildOptions),
    executables=executables
)