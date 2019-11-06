Option, ECHO=TRUE;
//////////////////////////////////////////////////////////////////////////////
// Input file for single bunch tracking through ERIT FFA ring              //
//////////////////////////////////////////////////////////////////////////////
Title,string="Small ring using OPAL code";
Option, ASCIIDUMP=TRUE;
Option, ENABLEHDF5=FALSE;
OPTION, PSDUMPFREQ=100000;
Option, VERSION=10900;
Option, SPTDUMPFREQ=1;
Option, STATDUMPFREQ=100000;

//////////// BEAM PARAMETERS //////////////////
REAL E0 = 2.55/1000; // [GeV]
REAL BEAM_THETA_INIT=0.0; // fraction of E0
REAL BEAM_PHI_INIT=0.0; // [fraction of cell length]; 0 is on PROBE01
REAL BEAM_CHARGE=1.0; // [fraction of cell length]; 0 is on PROBE01
REAL LATTICE_PHI_OFFSET=0.0; // [fraction of cell length]; 0 means centre of cell lines up with phi = 0.

//////////// PROBES /////////////////////
REAL CELL_PROBE_OFFSET=5; // [number of cells]
REAL PHI_TEST_PROBE=0.0; // [number of cells]

/////////// MAIN MAGNET //////////////////////
REAL FFA_B_MEAN = -0.492; // [T]; mean field over the entire cell at R0
REAL FFA_DF_RATIO=-0.36; // []; BD/BF
REAL FFA_F_LENGTH=0.2; // [fraction of cell length]
REAL FFA_D_LENGTH=0.1; // [fraction of cell length]
REAL FFA_TAN_DELTA=-0.8692867378162267; // []
REAL FFA_FIELD_INDEX=7.1; // []
REAL FFA_MAX_Y_POWER=2; // []
REAL FFA_F_END_LENGTH=0.0756285955107769; // [] end length in multiples of centre length
REAL FFA_D_END_LENGTH=0.5520887472286714; // [] end length in multiples of centre length
REAL FFA_NEG_EXTENT=1.0; // [m]
REAL FFA_POS_EXTENT=2.0; // [m]

/////////////////// GENERAL ////////////////////////////////////

REAL R0 = 4.;
REAL N_CELLS=15; // NOTE!! If you change the number of cells, you must *by hand*
                 // change the number of ringprobes
REAL FFA_CELL_LENGTH=2*PI/N_CELLS;
REAL CO_OFFSET = -1*R0;
REAL MILLIMETRE = 1.0;
REAL RADIANS = PI/180;
REAL RMIN=R0-2.0;
REAL RMAX=R0+2.0;
REAL BEAM_PHI_INIT_RAD=FFA_CELL_LENGTH*BEAM_PHI_INIT*180/PI;


/////////////////// RING PROBES //////////////////////////////////
REAL RING_PROBE_PHI_OFFSET=0.0;
REAL PROBE_PHI=(+2.)*PI/N_CELLS*(1.0+RING_PROBE_PHI_OFFSET);
BUILD_PROBE(NAME, ANGLE): MACRO {
    NAME: PROBE, xstart=RMIN*1000*cos(ANGLE),  xend=RMAX*1000*cos(ANGLE),  ystart=RMIN*1000*sin(ANGLE),  yend=RMAX*1000*sin(ANGLE);
}

