#!/usr/bin/perl -w 
  print "start !! \n";
  #input!!
  &input;
  #input!!
  #$PI=3.14159265358979;
  $Sample=5;
  $orb_num=$tmp_orb;
  $Lx=$tmp_Lx;
  $Ly=$tmp_Ly;
  $L=$Lx*$Ly;
  $Ns=$L;
  $All_N=$Ns*$orb_num;

  for($sum_i=1;$sum_i<=$Sample;$sum_i++){ #[s]$sum_i=1;$sum_i<=$Sample;$sum_i++
 #===============def input====================
    $cnt=0;
    $file=sprintf("aft/zvo_cisajs_00$sum_i.dat");
    print "$file $sum_i \n";
    open(INPUTFILE,$file);
    while($name=<INPUTFILE>){
      chomp $name;
      #DELETE EMPTY
      $_=$name; 
      s/^\s+//;
      $name=$_; 
      #DELETE EMPTY FINISH
      @foo = split /\s+/, $name;
      #printf "$cnt $foo[0] $foo[1] $foo[2] $foo[3] $foo[4] $foo[5] $foo[6] $foo[7] \n";
      if(defined($foo[0])){
        $all_i = $foo[0];
        $spn_i = $foo[1];
        $all_j = $foo[2];
        $spn_j = $foo[3];
        $OneG[$sum_i][$all_i][$spn_i][$all_j][$spn_j] = $foo[4];
      }
      $cnt+=1;
    }
    close(INPUTFILE);
#===============def input====================
    $cnt=0;
    $file=sprintf("aft/zvo_cisajscktalt_00$sum_i.dat");
    print "$file $sum_i \n";
    open(INPUTFILE,$file);
    while($name=<INPUTFILE>){
      chomp $name;
      #DELETE EMPTY
      $_=$name; 
      s/^\s+//;
      $name=$_; 
      #DELETE EMPTY FINISH
      @foo = split /\s+/, $name;
      if(defined($foo[0])){
        #printf "$cnt $foo[0] $foo[2] \n";
        $all_i = $foo[0];
        $spn_i = $foo[1];
        $all_j = $foo[2];
        $spn_j = $foo[3];
        $all_k = $foo[4];
        $spn_k = $foo[5];
        $all_l = $foo[6];
        $spn_l = $foo[7];
        $TwoG[$sum_i][$all_i][$spn_i][$all_j][$spn_j][$all_k][$spn_k][$all_l][$spn_l] = $foo[8];
      }
      $cnt+=1;
    }
    close(INPUTFILE);
  } #[e]$sum_i=1;$sum_i<=$Sample;$sum_i++


  for($orb=0;$orb<$orb_num;$orb++){
    $doublon_A = 0.0;
    $doublon_D = 0.0;
    for($sum_i=1;$sum_i<=$Sample;$sum_i++){
      $tmp = 0.0;
      for($all_i=0;$all_i<$All_N;$all_i+=1){
        $site_i = $all_i%$Ns;
        $orb_i  = ($all_i-$site_i)/$Ns;
        if($orb_i==$orb){
          $tmp +=$TwoG[$sum_i][$all_i][0][$all_i][0][$all_i][1][$all_i][1];
        }
      }
      $tmp = $tmp/$Ns;
      $doublon_A += $tmp;
      $doublon_D += $tmp**2;
    }   
    $doublon_A  = $doublon_A/$Sample;
    $doublon_D  = sqrt($doublon_D/(1.0*($Sample-1.0))-$Sample/($Sample-1.0)*$doublon_A**2)/(sqrt(1.0*$Sample));
    print("$doublon_A $doublon_D \n");

    $fname="Result_D_orb$orb.dat";
    open(FILE,">$fname");
    printf FILE ("$doublon_A $doublon_D\n");
    close(FILE);
  }

  $fname="All_SiSj.dat";
  open(FILE,">$fname");
  for($all_i=0;$all_i<$All_N;$all_i+=1){
    for($all_j=0;$all_j<$All_N;$all_j+=1){
      $S_A       = 0.0;
      $S_D       = 0.0;
      $Sxy_A     = 0.0;
      $Sxy_D     = 0.0;
      $Sz_A      = 0.0;
      $Sz_D      = 0.0;
      for($sum_i=1;$sum_i<=$Sample;$sum_i++){
        $tmp   =  0.0;
        $tmp   +=  $TwoG[$sum_i][$all_i][0][$all_i][0][$all_j][0][$all_j][0];
        $tmp   +=  -$TwoG[$sum_i][$all_i][1][$all_i][1][$all_j][0][$all_j][0];
        $tmp   +=  -$TwoG[$sum_i][$all_i][0][$all_i][0][$all_j][1][$all_j][1];
        $tmp   +=  $TwoG[$sum_i][$all_i][1][$all_i][1][$all_j][1][$all_j][1];
        $tmp    =  0.25*$tmp;
        $tmp_A  =  $tmp;
        $tmp_Sz =  $tmp;
        $Sz_A  +=  $tmp;
        $Sz_D  +=  $tmp**2;

        $tmp    =  0.0;
        $tmp   +=  $TwoG[$sum_i][$all_i][0][$all_j][0][$all_j][1][$all_i][1];
        $tmp   +=  $TwoG[$sum_i][$all_i][1][$all_j][1][$all_j][0][$all_i][0];
        $tmp    = -0.5*$tmp;
        if($all_i== $all_j){# fock term
          $tmp  += 0.5*($OneG[$sum_i][$all_i][0][$all_i][0]+$OneG[$sum_i][$all_i][1][$all_i][1]);
        }
        $Sxy_A +=  $tmp;
        $Sxy_D +=  $tmp**2;

        $tmp_Sxy =  $tmp;

        $tmp_A +=  $tmp;
        $S_A   +=  $tmp_A;
        $S_D   +=  $tmp_A**2;
#
        $XS[$sum_i][$all_i][$all_j]        = $tmp_Sz+$tmp_Sxy;
        $XSxy[$sum_i][$all_i][$all_j]      = $tmp_Sxy;
        $XSz[$sum_i][$all_i][$all_j]       = $tmp_Sz;
      }
      $S_A    = $S_A/(1.0*$Sample);
      $S_E    = sqrt($S_D/(1.0*($Sample-1.0))-$Sample/($Sample-1.0)*$S_A**2)/(sqrt(1.0*$Sample));
      $Sxy_A  = $Sxy_A/(1.0*$Sample);
      $Sxy_E  = sqrt($Sxy_D/(1.0*($Sample-1.0))-$Sample/($Sample-1.0)*$Sxy_A**2)/(sqrt(1.0*$Sample));
      $Sz_A   = $Sz_A/(1.0*$Sample);
      #$Sz_E   = sqrt($Sz_D/(1.0*($Sample-1.0))-$Sample/($Sample-1.0)*$Sz_A**2)/(sqrt(1.0*$Sample));

      #printf("$all_i $all_j $S_A $S_E $Sxy_A $Sxy_E $Sz_A $Sz_D\n");
      printf FILE ("$all_i $all_j $S_A $S_E $Sxy_A $Sxy_E $Sz_A $Sz_D\n");

      #$S[$all_i][$all_j]       = $S_A;
      #$S_err[$all_i][$all_j]   = $S_E;
      #$Sxy[$all_i][$all_j]     = $Sxy_A;
      #$Sxy_err[$all_i][$all_j] = $Sxy_E;
      #$Sz[$all_i][$all_j]      = $Sz_A;
      #$Sz_err[$all_i][$all_j]  = $Sz_E;
    }
  }
  close(FILE);

  for($orb=0;$orb<$orb_num;$orb++){#[s]($orb=0;$orb<$orb_num;$orb++
  #[s] Snn  
    $nn_x[0] =  1;  $nn_y[0] =  0;
    $nn_x[1] = -1;  $nn_y[1] =  0;
  #
    $S_Ave   = 0;
    $S_Err   = 0;
    $Sz_Ave  = 0;
    $Sz_Err  = 0;
    $Sxy_Ave = 0;
    $Sxy_Err = 0;
    $norm    = 2.0*$Ns;
    for($sum_i=1;$sum_i<=$Sample;$sum_i++){
      $tmp    = 0.0;
      $tmp_z  = 0.0;
      $tmp_xy = 0.0;
      for($all_i=0;$all_i<$All_N;$all_i+=1){
        $site_i = $all_i%$Ns;
        $orb_i  = ($all_i-$site_i)/$Ns;
        $x_i    = $site_i%$Lx;
        $y_i    = ($site_i-$x_i)/$Lx;
        if($orb_i==$orb){
           for($nn_i=0;$nn_i<2;$nn_i++){
            $x_j     = ($x_i+$nn_x[$nn_i]+$Lx)%$Lx;
            $y_j     = ($y_i+$nn_y[$nn_i]+$Ly)%$Ly;
            $site_j  = $x_j+$y_j*$Lx;
            $all_j   = $site_j+$Ns*$orb_i;
            #print("$all_i $all_j $sum_i $XS[$sum_i][$all_i][$all_j] \n");
            $tmp    += $XS[$sum_i][$all_i][$all_j]; 
            $tmp_z  += $XSz[$sum_i][$all_i][$all_j]; 
            $tmp_xy += $XSxy[$sum_i][$all_i][$all_j]; 
          }
        }
      } 
      $S_Ave   += ($tmp/$norm);
      $S_Err   += ($tmp/$norm)**2;
      $Sz_Ave  += ($tmp_z/$norm);
      $Sz_Err  += ($tmp_z/$norm)**2;
      $Sxy_Ave += ($tmp_xy/$norm);
      $Sxy_Err += ($tmp_xy/$norm)**2;
    } 
    $S_Ave     = $S_Ave/$Sample;
    $S_Err     = sqrt($S_Err/(1.0*($Sample-1.0))-$Sample/($Sample-1.0)*$S_Ave**2)/(sqrt(1.0*$Sample));
    $Sz_Ave    = $Sz_Ave/$Sample;
    $Sz_Err    = sqrt($Sz_Err/(1.0*($Sample-1.0))-$Sample/($Sample-1.0)*$Sz_Ave**2)/(sqrt(1.0*$Sample));
    $Sxy_Ave   = $Sxy_Ave/$Sample;
    $Sxy_Err   = sqrt($Sxy_Err/(1.0*($Sample-1.0))-$Sample/($Sample-1.0)*$Sxy_Ave**2)/(sqrt(1.0*$Sample));
    print("$S_Ave $S_Err $Sz_Ave $Sz_Err $Sxy_Ave $Sxy_Err \n");
  
    
    $fname="Result_Snn_orb$orb.dat";
    open(FILE,">$fname");
    print FILE ("$S_Ave $S_Err $Sz_Ave $Sz_Err $Sxy_Ave $Sxy_Err \n");
    close(FILE);
  }#[e]($orb=0;$orb<$orb_num;$orb++

  for($orb=0;$orb<1;$orb++){#[s]($orb=0;$orb<1;$orb++
  #[s] Snn  
    $nn_x[0] =  0;  $nn_y[0] =  0;
  #
    $S_Ave   = 0;
    $S_Err   = 0;
    $Sz_Ave  = 0;
    $Sz_Err  = 0;
    $Sxy_Ave = 0;
    $Sxy_Err = 0;
    $norm    = 1.0*$Ns;
    for($sum_i=1;$sum_i<=$Sample;$sum_i++){
      $tmp    = 0.0;
      $tmp_z  = 0.0;
      $tmp_xy = 0.0;
      for($all_i=0;$all_i<$All_N;$all_i+=1){
        $site_i = $all_i%$Ns;
        $orb_i  = ($all_i-$site_i)/$Ns;
        $x_i    = $site_i%$Lx;
        $y_i    = ($site_i-$x_i)/$Lx;
        if($orb_i==$orb){
           for($nn_i=0;$nn_i<1;$nn_i++){
            $x_j     = ($x_i+$nn_x[$nn_i]+$Lx)%$Lx;
            $y_j     = ($y_i+$nn_y[$nn_i]+$Ly)%$Ly;
            $site_j  = $x_j+$y_j*$Lx;
            $orb_j    = 1 ;
            $all_j   = $site_j+$Ns*$orb_j;
            #print("$all_i $all_j $sum_i $XS[$sum_i][$all_i][$all_j] \n");
            $tmp    += $XS[$sum_i][$all_i][$all_j]; 
            $tmp_z  += $XSz[$sum_i][$all_i][$all_j]; 
            $tmp_xy += $XSxy[$sum_i][$all_i][$all_j]; 
          }
        }
      } 
      $S_Ave   += ($tmp/$norm);
      $S_Err   += ($tmp/$norm)**2;
      $Sz_Ave  += ($tmp_z/$norm);
      $Sz_Err  += ($tmp_z/$norm)**2;
      $Sxy_Ave += ($tmp_xy/$norm);
      $Sxy_Err += ($tmp_xy/$norm)**2;
    } 
    $S_Ave     = $S_Ave/$Sample;
    $S_Err     = sqrt($S_Err/(1.0*($Sample-1.0))-$Sample/($Sample-1.0)*$S_Ave**2)/(sqrt(1.0*$Sample));
    $Sz_Ave    = $Sz_Ave/$Sample;
    $Sz_Err    = sqrt($Sz_Err/(1.0*($Sample-1.0))-$Sample/($Sample-1.0)*$Sz_Ave**2)/(sqrt(1.0*$Sample));
    $Sxy_Ave   = $Sxy_Ave/$Sample;
    $Sxy_Err   = sqrt($Sxy_Err/(1.0*($Sample-1.0))-$Sample/($Sample-1.0)*$Sxy_Ave**2)/(sqrt(1.0*$Sample));
    print("$S_Ave $S_Err $Sz_Ave $Sz_Err $Sxy_Ave $Sxy_Err \n");
  
    
    $fname="Result_LocalS.dat";
    open(FILE,">$fname");
    print FILE ("$S_Ave $S_Err $Sz_Ave $Sz_Err $Sxy_Ave $Sxy_Err \n");
    close(FILE);
  }#[e]($orb=0;$orb<$orb_num;$orb++





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
  close(INPUTFILE);
  $file=sprintf("modpara.def");
  open(INPUTFILE,$file);
  while($name=<INPUTFILE>){
    chomp $name;
    #DELETE EMPTY
    $_=$name; 
    s/^\s+//;
    $name=$_; 
    @tmp = split /\s+/, $name;
    #printf "$tmp[0] $tmp[1] \n";
    if($tmp[0] eq 'Ncond'){
      #printf "AA $tmp[0] $tmp[1] \n";
      #$Nelectron = $tmp[1];
    } 
  }
  close(INPUTFILE);

  #input FINISH
 }







