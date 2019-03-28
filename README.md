pyNumDiff [![logo](numdiff_avatar.png "Logo Title Text")]
=========================================================

Python based tool to compare putatively simiilar text file. Numerical
values in pairing lines are considered equal if their values return true format

   abs(float1 - float2) <= (aeps + reps * abs(float2))


```
usage: numdiff [-h] [-c <comment char>] [-e rEPS] [-a aEPS] [-C LINES] [-b]
               [-s SPLITRE] [--fixcols FIXCOLS] [-r] [-x PAT] [-I RE] [-q]
               [--matlab] [--verbose]
               <from file> <to file>

Compare two text files with taking into account numerical errors.

positional arguments:
  <from file>
  <to file>

optional arguments:
  -h, --help            show this help message and exit
  -c <comment char>, --comment-char <comment char>
                        Ignore lines starting with the comment char when
                        reading either file. Default: Do not ignore any line.
  -e rEPS, --reps rEPS  Relative error to be accepted in numerial comparisons.
                        Default: 1e-05
  -a aEPS, --aeps aEPS  Absolute error to be accepted in numerial comparisons.
                        Default: 1e-08
  -C LINES, --context LINES
                        Output NUM (default 3) lines of copied context.
  -b, --ignore-space-change
                        Ignore changes in the amount of white space.
  -r, --recursive       Recursively compare any subdirectories found.
  -x PAT, --exclude PAT
                        Exclude files that match PAT.
  -I RE, --ignore-matching-lines RE
                        Ignore changes whose lines all match RE.
  -q, --brief           Output only whether files differ.
  --matlab              Compare MATLAB output, ignore the first lines.
  --verbose             Generate verbose output.

colspec:
  -s SPLITRE, --splitre SPLITRE
                        python regular expression used to split lines before
                        checking for numerical changes
  --fixcols FIXCOLS     Comma separated list of columns for fixed column
                        format files
```
