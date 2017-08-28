#!/usr/bin/perl -w 
  #input!!
  &input;
  #input!!
  $orb_num=$tmp_orb;
  $L_x=$tmp_Lx;
  $L_y=$tmp_Ly;
  $L=$L_x*$L_y;
  $Ns=$L;
  $All_N=$Ns*$orb_num;
  printf("CHECK CisAjsCktAlt L_x=$L_x L_y=$L_y orb=$orb_num \n");

  $tmp=6*$All_N*$All_N;
  $fname="greentwo.def";
  open(FILE,">$fname");
  printf FILE "========misawa======== \n";
  printf FILE "NCisAjsCktAltDC $tmp  \n";
  printf FILE "========misawa======== \n";
  printf FILE "========Green functions for Sq AND Nq ====== \n";
  printf FILE "========misawa======== \n";

  $cnt=0;
  for($i=0;$i<$All_N;$i+=1){
    for($j=0;$j<$All_N;$j+=1){
      $inp[0]=$i;
      $inp[1]=$i;
      $inp[2]=0;
      $inp[3]=$j;
      $inp[4]=$j;
      $inp[5]=0;
      printf FILE "  $inp[0] $inp[2] $inp[1] $inp[2] $inp[3] $inp[5] $inp[4] $inp[5]\n";
      $cnt+=1;
      $inp[2]=0;
      $inp[5]=1;
      printf FILE "  $inp[0] $inp[2] $inp[1] $inp[2] $inp[3] $inp[5] $inp[4] $inp[5]\n";
      $cnt+=1;
      $inp[2]=1;
      $inp[5]=0;
      printf FILE "  $inp[0] $inp[2] $inp[1] $inp[2] $inp[3] $inp[5] $inp[4] $inp[5]\n";
      $cnt+=1;
      $inp[2]=1;
      $inp[5]=1;
      printf FILE "  $inp[0] $inp[2] $inp[1] $inp[2] $inp[3] $inp[5] $inp[4] $inp[5]\n";
      $cnt+=1;
    }
  }
  for($i=0;$i<$All_N;$i+=1){
    for($j=0;$j<$All_N;$j+=1){
#==============================
      $inp[0]=$i;
      $inp[1]=$j;
      $inp[2]=0;
      $inp[3]=$j;
      $inp[4]=$i;
      $inp[5]=1;
      printf FILE "  $inp[0] $inp[2] $inp[1] $inp[2] $inp[3] $inp[5] $inp[4] $inp[5]\n";
      $cnt+=1;
      $inp[0]=$i;
      $inp[1]=$j;
      $inp[2]=1;
      $inp[3]=$j;
      $inp[4]=$i;
      $inp[5]=0;
      printf FILE "  $inp[0] $inp[2] $inp[1] $inp[2] $inp[3] $inp[5] $inp[4] $inp[5]\n";
      $cnt+=1;
#===============================
    }
   }
 close(FILE);
 if($cnt!=6*$All_N**2){
   printf("ERROR IN CisAjsCktAltDC.prl \n");
 } 
 printf("CisAjsCktAltDC.prl finish \n");

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
 }
 