REAL THIS_PROBE_PHI=BEAM_PHI_INIT_RAD;
BUILD_PROBE(RingProbe01, THIS_PROBE_PHI);
THIS_PROBE_PHI = EVAL(THIS_PROBE_PHI+2.*PI/N_CELLS);
BUILD_PROBE(RingProbe02, THIS_PROBE_PHI);
THIS_PROBE_PHI = EVAL(THIS_PROBE_PHI+2.*PI/N_CELLS);
BUILD_PROBE(RingProbe03, THIS_PROBE_PHI);
THIS_PROBE_PHI = EVAL(THIS_PROBE_PHI+2.*PI/N_CELLS);
BUILD_PROBE(RingProbe04, THIS_PROBE_PHI);
THIS_PROBE_PHI = EVAL(THIS_PROBE_PHI+2.*PI/N_CELLS);
BUILD_PROBE(RingProbe05, THIS_PROBE_PHI);
THIS_PROBE_PHI = EVAL(THIS_PROBE_PHI+2.*PI/N_CELLS);
BUILD_PROBE(RingProbe06, THIS_PROBE_PHI);
THIS_PROBE_PHI = EVAL(THIS_PROBE_PHI+2.*PI/N_CELLS);
BUILD_PROBE(RingProbe07, THIS_PROBE_PHI);
THIS_PROBE_PHI = EVAL(THIS_PROBE_PHI+2.*PI/N_CELLS);
BUILD_PROBE(RingProbe08, THIS_PROBE_PHI);
THIS_PROBE_PHI = EVAL(THIS_PROBE_PHI+2.*PI/N_CELLS);
BUILD_PROBE(RingProbe09, THIS_PROBE_PHI);
THIS_PROBE_PHI = EVAL(THIS_PROBE_PHI+2.*PI/N_CELLS);
BUILD_PROBE(RingProbe10, THIS_PROBE_PHI);
THIS_PROBE_PHI = EVAL(THIS_PROBE_PHI+2.*PI/N_CELLS);
BUILD_PROBE(RingProbe11, THIS_PROBE_PHI);
THIS_PROBE_PHI = EVAL(THIS_PROBE_PHI+2.*PI/N_CELLS);
BUILD_PROBE(RingProbe12, THIS_PROBE_PHI);
THIS_PROBE_PHI = EVAL(THIS_PROBE_PHI+2.*PI/N_CELLS);
BUILD_PROBE(RingProbe13, THIS_PROBE_PHI);
THIS_PROBE_PHI = EVAL(THIS_PROBE_PHI+2.*PI/N_CELLS);
BUILD_PROBE(RingProbe14, THIS_PROBE_PHI);
THIS_PROBE_PHI = EVAL(THIS_PROBE_PHI+2.*PI/N_CELLS);
BUILD_PROBE(RingProbe15, THIS_PROBE_PHI);
THIS_PROBE_PHI = EVAL(THIS_PROBE_PHI+2.*PI/N_CELLS);

ringprobe: Line = (RingProbe01, RingProbe02, RingProbe03, RingProbe04, RingProbe05, 
                   RingProbe06, RingProbe07, RingProbe08, RingProbe09, RingProbe10,
                   RingProbe11, RingProbe12, RingProbe13, RingProbe14, RingProbe15);

/////////////////// CELL PROBES //////////////////////////////////

REAL PROBE_OFF=(+2.)*PI/N_CELLS*CELL_PROBE_OFFSET;
REAL PROBE_DELTA_PHI=(+2.)*PI/N_CELLS/20;
REAL PROBE_PHI=0*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe01: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);
REAL PROBE_PHI=1*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe02: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);
REAL PROBE_PHI=2*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe03: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);
REAL PROBE_PHI=3*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe04: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);
REAL PROBE_PHI=4*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe05: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);
REAL PROBE_PHI=5*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe06: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);
REAL PROBE_PHI=6*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe07: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);
REAL PROBE_PHI=7*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe08: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);
REAL PROBE_PHI=8*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe09: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);
REAL PROBE_PHI=9*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe10: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);
REAL PROBE_PHI=10*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe11: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);
REAL PROBE_PHI=11*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe12: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);
REAL PROBE_PHI=12*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe13: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);
REAL PROBE_PHI=13*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe14: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);
REAL PROBE_PHI=14*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe15: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);
REAL PROBE_PHI=15*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe16: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);
REAL PROBE_PHI=16*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe17: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);
REAL PROBE_PHI=17*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe18: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);
REAL PROBE_PHI=18*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe19: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);
REAL PROBE_PHI=19*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe20: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);
REAL PROBE_PHI=20*PROBE_DELTA_PHI+PROBE_OFF;
CellProbe21: PROBE, xstart=RMIN*1000*cos(PROBE_PHI),  xend=RMAX*1000*cos(PROBE_PHI),  ystart=RMIN*1000*sin(PROBE_PHI),  yend=RMAX*1000*sin(PROBE_PHI);

