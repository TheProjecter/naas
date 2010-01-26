This diskette contains the Osorio IAEA test spectra prepared in 
December 1995. For more detailed information, the reader is referred to
the IAEA TecDocs describing the testspectra and the Intercomparison where
the spectra were used.

The files on this diskette are organized into four directories: One
directory for the testspectra, one for the reference data, one for some
programs and one for an example file to be tested.


THE TESTSPC DIRECTORY
---------------------

In the \testspc directory, the testspectra can be found.
All spectra are in ASCII format, 1 channel per line, 8192 channels, integer
format. The first two channels contain real and live counting time in
seconds.

The files are the following:
CALIB.ASC: calibration spectrum containing Co-57, Cs-137, Na-22, Mn-54 and
	   Co-60. To give a rough idea of the energy calibration, here's a
	   few channels and energies:

	   Channel       Energy (keV)
	   301           122.06
	   1281          511.00
	   1661          661.66
	   2097          834.84
	   2951         1173.24
	   3207         1274.54
	   3353         1332.50

STRAIGHT.ASC: Ra-226 + progeny spectrum, counted 2000 s.
DISTORT.ASC:  same, but counted in the presence of a Am-241 source to
	      induce high-energy tailing.
ADD1N1.ASC:   Sum of two Ra-226 spectra, one of them shifted by 3 channels
	      to the right.
ADD3N1.ASC:   Sum of two Ra-226 spectra, one counted 2000 s, one 667 s.,
	      the second shifted to the right left by 3 channels.
ADD1N3.ASC:   Sum of two Ra-226 spectra, one counted 2000 s, one 667 s,
	      the second shifted to the left by 3 channels.
ADD10N1.ASC:  Sum of two Ra-226 spectra, one counted 2000 s, one 200 s,
	      the second shifted to the right by 3 channels.
ADD1N100.ASC: Sum of two Ra-226 spectra, one counted 2000 s, one 20 s,
	      the second shifted to the left by 3 channels


THE REFRSL DIRECTORY
--------------------

In the \refrsl directory, the reference lists of peak areas are given
for each spectrum, with the same filename but with the *.ref or *.rhf
extension. The first contain all peaks that could be found in the
spectrum with the best extimate of their areas and its 1 standard
deviation uncertainty. The second (with the *.rhf extension) contain
the same information, but only the peaks that can be found in the
first 4096 channels of the spectrum.


THE PROGS DIRECTORY
-------------------

This directory contains three versions of the program that reports the
comparison of output results of any program and the reference values.
The first and most improtant version is 'cmpspec.exe'. The second one is
'cmpspcs.exe', which does exactly the same thing but outputs only the final
table of chisqr values to be described. The third version is 'cmprat.exe'.
This program computes the average ratio of peak areas between the two
files.
Each program is a standard, non-interactive DOS application.
Each can be called without arguments or with the /h option to get help.
To use 'cmpspec.exe' for comparison with the IAEA reference values, use
the following call:

cmpspec straight.ref test.dat

where 'straight.ref' is an example of the filename of a file containing
reference data. The second argument, 'test.dat' is a file
containing the analysis results to be tested. The data in 'test.dat'
must be formatted as follows (example in the example directory):

- 1 peak per line
- for each peak: Energy dE Area dA
  where Energy is the peak energy in keV, Area is the photopeak area
  and the uncertainties dE and dA are both abolute 1 standard deviation
  uncertainties. The values can be given in any numeric format but
  must be separated by spaces.

The program output can be redirected to file or show one page at a time
with the standard DOS redirection and piping commands.
You can also run a test of your own with the cmpspec program: You can
compare any two lists of peaks in the format described above that you
would expect to be equal in a statistical sense of the word. If you
wish to do this, you will first have to prepare your own reference
file. The format is the same as for the TEST.DAT file, except for an
extra item per line: After the uncertainty in the area, the number 0
or 1 is listed to indicate whether the peak should be considered in
the comparison or not (0: do not consider, 1: consider). This parameter
is useful in the case of peaks that could not be analyzed acuurately
even in the reference spectrum. You can look at the format of the
reference files on this diskette as example: The 295 keV peak has been
labelled as unquantifiable in the STRAIGHt.REF file.

Now, to run your own comparison, you need to call the program with
three parameters:

cmpspec ref.dat test.dat factor

where factor is the ratio of the counting times of the spectrum
underlying the ref.dat file and the spectrum underlying the test.dat
file. In the case of the IAEA test this ratio was 20: The reference
spectrum had been counted 40,000 seconds, the test spectra
2000 seconds. The factor 20 is taken as default if you omit this
parameter in the command.


OUTPUT FORMAT 

The program will output a table of the following form:

---------------------------------------------------------------------------

This report was generated by CMPSPEC (version Dec 11 1995, 20:20:42)

---------------------------------------------------------------------------
           'TRUE' DATA          |         MEASURED DATA        |             
           STRAIGHT.REF         |         HYPSTRAI.OPC         |
---------------------------------------------------------------------------
        E      |        A       |       E      |       A       |   Z-scores  
    val   unc  |   val    unc   |   val   unc  |   val     unc |  rep   ref
---------------------------------------------------------------------------
   106.7   0.1 |     101    24  |  106.7   0.1 |       0   109 |       -0.9
   156.4   0.4 |     117    17  |  156.4   0.4 |       0    77 |       -1.5
   186.2   0.1 |   18035    36  |  186.2   0.0 |   17786   182 | -1.3  -1.5
   196.3   0.1 |     357    16  |  196.3   0.1 |       0    74 |       -4.7
   200.9   0.1 |       0     0  |  200.9   0.1 |     345    98 |  3.5 
