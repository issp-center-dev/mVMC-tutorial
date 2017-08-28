#!/usr/bin/perl -w 
  print "start !! \n";
  #input!!
  &input;
  #input!!
  $PI=3.14159265358979;
  $all_i=5;
  $L_y = 1;
  $orb_num=$tmp_orb;
  $L_x=$tmp_Lx;
  $L=$L_x*$L_y;
  $Ns=$L;
  $All_N=$Ns*$orb_num;

  $sublattice = $Ns;
  $unitcell   = $sublattice*$orb_num ; 

  $norm = $Ns/$sublattice;

  printf("CHECK Energy L_x=$L_x L_y=$L_y orb=$orb_num norm=$norm\n");

  for($kx=0;$kx<=$L_x;$kx+=1){
    for($ky=0;$ky<$L_y;$ky+=1){
      $All_Sq[$kx][$ky]=0.0;
      $All_Sq_err[$kx][$ky]=0.0;
      $All_Nq[$kx][$ky]=0.0;
      $All_Nq_err[$kx][$ky]=0.0;
      for($orb_i=0;$orb_i<$orb_num;$orb_i++){
        $All_Sq_dec[$kx][$ky][$orb_i]=0.0;
        $All_Sq_dec_err[$kx][$ky][$orb_i]=0.0;
        $All_Nq_dec[$kx][$ky][$orb_i]=0.0;
        $All_Nq_dec_err[$kx][$ky][$orb_i]=0.0;
      } 
    }
  }

  for($sum_i=1;$sum_i<=$all_i;$sum_i++){
  
 #===============def input====================
    for($orb_i=0;$orb_i<$orb_num;$orb_i++){
      $num[$orb_i] = 0.0;
    }
    $cnt=0;
    $file=sprintf("aft/zvo_cisajs_00%d.dat",$sum_i);
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
        if($foo[0]==$foo[2] && defined($foo[0])){
#[s] orbital indices for Standard mode
          $orb_i        = $foo[0]/$Ns;
          $num[$orb_i] += $foo[4];
#[e] orbital indices for Standard mode
        }
      }
      $cnt+=1;
    }
    close(INPUTFILE);
    for($orb_i=0;$orb_i<$orb_num;$orb_i++){
      $tmp = $num[$orb_i]/$L;
      printf "orb = $orb_i num = $num[$orb_i] \n";
    }
