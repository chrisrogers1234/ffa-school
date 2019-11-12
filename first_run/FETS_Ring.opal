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

/////////////////// GENERAL ////////////////////////////////////
REAL R0 = 4.; // reference radius
REAL N_CELLS=15; // NOTE!! If you change the number of cells, you must *by hand*
                 // change the number of ringprobes
REAL FFA_CELL_LENGTH=2*PI/N_CELLS; // length of a cell in the FFA
REAL RADIANS = PI/180; // units
REAL RMIN=R0-2.0; // minimum radius for tracking
REAL RMAX=R0+2.0; // maximum radius for tracking
REAL N_TURNS=5.1; // number of turns to track through
REAL STEP_SIZE_MM=10.0; // step size in mm
REAL PERIOD=1152.13; // time taken to go through one revolution of the ring
REAL MM=1000.0; // unit conversion

//////////// BEAM PARAMETERS //////////////////
REAL E0 = 2.55/1000; // initial energy [GeV]
REAL BEAM_THETA_INIT=0.0; // beam initial rotation
REAL BEAM_PHI_INIT=0.0; // [fraction of cell length]; 0 is on RINGPROBE01
REAL BEAM_CHARGE=1.0; // [fraction of cell length]; 0 is on RINGPROBE01
REAL LATTICE_PHI_OFFSET=0.0; // [fraction of cell length]; 0 means centre of cell lines up with phi = 0.

/////////// MAIN MAGNET //////////////////////
REAL FFA_B_MEAN=0.492; // [T]; mean field over the entire cell at R0
REAL FFA_DF_RATIO=-0.36; // []; BD/BF
REAL FFA_F_LENGTH=0.2; // [fraction of cell length]; F magnet length
REAL FFA_D_LENGTH=0.1; // [fraction of cell length]; D magnet length
REAL FFA_TAN_DELTA=-0.8692867378162267; // []; tan(delta) where delta is spiral angle
REAL FFA_FIELD_INDEX=7.1; // []; field index k
REAL FFA_MAX_Y_POWER=2; // []; maximum power in field expansion off midplane 
REAL FFA_F_END_LENGTH=0.0756285955107769; // [] end length in multiples of centre length
REAL FFA_D_END_LENGTH=0.5520887472286714; // [] end length in multiples of centre length
REAL FFA_NEG_EXTENT=1.0; // radial extent inwards from R0 [m]
REAL FFA_POS_EXTENT=1.0; // radial extent outwards from R0 [m]

/////////////////// RING PROBES //////////////////////////////////
REAL RING_PROBE_PHI_OFFSET=0.0;

BUILD_PROBE(NAME, ANGLE): MACRO {
    NAME: PROBE, xstart=RMIN*MM*cos(ANGLE), xend=RMAX*MM*cos(ANGLE),
                 ystart=RMIN*MM*sin(ANGLE),  yend=RMAX*MM*sin(ANGLE);
}

REAL THIS_PROBE_PHI=RING_PROBE_PHI_OFFSET;
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
REAL FFA_BF=-FFA_B_MEAN/(FFA_F_LENGTH+FFA_DF_RATIO*FFA_D_LENGTH);
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

REAL C_LIGHT = 300.; // mm/ns

REAL STEP_SIZE_NS = STEP_SIZE_MM/(P0/(E0+M_P)*C_LIGHT); // ns

REAL BFREQ = 1./1.15213; // MHz;
REAL STEPS_PER_TURN = 1.e3/BFREQ/STEP_SIZE_NS;
REAL MAX_STEPS = N_TURNS*STEPS_PER_TURN;
REAL CO_OFFSET = -1*R0; // 


value, {BFREQ, STEP_SIZE_NS, STEP_SIZE_MM, MAX_STEPS, STEPS_PER_TURN};

value, {START_D, END_D, FFA_D_CENTRE_LENGTH, FFA_BD};
value, {START_F, END_F, FFA_F_CENTRE_LENGTH, FFA_BF};
REAL DF_RATIO = FFA_BD/FFA_BF;
REAL MEAN_B = (FFA_BD*FFA_D_CENTRE_LENGTH + FFA_BF*FFA_F_CENTRE_LENGTH)/FFA_CELL_LENGTH;
value, {DF_RATIO, MEAN_B};
value, {D_PHI_DRIFT, DX_DRIFT, DY_DRIFT, DXN_DRIFT, DYN_DRIFT};
REAL BEAM_PHI_INIT_RAD=FFA_CELL_LENGTH*BEAM_PHI_INIT*180/PI; // 


ringdef: RINGDEFINITION, HARMONIC_NUMBER=1, LAT_RINIT=R0, LAT_PHIINIT=0,
         LAT_THETAINIT=0.0, BEAM_PHIINIT=BEAM_PHI_INIT_RAD, BEAM_PRINIT=BEAM_THETA_INIT,
         BEAM_RINIT=R0+CO_OFFSET, SYMMETRY=1, RFFREQ=1, IS_CLOSED=false,
         MIN_R=R0-2, MAX_R=R0+2;

halfDrift: LOCAL_CARTESIAN_OFFSET, end_position_x=DX_DRIFT*MM,
                                   end_position_y=DY_DRIFT*MM,
                                   end_normal_x=DXN_DRIFT,
                                   end_normal_y=DYN_DRIFT;
magnetD: ScalingFFAGMagnet, B0=FFA_BD,
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
magnetF: ScalingFFAGMagnet, B0=FFA_BF,
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
latticeOffset: LOCAL_CARTESIAN_OFFSET, end_position_x=DX_LATT*MM,
                                       end_position_y=DY_LATT*MM,
                                       end_normal_x=DXN_LATT,
                                       end_normal_y=DYN_LATT;

cell: Line = (halfDrift, magnetF, magnetD, halfDrift);
ring: Line = (ringdef,
            latticeOffset,
            cell, cell, cell, cell, cell,
            cell, cell, cell, cell, cell,
            cell, cell, cell, cell, cell
            , ringprobe
           );

Dist1: DISTRIBUTION, TYPE=fromfile, FNAME="disttest.dat", INPUTMOUNITS=NONE;

Fs1:FIELDSOLVER, FSTYPE=None, MX=5, MY=5, MT=5,
                 PARFFTX=true, PARFFTY=false, PARFFTT=false,
                 BCFFTX=open, BCFFTY=open, BCFFTT=open,BBOXINCR=2;

beam1: BEAM, PARTICLE=PROTON, pc=P0, NPART=1, BCURRENT=1.6e-19, CHARGE=1.0, BFREQ=BFREQ;

TRACK, LINE=ring, BEAM=beam1, MAXSTEPS=MAX_STEPS, STEPSPERTURN=STEPS_PER_TURN;
RUN, METHOD="CYCLOTRON-T", BEAM=beam1, FIELDSOLVER=Fs1, DISTRIBUTION=Dist1;
ENDTRACK;
STOP;

