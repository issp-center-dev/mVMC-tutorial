#!/usr/bin/perl -w 
  #input!!
  &input;
  #input!!
  $L=$Lx*$Ly;
  $Ns=$L;
  $All_N=$Ns*$orb_num;
  printf("CHECK CisAjsCktAlt Lx=$Lx Ly=$Ly orb=$orb_num \n");


  $tmp=2*$All_N*$All_N;
  $fname="SC_cisajscktaltdc.def";
  open(FILE,">$fname");
  printf FILE "========SC ======== \n";
  printf FILE "SCCisAjsCktAltDC $tmp  \n";
  printf FILE "========SC ======== \n";
  printf FILE "========SC ======== \n";
  printf FILE "========SC ======== \n";

  for($ini_i=0;$ini_i<$All_N;$ini_i+=1){
    $all_i  = $ini_i;
    for($j=0;$j<$All_N;$j+=1){
      $inp[0]=$all_i;
      $inp[1]=$j;
      $inp[2]=0;
      $inp[3]=$all_i;
      $inp[4]=$j;
      $inp[5]=1;
      printf FILE "  $inp[0] $inp[2] $inp[1] $inp[2] $inp[3] $inp[5] $inp[4] $inp[5]\n";
      printf FILE "  $inp[1] $inp[2] $inp[0] $inp[2] $inp[4] $inp[5] $inp[3] $inp[5]\n";
    }
  }
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
    if($tmp[0] eq 'Ly'){
      $Ly = $tmp[1];
    } 
    if($tmp[0] eq 'orb_num'){
      $orb_num = $tmp[1];
    } 
  }
  #input FINISH
 }
 
