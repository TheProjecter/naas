      
                              JULY 1990      

ASCII FILES OF GAMMA-RAY SPECTRA USED FOR PC DATA REDUCTION EVALUATION

Colin G. Sanderson
US Dept. of Energy - EML
376 Hudson Street
NY, NY 10014  212-620 3642

The gamma-ray spectra on this disk were created by adding varying amounts
of the spectral data from a mixed gamma-ray standard to a random set of data
points.  The random set of data points approximated the shape of a background
spectrum obtained from the same germanium detector used to analyze the mixed 
standard.

FORMAT:  1 Header line
       409 lines of 10I7 (10F7.0) data - 4090 data points.

The random set of data points is labeled: BKG.DAT
Count time for BKG.dat  240000 seconds.
The mixed gamma-ray standard is labeled: CALIBR01.DAT 
Count date for CALIBR01.DAT  22-NOV-89 @ 16:20:52
Count time for CALIB01.DAT   6000 seconds.

CALIBRATION FILE DATA:     Reference date  01-Jul-89 @ 12:00:00 EST

           GAMMA                        GAMMA-RAYS       % TOTAL
ISOTOPE    ENERGY        HALF-LIFE      PER SECOND     UNCERTAINTY
Am-241       59.5 keV   432    Years       769.3           5.0
Cd-109       88         463.9  Days       1154.            4.8
Co-57       122         272.4  Days        551.0           4.5
Ce-139      166         137.7  Days        830.4           4.9
Hg-203      279         46.62  Days       1608.            4.9
Sn-113      392         115.0  Days       1392.            4.4
Sr-85       514         64.85  Days       2001.            5.0
Cs-137      662         30.0   Years      2105.            4.7
Y-88        898         106.66 Days       2922.            4.3
Co-60      1173         5.271  Years      2070.            4.2
Co-60      1332         5.271  Years      2078.            4.8
Y-88       1836         106.66 Days       3078.            4.6


TEST SPECTRA:   GAMMA-RAY         TOTAL NET COUNTS
                ENERGY keV            PER PEAK

                   122                 112768
                   662                 136893
                  1332                  62723

Count time for all TEST spectra is 240000 seconds.

       SPECTRUM     MULTIPLYER     SHIFT            COMMENTS
                                 (CHANNELS)

        TEST01         0.1000        0          Peak Detection
        TEST02         0.0500        0
        TEST03         0.0100        0
        TEST04         0.0050        0
        TEST05         0.0010        0
        TEST06         0.0005        0
        TEST07         0.00025       0
        TEST08         0.0001        0
        TEST09         0.0           0

        TEST10         0.01          0       Doublet Peak Resolution
                       0.01          1          
        TEST11         0.01          0       Peaks of Equal Intensity
                       0.01          2
        TEST12         0.01          0
                       0.01          3
        TEST13         0.01          0
                       0.01          4
        TEST14         0.01          0
                       0.01          5
        TEST15         0.01          0     
                       0.01          6
        TEST16         0.01          0
                       0.01          7
        TEST17         0.01          0
                       0.01          8
        TEST18         0.01          0
                       0.01          9
        TEST19         0.01          0
                       0.01          10



        TEST20         0.1           0       Doublet Peak Resolution
                       0.1           4
        TEST21         0.1           0       Peaks with different intensities
                       0.08          4
        TEST22         0.1           0
                       0.06          4
        TEST23         0.1           0
                       0.04          4
        TEST24         0.1           0
                       0.02          4
        TEST25         0.10          0
                       0.01          4
        TEST26         0.1           0       
                       0.005         4
        TEST27         0.08          0     
                       0.1           4
        TEST28         0.06          0
                       0.1           4
        TEST29         0.04          0
                       0.1           4
        TEST30         0.02          0
                       0.1           4
        TEST31         0.01          0
                       0.1           4
        TEST32         0.005         0
                       0.1           4


        TEST33         Efficiency test at 100 keV
                                          110
                                          140
                                          780

        TEST34         Chernobyl Fallout Data
Count date for TEST34  15-MAY-86 @ 12:00:00
Count time for TEST34  10000 seconds.
        
The mixed gamma-ray standard for TEST34 is labeled: CALIBR02.DAT 
Count date for CALIBR02.DAT  15-MAY-86 @ 16:20:52
Count time for CALIB02.DAT   4000 seconds.

CALIBRATION FILE DATA:     Reference date  16-Nov-85 @ 12:00:00 EST

           GAMMA                        GAMMA-RAYS       % TOTAL
ISOTOPE    ENERGY        HALF-LIFE      PER SECOND     UNCERTAINTY
Cd-109       88         463.9  Days         46.4           5.9
Co-57       122         272.4  Days         39.3           4.5
Ce-139      166         137.7  Days         16.0           5.8
Sn-113      392         115.0  Days         34.0           6.8
Cs-137      662         30.0   Years       315.            5.2
Y-88        898         106.66 Days         78.0           5.8
Co-60      1173         5.271  Years       379.            4.4
Co-60      1332         5.271  Years       380.            4.4
Y-88       1836         106.66 Days         82.0           5.8




END!
           
