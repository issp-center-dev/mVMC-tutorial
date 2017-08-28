#!/usr/local/bin/perl
  $PI=3.14159265358979;
  #input!!
  &input;
  #input!!
  $orb_num=$tmp_orb;
  $L_x=$tmp_Lx;
  $L_y=$tmp_Ly;
  $L=$L_x*$L_y;
  $Ns=$L;
  $All_N=$Ns*$orb_num;
  $Particle=1.0;
  printf("CHECK L_x=$L_x L_y=$L_y \n");

  $tmp=2*$All_N;
  $fname=sprintf("zinitial.def");
  open(FILE,">$fname");
  printf FILE "========misawa======== \n";
  printf FILE "NInitial $tmp  \n";
  printf FILE "========misawa======== \n";
  printf FILE "========initial Green functions ====== \n";
  printf FILE "========misawa======== \n";

#
#  $Q1x        = 0;
#  $Q1y        = $PI;
#
#  $Q2x        = $PI;
#  $Q2y        = 0;
#
  $Q3x        = $PI;
  $Q3y        = $PI;
#
  $Intensity = 0.1;

  for($all_i=0;$all_i<$All_N;$all_i++){
    $orb_i  = $all_i%$orb_num;  
    $site_i = ($all_i-$orb_i)/$orb_num;  
    $int_x  = $site_i%$L_x;
    $int_y  = ($site_i-$int_x)/$L_x;
    $theta  = $Q3x*$int_x+$Q3y*$int_y;
    $re     = $Intensity*cos($theta);
    $im     = 0.0;
    printf FILE (" %4d 0 %4d  0 %f %f\n",$all_i,$all_i,0.5*$Particle+$re,$im); 
    printf FILE (" %4d 1 %4d  1 %f %f\n",$all_i,$all_i,0.5*$Particle-$re,$im); 
  }

#  for($all_i=0;$all_i<$All_N;$all_i++){
#    $orb_i  = $all_i%$orb_num;  
#    $site_i = ($all_i-$orb_i)/$orb_num;  
#    $int_x  = $site_i%$L_x;
#    $int_y  = ($site_i-$int_x)/$L_x;
#    $tmp    = $Intensity;   
#    $theta  = $Q1x*$int_x+$Q1y*$int_y;
#    $tmp1   = $Intensity*cos($theta);
#    $theta  = $Q2x*$int_x+$Q2y*$int_y;
#    $tmp2   = $Intensity*cos($theta);
#    #$theta  = 2*$PI*(0.5-rand()); 
#    printf FILE (" %4d 0 %4d 1 %f %f\n",$all_i,$all_i,$tmp1,-$tmp2); 
#    printf FILE (" %4d 1 %4d 0 %f %f\n",$all_i,$all_i,$tmp1,$tmp2); 
#  }



  close(FILE);
 sub input{
  #input START 
  $Lx_cnt=0;
  $Ly_cnt=0;
  $orb_cnt=0;
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
      #printf "AA $tmp[0] $tmp[1] \n";
      $tmp_Lx = $tmp[1];
      $Lx_cnt=1;
    } 
    if($tmp[0] eq 'Ly'){
      #printf "AA $tmp[0] $tmp[1] \n";
      $tmp_Ly = $tmp[1];
      $Ly_cnt=1;
    } 
    if($tmp[0] eq 'orb_num'){
      #printf "AA $tmp[0] $tmp[1] \n";
      $tmp_orb = $tmp[1];
      $orb_cnt=1;
    } 
  }
  if($Lx_cnt==0 || $Ly_cnt==0||$orb_cnt==0){
    printf "FAITAL ERROR IN input.txt !!!!!!!!!!!!! \n";
  }
  #input FINISH
  close(INPUTFILE);
 }