cellprobe: Line = (CellProbe01, CellProbe02, CellProbe03, CellProbe04, CellProbe05, 
                   CellProbe06, CellProbe07, CellProbe08, CellProbe09, CellProbe10,
                   CellProbe11, CellProbe12, CellProbe13, CellProbe14, CellProbe15,
                   CellProbe16, CellProbe17, CellProbe18, CellProbe19, CellProbe20,
                   CellProbe21);

/////////////////// TEST PROBE ///////////////////////////////////

REAL PHI_TEST_PROBE_RAD=PHI_TEST_PROBE*FFA_CELL_LENGTH;
value, {PHI_TEST_PROBE_RAD};

TestProbe: PROBE, xstart=RMIN*1000*cos(PHI_TEST_PROBE_RAD),  xend=RMAX*1000*cos(PHI_TEST_PROBE_RAD),  
                  ystart=RMIN*1000*sin(PHI_TEST_PROBE_RAD),  yend=RMAX*1000*sin(PHI_TEST_PROBE_RAD);



/////////////////// MAIN MAGNETS //////////////////////////////////

// Aim is that DF ratio controls relative amount of bend out vs bend in (and associated quad strengths)
// independent of the magnet length parameters
// * B_MEAN controls the total dipole field;
// * DF_RATIO controls the relative amount of vertical vs horizontal focussing
// * FIELD_INDEX controls the focusing strength of each magnet and width of the magnet
// * TAN_DELTA controls tan delta
// * END_LENGTH and MAX_Y_POWER control the degree of non-linearity
// * DF_RATIO, END_LENGTH and TAN_DELTA also control the vertical tune 
// * RF_VOLTAGE, RF_PHASE controls the RF voltage and phase

// length
REAL FFA_F_CENTRE_LENGTH=FFA_CELL_LENGTH*FFA_F_LENGTH;
REAL FFA_D_CENTRE_LENGTH=FFA_CELL_LENGTH*FFA_D_LENGTH;
// field magnitude
REAL FFA_BF=FFA_B_MEAN/(FFA_F_LENGTH+FFA_DF_RATIO*FFA_D_LENGTH);
REAL FFA_BD=FFA_DF_RATIO*FFA_BF;

// Magnet has 2 end lengths; then a centre length; then 2 end lengths
// If STAY_CLEAR=0 then B = B0/2. at the start/end of the magnet
REAL STAY_CLEAR = 2;
REAL START_D = FFA_D_CENTRE_LENGTH*FFA_D_END_LENGTH*STAY_CLEAR;
REAL END_D = FFA_D_CENTRE_LENGTH*(1+FFA_D_END_LENGTH*STAY_CLEAR*2);
REAL START_F = FFA_F_CENTRE_LENGTH*FFA_F_END_LENGTH*STAY_CLEAR;
REAL END_F = FFA_F_CENTRE_LENGTH*(1+FFA_F_END_LENGTH*STAY_CLEAR*2);
REAL D_PHI_DRIFT = (FFA_CELL_LENGTH-END_F- END_D)/2; //
// Bounding box extends for 0.5 centre length + 8 end lengths in each direction
REAL BB = 16;
REAL FFA_D_AZIMUTHAL_EXTENT = FFA_D_CENTRE_LENGTH*(0.5+FFA_D_END_LENGTH*BB);
REAL FFA_F_AZIMUTHAL_EXTENT = FFA_F_CENTRE_LENGTH*(0.5+FFA_F_END_LENGTH*BB);