...
   277.9   0.2 |       0     0  |  277.9   0.2 |     280   109 |  2.6 
   280.9   0.2 |     253    22  |  280.9   0.2 |     332   113 |  0.7   0.8
*  295.2   0.5 |   61144   610  |  294.8   0.0 |   55912   667 |  0.0   0.0
*  295.2   0.5 |   61144   610  |  295.5   0.1 |    5495   604 |  0.0   0.0
*  298.0   0.3 |     215    23  |  298.0   0.3 |       0   106 |        0.0
   304.1   0.1 |      49     6  |  304.1   0.1 |       0    30 |       -1.6

   474.4   0.1 |     216    11  |  474.4   0.1 |       0    51 |       -4.1
   480.4   0.1 |     703    15  |  479.9   0.0 |     601    49 | -2.0  -1.5
   487.0   0.1 |     800    13  |  486.5   0.0 |     809    54 |  0.2   0.1
...
   502.1   0.1 |      46    10  |  502.1   0.1 |       0    47 |       -0.9
A  509.5   0.1 |       0     0  |  509.5   0.1 |    1279   118 | 10.8 
A  511.0   0.1 |    3548    21  |  511.0   0.1 |    1741   125 |-14.3 -18.6
   533.6   0.1 |     348     8  |  533.0   0.1 |     294    52 | -1.0  -1.3
   536.7   0.1 |     106     8  |  536.7   0.1 |       0    36 |       -2.8
...
COMPARISON RESULTS

TRUE MATCHES
    Number of matches for high peaks: 47
      related chisqr for areas and reported uncertainty:  0.7 *
      and for reported areas with reference uncertainty:  1.1
    Number of matches for small peaks on high continuum: 20
      related chisqr for areas and reported uncertainty:  3.1 *
      and for reported areas with reference uncertainty:  2.3 *
    Number of matches for small peaks on low continuum: 18
      related chisqr for areas and reported uncertainty:  1.7
      and for reported areas with reference uncertainty:  1.6
  Number of non-511 matches all together: 85
    related chisqr for areas and reported uncertainty:  1.5 *
    and for reported areas with reference uncertainty:  1.5 *
    and the chisqr for their positions:  11.8 *

FITTING THE 511 keV PEAK
  Number of peaks found there: 2
    related chisqr:                   160.3 *

MISSES AND FALSE HITS
  Number of misses: 82
    related chisqr:                    7.0 *
  Number of false hits: 15
    related chisqr:                   13.8 *


TOTALS
  Number of regarded peaks: 184
    related chisqr for areas:          6.7 *


CONSTANTS USED:
  Second spectrum was counted 20.0 times shorter than the first.
  Threshold energy: 100.00 keV.
  Criteria for energy matching:
     E1 - E2  <  2 * sqrt(sqr(dE1) + sqr(dE2)), or
     E1 - E2  <  0.5 * FWHM(E1).
  Criterion for high significance: A/ref_err > 10.
  Criterion for high continuum: 3.0 * net < gross.
  Criterion for annihilaton peak: |E - 511| < 3.0.

----------------------------------------------------------------------------

The presented data are the following:

First, the program states its name and compilation time and date.
Then, the comparison table is printed. This table contains one peak per
line. For peak area given:
   The reference peak positon and its uncertainty, taken from the *.REF
   file, and the reference area and its uncertainty, Ar and dAr.
   The measured position, its incertainty, the measured area and its
   uncertainty, Am and dAm, taken from the *.DAT file.
   A standardized difference between the two, computed as

                                Am - Ar
                     z =  -------------------
                          sqrt(dAm^2 + dAr^2)

   and a second standardized difference, where not the reported uncertainty
   was used, but the reference uncertainty multiplied by the square root
   of the ratio of the counting times. This second Z-score is meaningful
   only in the case of singlets, as encountered in the STRAIGHT spectrum.

There are two cases where the Z-score cannot be computed with this formula:
The peaks may have been detected by the program to be tested even though
it's not really there (false hit) or it may not have been detected even
though it is there in reality (miss). In the case of a false hit, the
Z-score is computed as

                                  Am
                     z =  -------------------
                                 dAm

In the case of a miss, the Z-score is computed as

                                  Ar
                     z =  -------------------
                                 C*dAr

where C is the square root of the ratio of the counting times.

The Z-scores are squared, added and divided by the number of scores
added to get a kind of reduced chisqr value. These chisqr values are
computed and reported for different groups of peaks, and then averaged,
weighted with their respective numbers of degrees of freedom, to obtain
chisqr values corresponding to larer groups of peaks, until finally a
'grand total' chisqr is obtained.

The groups of peaks are:
- High peaks: peaks with a siginificance exceeding 10
- Low peaks on high background
- Low peaks on low background
- The 511 peak
- False hits   ("type 2 error")
- False misses ("type 1 error")

If the filename of the reference file is 'STRAIGHT.REF' or 'STRAIGHT.RHF',
the program will output two chisqrs for the first three groups: The ones
based on the Z-scores computed with the reported uncertainties and the ones
based on the Z-scores computed with the reference uncertainties only. The
latter are meaningless in the case of spectra with many multiplets.
Therefore, if the filename of the reference file is not one of the two
mentioned, the program assumes it is comparing results of a complex
spectrum and will only report the chisqr values of the first kind.

The exact criteria applied by the program to divide the peaks into groups
given at the end of the output.