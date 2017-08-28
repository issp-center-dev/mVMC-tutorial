#!/usr/bin/perl -w 
  #input!!
  &input;
  #input!!
  #$PI=3.14159265358979;
  $all_i=5;
  printf("CHECK L_x=$Lx L_y=$Ly orb=$orb_num \n");
  $Ns = $Lx*$Ly;

  $H=0.0;
  $H_err=0.0;
  $H_2=0.0;
  $H_2_err=0.0;
  $Delta=0.0;
  $Delta_err=0.0;
  for($i=1;$i<=$all_i;$i++){
#===============def input====================
    #$cnt=0;
    $file=sprintf("aft/zvo_out_00%d.dat",$i);
    #print "$file \n";
    open(INPUTFILE,$file);
    while($name=<INPUTFILE>){
      chomp $name;
      #DELETE EMPTY
      $_=$name; 
      s/^\s+//;
      $name=$_; 
      @tmp = split /\s+/, $name;
      printf "$tmp[0]\n";
      $H         += $tmp[0];
      $H_err     += $tmp[0]**2;
      $H_2       += $tmp[2];
      $H_2_err   += $tmp[2]**2;
      $Delta     += $tmp[3];
      $Delta_err += $tmp[3]**2;
    }
    close(INPUTFILE);
  }
  $H=$H/($all_i*1.0);
  $H_err=sqrt(abs($H_err/(1.0*($all_i-1.0))-$all_i/($all_i-1.0)*$H**2))/(sqrt(1.0*$all_i));
  $H_2=$H_2/($all_i*1.0);
  $H_2_err=sqrt(abs($H_2_err/(1.0*($all_i-1.0))-$all_i/($all_i-1.0)*$H_2**2))/(sqrt(1.0*$all_i));
  $Delta=$Delta/($all_i*1.0);
  $Delta_err=sqrt(abs($Delta_err/(1.0*($all_i-1.0))-$all_i/($all_i-1.0)*$Delta**2))/(sqrt(1.0*$all_i));

  $fname="Tmp_energy.dat";
  open(FILE,">$fname");
  printf FILE ("%lf    %lf  ",$H,$H_err);
  printf FILE ("%lf    %lf  ",$H_2,$H_2_err);
  printf FILE ("%lf    %lf  ",$Delta,$Delta_err);
  printf FILE ("\n");
  close(FILE); 

  $fname="Result_energy.dat";
  open(FILE,">$fname");
  printf FILE ("Energy Err  \n");
  printf FILE ("%.16lf    %.16lf  \n",$H,$H_err);
  printf FILE ("\n");
  printf FILE ("Energy/Ns Err/Ns  \n");
  printf FILE ("%.16lf    %.16lf  \n",$H/$Ns,$H_err/$Ns);
  printf FILE ("\n");
  printf FILE ("H2 Err  \n");
  printf FILE ("%.16lf    %.16lf  \n",$H_2,$H_2_err);
  printf FILE ("\n");
  printf FILE ("Variance Err  \n");
  printf FILE ("%.16lf    %.16lf  \n",$Delta,$Delta_err);
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
    #printf "$tmp[0] $tmp[1] \n";
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
  close(INPUTFILE);
  #input FINISH
 }