REAL DX_DRIFT = R0*sin(D_PHI_DRIFT);
REAL DY_DRIFT = R0*(1-cos(D_PHI_DRIFT));
REAL DXN_DRIFT = cos(D_PHI_DRIFT);
REAL DYN_DRIFT = sin(D_PHI_DRIFT);

REAL M_P = 0.93827208; // GeV/c^2
REAL P0 = ((E0+M_P)^2-M_P^2)^0.5; // GeV/c

value, {P0, E0, M_P};

REAL C_LIGHT = 300.; // MM/NS

REAL STEP_SIZE_MM = 1.0; //*STEP_SIZE_NS;
REAL STEP_SIZE_NS = STEP_SIZE_MM/(P0/E0*C_LIGHT);

REAL STEPS_PER_TURN = 2*PI*R0*1000./STEP_SIZE_MM*10./25.; //1000000;
REAL MAX_STEPS = 5.1*STEPS_PER_TURN*3.;
REAL BFREQ = 1.e3/STEPS_PER_TURN/STEP_SIZE_NS*3.18658692e-05*100.;

value, {BFREQ, STEP_SIZE_NS, STEP_SIZE_MM, MAX_STEPS, STEPS_PER_TURN};

value, {START_D, END_D, FFA_D_CENTRE_LENGTH, FFA_BD};
value, {START_F, END_F, FFA_F_CENTRE_LENGTH, FFA_BF};
REAL DF_RATIO = FFA_BD/FFA_BF;
REAL MEAN_B = (FFA_BD*FFA_D_CENTRE_LENGTH + FFA_BF*FFA_F_CENTRE_LENGTH)/FFA_CELL_LENGTH;
value, {DF_RATIO, MEAN_B};
value, {D_PHI_DRIFT, DX_DRIFT, DY_DRIFT, DXN_DRIFT, DYN_DRIFT};

ringdef: RINGDEFINITION, HARMONIC_NUMBER=1, LAT_RINIT=R0, LAT_PHIINIT=0,
         LAT_THETAINIT=0.0, BEAM_PHIINIT=BEAM_PHI_INIT_RAD, BEAM_PRINIT=BEAM_THETA_INIT,
         BEAM_RINIT=R0+CO_OFFSET, SYMMETRY=1, RFFREQ=1, IS_CLOSED=false,
         MIN_R=R0-2, MAX_R=R0+2;

halfDrift: LOCAL_CARTESIAN_OFFSET, end_position_x=DX_DRIFT*MILLIMETRE,
                                   end_position_y=DY_DRIFT*MILLIMETRE,
                                   end_normal_x=DXN_DRIFT,
                                   end_normal_y=DYN_DRIFT;
magnetD: ScalingFFAMagnet, B0=FFA_BD,
                            R0=R0,
                            FIELD_INDEX=FFA_FIELD_INDEX,
                            TAN_DELTA=FFA_TAN_DELTA, 
                            MAX_Y_POWER=FFA_MAX_Y_POWER,
                            CENTRE_LENGTH=R0*FFA_D_CENTRE_LENGTH,
                            END_LENGTH=R0*FFA_D_CENTRE_LENGTH*FFA_D_END_LENGTH,
                            RADIAL_NEG_EXTENT=FFA_NEG_EXTENT,
                            RADIAL_POS_EXTENT=FFA_POS_EXTENT,
                            MAGNET_START=R0*START_D,
                            MAGNET_END=R0*END_D,
                            HEIGHT=1.,
                            AZIMUTHAL_EXTENT=R0*FFA_D_AZIMUTHAL_EXTENT;
