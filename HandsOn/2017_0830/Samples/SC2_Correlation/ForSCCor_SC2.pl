#!/usr/bin/perl -w 
  #input!!
  &input;
  #input!!
  $L=$Lx*$Ly;
  $Ns=$L;
  $All_N=$Ns*$orb_num;
  printf("CHECK CisAjsCktAlt Lx=$Lx Ly=$Ly orb=$orb_num \n");


  $tmp=16*8*$All_N*$All_N;
  $fname="SC_cisajscktaltdc.def";
  open(FILE,">$fname");
  printf FILE "========SC======== \n";
  printf FILE "SCCisAjsCktAltDC $tmp  \n";
  printf FILE "========SC======== \n";
  printf FILE "========SC======== \n";
  printf FILE "========SC======== \n";

  #dwave d_x2-y2
  $near_x[0]=1;
  $near_y[0]=0;

  $near_x[1]=-1;
  $near_y[1]=0;

  $near_x[2]=0;
  $near_y[2]=1;

  $near_x[3]=0;
  $near_y[3]=-1;

  for($ini_i=0;$ini_i<$All_N;$ini_i+=1){
    $all_i  = $ini_i;
    $site_i = $ini_i;
    $i_x=$site_i%$Lx;
    $i_y=($site_i-$i_x)/$Lx;
    for($j=0;$j<$All_N;$j+=1){
      $all_j = $j; 
      $site_j = $j; 
      $j_x=$site_j%$Lx;
      $j_y=($site_j-$j_x)/$Lx;
      for($i_n=0;$i_n<4;$i_n++){
        $i_til_x    = ($i_x+$near_x[$i_n]+$Lx)%$Lx;
        $i_til_y    = ($i_y+$near_y[$i_n]+$Ly)%$Ly;
        $site_i_til = $i_til_y*$Lx+$i_til_x;
        for($j_n=0;$j_n<4;$j_n++){
          $j_til_x=($j_x+$near_x[$j_n]+$Lx)%$Lx;
          $j_til_y=($j_y+$near_y[$j_n]+$Ly)%$Ly;
          $site_j_til = $j_til_y*$Lx+$j_til_x;
          #
          $all_i     = $site_i;
          $all_i_til = $site_i_til;
          $all_j     = $site_j;
          $all_j_til = $site_j_til;
               
          $inp[0]=$all_i;
          $inp[1]=$all_j;
          $inp[2]=0;
          $inp[3]=$all_i_til;
          $inp[4]=$all_j_til;
          $inp[5]=1;
          printf FILE "  $inp[0] $inp[2] $inp[1] $inp[2] $inp[3]  $inp[5] $inp[4] $inp[5]\n";
          printf FILE "  $inp[1] $inp[2] $inp[0] $inp[2] $inp[4]  $inp[5] $inp[3] $inp[5]\n";

          $inp[0]=$all_i;
          $inp[1]=$all_j_til;
          $inp[2]=0;
          $inp[3]=$all_i_til;
          $inp[4]=$all_j;
          $inp[5]=1;
          printf FILE "  $inp[0] $inp[2] $inp[1] $inp[2] $inp[3]  $inp[5] $inp[4] $inp[5]\n";
          printf FILE "  $inp[1] $inp[2] $inp[0] $inp[2] $inp[4]  $inp[5] $inp[3] $inp[5]\n";

          $inp[0]=$all_i_til;
          $inp[1]=$all_j;
          $inp[2]=0;
          $inp[3]=$all_i;
          $inp[4]=$all_j_til;
          $inp[5]=1;
          printf FILE "  $inp[0] $inp[2] $inp[1] $inp[2] $inp[3]  $inp[5] $inp[4] $inp[5]\n";
          printf FILE "  $inp[1] $inp[2] $inp[0] $inp[2] $inp[4]  $inp[5] $inp[3] $inp[5]\n";

          $inp[0]=$all_i_til;
          $inp[1]=$all_j_til;
          $inp[2]=0;
          $inp[3]=$all_i;
          $inp[4]=$all_j;
          $inp[5]=1;
          printf FILE "  $inp[0] $inp[2] $inp[1] $inp[2] $inp[3]  $inp[5] $inp[4] $inp[5]\n";
          printf FILE "  $inp[1] $inp[2] $inp[0] $inp[2] $inp[4]  $inp[5] $inp[3] $inp[5]\n";
          #$cnt+=8;
        }
      }
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
 
