from pathlib import Path
import os

for script in Path('src/scrapers').glob('*.py'):
    print(script)
    modeldir = Path('data/models')
    
    retval = os.system(f'python {script}')
    assert retval == 0

    modelfile = modeldir / f'{script.stem}.csv'
    assert modelfile.exists()

    outimage = modeldir / f'{script.stem}.png'
    if outimage.exists():
        # remove old image
        outimage.unlink()

    retval = os.system(f'python src/plotmodel.py --model={modelfile} --outfile={outimage} --title="@{script.stem} estimate"')
    assert retval == 0
    assert outimage.exists()

retval = os.system('python src/ensemble_and_plot.py')
assert retval == 0

retval = os.system('python src/tweet.py')
assert retval == 0
