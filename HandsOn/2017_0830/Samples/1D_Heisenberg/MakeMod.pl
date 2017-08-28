#!/usr/local/bin/perl
  #input!!
  &input;
  #input!!
  $fname="StdFace.def";
  open(FILE,">$fname");
  printf FILE "L             = $Lx\n";
  printf FILE "Lsub          = 2\n";
  printf FILE "model         = \"Spin\"\n";
  printf FILE "lattice       = \"chain\"\n";
  printf FILE "J             = 1.0\n";
  printf FILE "2Sz           = 0\n";
  printf FILE "NVMCSample    = 200\n";
  printf FILE "NSROptItrStep = 500\n";
  printf FILE "NSROptItrSmp  = 50\n";
  printf FILE "NMPTrans      = 1\n";
  printf FILE "NSPStot       = $NSPStot\n";
  close(FILE);

  $fname="StdFace_2.def";
  open(FILE,">$fname");
  printf FILE "L             = $Lx\n";
  printf FILE "Lsub          = 2\n";
  printf FILE "model         = \"Spin\"\n";
  printf FILE "lattice       = \"chain\"\n";
  printf FILE "J             = 1.0\n";
  printf FILE "2Sz           = 0\n";
  printf FILE "NVMCSample    = 200\n";
  printf FILE "NSROptItrStep = 200\n";
  printf FILE "NSROptItrSmp  = 100\n";
  printf FILE "NMPTrans      = 1\n";
  printf FILE "NSPStot       = $NSPStot\n";
  close(FILE);


  $fname="StdFace_aft.def";
  open(FILE,">$fname");
  printf FILE "L             = $Lx\n";
  printf FILE "Lsub          = 2\n";
  printf FILE "model         = \"Spin\"\n";
  printf FILE "lattice       = \"chain\"\n";
  printf FILE "J             = 1.0\n";
  printf FILE "2Sz           = 0\n";
  printf FILE "NVMCSample    = 200\n";
  printf FILE "NVMCCalMode   = 1\n";
  printf FILE "NDataIdxStart = 1\n";
  printf FILE "NDataQtySmp   = 5\n";
  printf FILE "NMPTrans      = 1\n";
  printf FILE "NSPStot       = $NSPStot\n";
  close(FILE);



 sub input{
  #input START 
  $file=sprintf("input.txt");
  open(INPUTFILE,$file);
  while($name=<INPUTFILE>){
    chomp $name;
    #DELETE EMPTY
    $_=$name; 
    s/^\s+//;
    $name=$_; 
    @tmp = split /\s+/, $name;
    if($tmp[0] eq 'Lx'){
      $Lx = $tmp[1];
    } 
    if($tmp[0] eq 'NSPStot'){
      $NSPStot = $tmp[1];
    } 
  }
  close(INPUTFILE);
  #input FINISH
 }