#===============def input====================
    $cnt=0;
    $file=sprintf("aft/zvo_cisajscktalt_00%d.dat",$sum_i);
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
        for($i=0;$i<10;$i++){
          $phys[$cnt][$i]=$foo[$i];
        }
      }
      $cnt+=1;
    }
    close(INPUTFILE);
   if($sum_i==1){
#==== make cos ====
   for($kx=0;$kx<=$L_x;$kx+=1){
     for($ky=0;$ky<$L_y;$ky+=1){
        for($cnt=0;$cnt<$All_N*$unitcell*4;$cnt+=1){
#========================
#[s] orbital & site indices for Standard mode
          $site_1 = $phys[$cnt][0]%$Ns;
          $orb_1  = ($phys[$cnt][0]-$site_1)/$Ns;
          $site_2 = $phys[$cnt][4]%$Ns;
          $orb_2  = ($phys[$cnt][4]-$site_2)/$Ns;
#[e] orbital & site indices for Standard mode
          $x_1=$site_1%$L_x;
          $y_1=($site_1-$x_1)/$L_x;
          $x_2=$site_2%$L_x;
          $y_2=($site_2-$x_2)/$L_x;
          $dif_x=$x_1-$x_2;
          $dif_y=$y_1-$y_2;

          if($cnt%4==0 || $cnt%4==3){
            $sgn=1.0;
          }else{
            $sgn=-1.0;
          }
          $t_cos[$kx][$ky][$cnt] = $sgn*0.25*cos(2*$PI*$kx*$dif_x/$L_x+2*$PI*$ky*$dif_y/$L_y);
          $u_cos[$kx][$ky][$cnt] = cos(2*$PI*$kx*$dif_x/$L_x+2*$PI*$ky*$dif_y/$L_y);
          if($orb_1==$orb_2){
            $orb_dec[$cnt] = $orb_1;
            $tmp_dec[$cnt] = 1.0;
          }else{
            $orb_dec[$cnt] = $orb_num;
            $tmp_dec[$cnt] = 0.0;
          } 
        }
        for($cnt=$All_N*$unitcell*4;$cnt<$All_N*$unitcell*6;$cnt+=1){
#[s] orbital & site indices for Standard mode
          $site_1 = $phys[$cnt][0]%$Ns;
          $orb_1  = ($phys[$cnt][0]-$site_1)/$Ns;
          $site_2 = $phys[$cnt][4]%$Ns;
          $orb_2  = ($phys[$cnt][4]-$site_2)/$Ns;
#[e] orbital & site indices for Standard mode
          $x_1=$site_1%$L_x;
          $y_1=($site_1-$x_1)/$L_x;
          $x_2=$site_2%$L_x;
          $y_2=($site_2-$x_2)/$L_x;
          $dif_x=$x_1-$x_2;
          $dif_y=$y_1-$y_2;

          if($orb_1==$orb_2){
            $orb_dec[$cnt] = $orb_1;
            $tmp_dec[$cnt] = 1.0;
          }else{
            $orb_dec[$cnt] = $orb_num;
            $tmp_dec[$cnt] = 0.0;
          } 

          $t_cos[$kx][$ky][$cnt] =  -0.5*cos(2*$PI*$kx*$dif_x/$L_x+2*$PI*$ky*$dif_y/$L_y);
        }
      }
    }   
    printf "make cos finishes !\n ";
    }