magnetF: ScalingFFAMagnet, B0=FFA_BF,
                            R0=R0,
                            FIELD_INDEX=FFA_FIELD_INDEX,
                            TAN_DELTA=FFA_TAN_DELTA,
                            MAX_Y_POWER=FFA_MAX_Y_POWER,
                            CENTRE_LENGTH=R0*FFA_F_CENTRE_LENGTH,
                            END_LENGTH=R0*FFA_F_CENTRE_LENGTH*FFA_F_END_LENGTH,
                            RADIAL_NEG_EXTENT=FFA_NEG_EXTENT,
                            RADIAL_POS_EXTENT=FFA_POS_EXTENT,
                            MAGNET_START=R0*START_F,
                            MAGNET_END=R0*END_F,
                            HEIGHT=1.,
                            AZIMUTHAL_EXTENT=R0*FFA_F_AZIMUTHAL_EXTENT;


///////////// FIELD OUTPUT ////////////////////////////////////////////////////

REAL MAP_NR_STEPS=400;
REAL MAP_R_STEP=(FFA_POS_EXTENT+FFA_NEG_EXTENT)/MAP_NR_STEPS;

DUMPFIELDS, X_START=-5., X_STEPS=501, DX=0.02, Y_START=-5., Y_STEPS=501, DY=0.02, Z_START=0.001, Z_STEPS=1, DZ=0.100, FILE_NAME="FieldMapXY.dat";
DUMPEMFIELDS, COORDINATE_SYSTEM=CYLINDRICAL, R_START=R0-FFA_NEG_EXTENT, R_STEPS=MAP_NR_STEPS, DR=MAP_R_STEP, PHI_START=-24.*RADIANS, PHI_STEPS=24.*8*4, DPHI=0.25*RADIANS, Z_START=0, Z_STEPS=1, DZ=0.100, T_START=0, T_STEPS=1, DT=1., FILE_NAME="FieldMapRPHI.dat";
DUMPEMFIELDS, COORDINATE_SYSTEM=CYLINDRICAL, R_START=R0, R_STEPS=80, DR=0.01, PHI_START=0.*RADIANS,  PHI_STEPS=1,   DPHI=1*RADIANS,    Z_START=0, Z_STEPS=1, DZ=0.100, T_START=0., T_STEPS=1, DT=2., FILE_NAME="ProbeField.dat";

REAL D_PHI_LATT=LATTICE_PHI_OFFSET*FFA_CELL_LENGTH;
REAL DX_LATT = R0*sin(D_PHI_LATT);
REAL DY_LATT = R0*(1-cos(D_PHI_LATT));
REAL DXN_LATT = cos(D_PHI_LATT);
REAL DYN_LATT = sin(D_PHI_LATT);
latticeOffset: LOCAL_CARTESIAN_OFFSET, end_position_x=DX_LATT*MILLIMETRE,
                                       end_position_y=DY_LATT*MILLIMETRE,
                                       end_normal_x=DXN_LATT,
                                       end_normal_y=DYN_LATT;

cell: Line = (halfDrift, magnetF, magnetD, halfDrift);
l1: Line = (ringdef,
            latticeOffset,
            cell, cell, cell, cell, cell,
            cell, cell, cell, cell, cell,
            cell, cell, cell, cell, cell
            , ringprobe
            , cellprobe
            , testprobe
           );

Dist1: DISTRIBUTION, TYPE=fromfile, FNAME="disttest.dat", INPUTMOUNITS=NONE;

Fs1:FIELDSOLVER, FSTYPE=None, MX=5, MY=5, MT=5,
                 PARFFTX=true, PARFFTY=false, PARFFTT=false,
                 BCFFTX=open, BCFFTY=open, BCFFTT=open,BBOXINCR=2;

beam1: BEAM, PARTICLE=PROTON, pc=P0, NPART=1, BCURRENT=1.6e-19, CHARGE=1.0, BFREQ=BFREQ;

TRACK, LINE=l1, BEAM=beam1, MAXSTEPS=MAX_STEPS, STEPSPERTURN=STEPS_PER_TURN;
RUN, METHOD="CYCLOTRON-T", BEAM=beam1, FIELDSOLVER=Fs1, DISTRIBUTION=Dist1;
ENDTRACK;
STOP;