#================Sq=================
    $fname=sprintf("R_Sq_00%d_2.dat",$sum_i);
    open(FILE,">$fname");
    for($kx=0;$kx<=$L_x;$kx+=1){
      for($ky=0;$ky<$L_y;$ky+=1){
        for($orb_i=0;$orb_i<$orb_num;$orb_i++){
          $Sq_dec[$orb_i]=0.0;
          $Nq_dec[$orb_i]=0.0;
        }
        $Sq=0.0;
        $Nq=0.0;
        $Sq_z=0.0;
        $Sq_xy=0.0;
        $D=0.0;
#======= Sz =====================      
        for($cnt=0;$cnt<$All_N*$unitcell*4;$cnt+=1){
          $tmp_orb = $orb_dec[$cnt];  
          $Sq_dec[$tmp_orb]+=$t_cos[$kx][$ky][$cnt]*$phys[$cnt][8]*$tmp_dec[$cnt];
          $Nq_dec[$tmp_orb]+=$u_cos[$kx][$ky][$cnt]*$phys[$cnt][8]*$tmp_dec[$cnt];
          $Sq+=$t_cos[$kx][$ky][$cnt]*$phys[$cnt][8];
          $Nq+=$u_cos[$kx][$ky][$cnt]*$phys[$cnt][8];
          $Sq_z+=$t_cos[$kx][$ky][$cnt]*$phys[$cnt][8];
        }
#======= Sxy =====================      
        for($cnt=$All_N*$unitcell*4;$cnt<$All_N*$unitcell*6;$cnt+=1){
#========================
          $tmp_orb = $orb_dec[$cnt];  
          $Sq_dec[$tmp_orb]+=$t_cos[$kx][$ky][$cnt]*$phys[$cnt][8]*$tmp_dec[$cnt];
          $Sq+=$t_cos[$kx][$ky][$cnt]*$phys[$cnt][8];
          $Sq_xy+=$t_cos[$kx][$ky][$cnt]*$phys[$cnt][8];
        }
        $D=$D/($All_N);
        for($orb_i=0;$orb_i<$orb_num;$orb_i++){
          $Sq_dec[$orb_i]+=0.5*$num[$orb_i]/($norm);
        }
#[s] Sq+
        $Sq    += 0.5*$Ns/$norm;
        $Sq_xy += 0.5*$Ns/$norm;
#[e]
        if($kx%$L_x==0 && $ky%$L_y==0){
          $Nq+=-($Ns)**2/$norm;
          for($orb_i=0;$orb_i<$orb_num;$orb_i++){
            $Nq_dec[$orb_i]+=-($num[$orb_i])**2/($norm);
          }
        }
        #$Sq_z+=0.5*16.0;
        for($orb_i=0;$orb_i<$orb_num;$orb_i++){
          $Sq_dec[$orb_i] = ($Sq_dec[$orb_i]/3.0/($Ns*$Ns/$norm));
          $Nq_dec[$orb_i] = ($Nq_dec[$orb_i]/($Ns*$Ns/$norm));
        }
        #$Sq=sqrt(abs($Sq)/3.0/($Ns*$Ns/$norm)); for ms
        $Sq=(($Sq)/3.0/($Ns*$Ns/$norm));
        $Nq=(($Nq)/($Ns*$Ns/$norm));
        $Sq_z=$Sq_z/(1.0);
        $Sq_xy=$Sq_xy/(1.0);
        $Sq_all=$Sq_z+$Sq_xy;
        printf FILE "$kx $ky $Sq $Sq_z $Sq_xy $Sq_all \n";
        for($orb_i=0;$orb_i<$orb_num;$orb_i++){
          $All_Sq_dec[$kx][$ky][$orb_i]+=$Sq_dec[$orb_i];
          $All_Sq_dec_err[$kx][$ky][$orb_i]+=$Sq_dec[$orb_i]**2;
          $All_Nq_dec[$kx][$ky][$orb_i]+=$Nq_dec[$orb_i];
          $All_Nq_dec_err[$kx][$ky][$orb_i]+=$Nq_dec[$orb_i]**2;
        }
        $All_Sq[$kx][$ky]+=$Sq;
        $All_Sq_err[$kx][$ky]+=$Sq**2;
        $All_Nq[$kx][$ky]+=$Nq;
        $All_Nq_err[$kx][$ky]+=$Nq**2;
      }
      printf FILE "\n";
    }
    close(FILE);
  }
  $fname="Result_Sq.dat";
  open(FILE,">$fname");
  for($kx=0;$kx<=$L_x;$kx+=1){
    for($ky=0;$ky<$L_y;$ky+=1){
      $tmp=$All_Sq[$kx][$ky]/($all_i*1.0);
      $tmp_err=sqrt(abs($All_Sq_err[$kx][$ky]/(1.0*($all_i-1.0))-$all_i/($all_i-1.0)*$tmp**2))/(sqrt(1.0*$all_i));
      printf FILE "$kx $tmp $tmp_err \n";
    }
  }
 close(FILE);

  $fname="Result_Nq.dat";
  open(FILE,">$fname");
  for($kx=0;$kx<=$L_x;$kx+=1){
    for($ky=0;$ky<$L_y;$ky+=1){
      $tmp=$All_Nq[$kx][$ky]/($all_i*1.0);
      $tmp_err=sqrt($All_Nq_err[$kx][$ky]/(1.0*($all_i-1.0))-$all_i/($all_i-1.0)*$tmp**2)/(sqrt(1.0*$all_i));
      printf FILE "$kx $ky $tmp $tmp_err \n";
    }
  }
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
    if($tmp[0] eq 'orb_num'){
      #printf "AA $tmp[0] $tmp[1] \n";
      $tmp_orb = $tmp[1];
      $orb_cnt=1;
    } 
  }
  if($Lx_cnt==0 ||$orb_cnt==0){
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
      $Nelectron = $tmp[1];
    } 
  }
  close(INPUTFILE);

  #input FINISH
 }
