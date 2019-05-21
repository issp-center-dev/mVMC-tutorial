#!/usr/bin/perl -w 
  #$PI=3.14159265358979;
  #input!!
  &input;
  #input!!
  $Sample=5;
  $orb_num=$tmp_orb;
  $Lx=$tmp_Lx;
  $Ly=$tmp_Ly;
  $L=$Lx*$Ly;
  $Ns=$L;
  $All_N=$Ns*$orb_num;
  printf("CHECK ED_Sq.prl $All_N Lx=$Lx Ly=$Ly orb_num=$orb_num \n");

  for($sum_i=1;$sum_i<=$Sample;$sum_i++){
#===============def input====================
    $cnt=0;
    #$file=sprintf("F_Cor.dat");
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
      #printf "$cnt $foo[0] $foo[1] $foo[2] $foo[3] $foo[4] $foo[5] $foo[6]  \n";
      #for($i=0;$i<4;$i++){
      if(defined($foo[0])){
        if($foo[1]==$foo[3] && defined($foo[0])){
          $all_i = $foo[0];  
          $all_j = $foo[2];  
          $spin  = $foo[1];  
          $Green[$all_i][$all_j][$spin]=$foo[4];
        }
      }
      $cnt+=1;
    }
    close(INPUTFILE);
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
      #printf "$cnt $foo[0] $foo[1] $foo[2] $foo[3] $foo[4] $foo[5] $foo[6]  \n";
      if(defined($foo[0])){
        $tmp_0 = $foo[0]; # i 
        $tmp_1 = $foo[2]; # j
        $tmp_2 = $foo[1]; # s
        $tmp_3 = $foo[4]; # k
        $tmp_4 = $foo[6]; # l
        $tmp_5 = $foo[5]; # t
        $Cor[$tmp_0][$tmp_1][$tmp_2][$tmp_3][$tmp_4][$tmp_5] = $foo[8];
      } 
    }
    close(INPUTFILE);

    #dwave s2 or d_x2-y2
    $sn[0]=1.0;
    $sn[1]=1.0;
    $sn[2]=-1.0;
    $sn[3]=-1.0;


    $near_x[0]=1;
    $near_y[0]=0;

    $near_x[1]=-1;
    $near_y[1]=0;

    $near_x[2]=0;
    $near_y[2]=1;

    $near_x[3]=0;
    $near_y[3]=-1;
    $cnt=0;


    $orb_i = 0;
    $fname="Aft_SC_$sum_i.dat";
    open($FILE[$orb_i],">$fname");
    
    for($site_i=0;$site_i<$Ns;$site_i+=1){
      $i_x=$site_i%$Lx;
      $i_y=($site_i-$i_x)/$Lx;
      for($site_j=0;$site_j<$Ns;$site_j+=1){
        $j_x=$site_j%$Lx;
        $j_y=($site_j-$j_x)/$Lx;
        #
        $D_2d_1[$sum_i][$site_i][$site_j]=0.0;
        $D_2d_2[$sum_i][$site_i][$site_j]=0.0;
        $D_2s_1[$sum_i][$site_i][$site_j]=0.0;
        $D_2s_2[$sum_i][$site_i][$site_j]=0.0;
        #
        for($i_n=0;$i_n<4;$i_n++){
          $i_til_x    = ($i_x+$near_x[$i_n]+$Lx)%$Lx;
          $i_til_y    = ($i_y+$near_y[$i_n]+$Ly)%$Ly;
          $site_i_til = $i_til_y*$Lx+$i_til_x;
 
          for($j_n=0;$j_n<4;$j_n++){
            $j_til_x=($j_x+$near_x[$j_n]+$Lx)%$Lx;
            $j_til_y=($j_y+$near_y[$j_n]+$Ly)%$Ly;
            $site_j_til = $j_til_y*$Lx+$j_til_x;

            $sign=$sn[$i_n]*$sn[$j_n];
            # 
            $all_i     = $site_i;
            $all_i_til = $site_i_til;
            $all_j     = $site_j;
            $all_j_til = $site_j_til;
            #
            #1
            $tmp_0 = $all_i;
            $tmp_1 = $all_j;
            $tmp_2 = 0;
            $tmp_3 = $all_i_til;
            $tmp_4 = $all_j_til;
            $tmp_5 = 1;
            &mlt;
            #
            $tmp_0 = $all_i;
            $tmp_1 = $all_j_til;
            $tmp_2 = 0;
            $tmp_3 = $all_i_til;
            $tmp_4 = $all_j;
            $tmp_5 = 1;
            &mlt;
            #
            $tmp_0 = $all_i_til;
            $tmp_1 = $all_j;
            $tmp_2 = 0;
            $tmp_3 = $all_i;
            $tmp_4 = $all_j_til;
            $tmp_5 = 1;
            &mlt;
            #
            $tmp_0 = $all_i_til;
            $tmp_1 = $all_j_til;
            $tmp_2 = 0;
            $tmp_3 = $all_i;
            $tmp_4 = $all_j;
            $tmp_5 = 1;
            &mlt;
          }
        }
        $sc_2s[$sum_i][$site_i][$site_j] = $D_2s_1[$sum_i][$site_i][$site_j]+$D_2s_2[$sum_i][$site_i][$site_j];
        $sc_2d[$sum_i][$site_i][$site_j] = $D_2d_1[$sum_i][$site_i][$site_j]+$D_2d_2[$sum_i][$site_i][$site_j];
  
        $diff_x = abs($i_x-$j_x);
        if($diff_x > $Lx/2){
          $diff_x = $diff_x-$Lx;
        }
        $diff_y = abs($i_y-$j_y);
        if($diff_y > $Ly/2){
          $diff_y = $diff_y-$Ly;
        }
        $dis = $diff_x**2+$diff_y**2;
        printf {$FILE[$orb_i]} " $site_i $site_j $dis $sc_2s[$sum_i][$site_i][$site_j]  $sc_2s[$sum_i][$site_i][$site_j]  \n";
      }
    }
    close($FILE[$orb_i]);
  }

  for($orb_i=0;$orb_i<$orb_num;$orb_i++){
    for($vec_i=0;$vec_i<$Ns;$vec_i+=1){
      $vec_x=$vec_i%$Lx;
      $vec_y=($vec_i-$vec_x)/$Lx;
  
      $sum_2s  = 0.0;
      $err_2s  = 0.0;
      $sum_2d  = 0.0;
      $err_2d  = 0.0;
      for($sum_i=1;$sum_i<=$Sample;$sum_i+=1){
        $tmp_2s    = 0.0;
        $tmp_2d    = 0.0;
        for($ini_i=0;$ini_i<$Ns;$ini_i+=1){
          $ini_x    = $ini_i%$Lx;
          $ini_y    = ($ini_i-$ini_x)/$Lx;
  
          $tmp_x    = ($vec_x+$ini_x)%$Lx;
          $tmp_y    = ($vec_y+$ini_y)%$Ly;
          $tmp_i    = $tmp_y*$Lx+$tmp_x;
  
          $tmp_2s   += $sc_2s[$sum_i][$ini_i][$tmp_i];
          $tmp_2d   += $sc_2d[$sum_i][$ini_i][$tmp_i];
  
        }
        $sum_2s   +=  $tmp_2s/($Ns*4.0);
        $sum_2d   +=  $tmp_2d/($Ns*4.0);
        $err_2s   +=  ($tmp_2s/($Ns*4.0))**2;
        $err_2d   +=  ($tmp_2d/($Ns*4.0))**2;
      }
      $sum_2s                       =  $sum_2s/$Sample;
      $sum_2d                       =  $sum_2d/$Sample;
      $all_sum_2s[$orb_i][$vec_i]   =  $sum_2s;
      $all_sum_2d[$orb_i][$vec_i]   =  $sum_2d;
  
      $all_err_2s[$orb_i][$vec_i]   = sqrt($err_2s/(1.0*($Sample-1.0))-$Sample/($Sample-1.0)*$sum_2s**2)/sqrt($Sample);
      $all_err_2d[$orb_i][$vec_i]   = sqrt($err_2d/(1.0*($Sample-1.0))-$Sample/($Sample-1.0)*$sum_2d**2)/sqrt($Sample);
    }
  }

  for($orb_i=0;$orb_i<$orb_num;$orb_i++){
    $fname="Ave_SC_Sum_1s_$orb_i.dat";
    open($FILE_1s[$orb_i],">$fname");

    for($vec_i=0;$vec_i<$Ns;$vec_i+=1){
      $vec_x=$vec_i%$Lx;
      $vec_y=($vec_i-$vec_x)/$Lx;

      $diff_x = ($vec_x);
      if($diff_x > $Lx/2){
        $diff_x = $diff_x-$Lx;
      }

      $diff_y = ($vec_y);
      if($diff_y > $Ly/2){
        $diff_y = $diff_y-$Ly;
      }
      $dis = $diff_x**2+$diff_y**2;
      printf {$FILE_1s[$orb_i]} ("%5d  %5d  %10f  %10f  %10f  %10f  \n",$vec_i,$dis,$all_sum_2s[$orb_i][$vec_i],$all_err_2s[$orb_i][$vec_i],$all_err_2d[$orb_i][$vec_i],$all_err_2d[$orb_i][$vec_i]);
    }
    close($FILE_1s[$orb_i]);

    $fname="Ave_Max_SC_Sum_2s_$orb_i.dat";
    open($FILE_2s[$orb_i],">$fname");
    $fname="Ave_Max_SC_Sum_2d_$orb_i.dat";
    open($FILE_2d[$orb_i],">$fname");

    printf {$FILE_2s[$orb_i]} ("# distance    P_2s    err \n");
    printf {$FILE_2d[$orb_i]} ("# distance    P_2d    err \n");

    for($tmp_dis=0;$tmp_dis<$Ns**2;$tmp_dis+=1){
      $cnt_dis = 0;
      for($vec_i=0;$vec_i<$Ns;$vec_i+=1){
        $vec_x=$vec_i%$Lx;
        $vec_y=($vec_i-$vec_x)/$Lx;

        $diff_x = ($vec_x);
        if($diff_x > $Lx/2){
          $diff_x = $diff_x-$Lx;
        }
        $diff_y = ($vec_y);
        if($diff_y > $Ly/2){
          $diff_y = $diff_y-$Ly;
        }
        $dis = $diff_x**2+$diff_y**2;
        if($dis==$tmp_dis){
          if($cnt_dis==0){
            $Max_sum_2s = abs($all_sum_2s[$orb_i][$vec_i]);
            $Max_err_2s = $all_err_2s[$orb_i][$vec_i];
            $Max_sum_2d = abs($all_sum_2d[$orb_i][$vec_i]);
            $Max_err_2d = $all_err_2d[$orb_i][$vec_i];

            $cnt_dis=1;  
          }else{
            if(abs($all_sum_2s[$orb_i][$vec_i]) > abs($Max_sum_2s)){
              $Max_sum_2s = abs($all_sum_2s[$orb_i][$vec_i]);
              $Max_err_2s = $all_err_2s[$orb_i][$vec_i];
            } 
            if(abs($all_sum_2d[$orb_i][$vec_i]) > abs($Max_sum_2d)){
              $Max_sum_2d = abs($all_sum_2d[$orb_i][$vec_i]);
              $Max_err_2d = $all_err_2d[$orb_i][$vec_i];
            } 
          } 
        } 
      }
      if($cnt_dis!=0){
        #printf("$tmp_dis \n");
        printf {$FILE_2s[$orb_i]} ("%10f %10f  %10f \n",sqrt($tmp_dis),$Max_sum_2s,$Max_err_2s);
        printf {$FILE_2d[$orb_i]} ("%10f %10f  %10f \n",sqrt($tmp_dis),$Max_sum_2d,$Max_err_2d);
      }
    }
    close($FILE_2s[$orb_i]);
    close($FILE_2d[$orb_i]);
  } 
 sub input{
  #input START 
  $Lx_cnt=0;
  $Ly_cnt=0;
 # $orb_cnt=0;
 # $lambda_cnt=0;
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
      $tmp_orb = $tmp[1];
    } 
  }
  if($Lx_cnt==0 || $Ly_cnt==0){
    printf "FAITAL ERROR IN input.txt !!!!!!!!!!!!! \n";
  }
  #input FINISH
 }
 sub mlt{
   $tmp_Cor_1 = $Cor[$tmp_0][$tmp_1][$tmp_2][$tmp_3][$tmp_4][$tmp_5];
   $tmp_Cor_2 = $Cor[$tmp_1][$tmp_0][$tmp_2][$tmp_4][$tmp_3][$tmp_5];
   $kr_1      = 0.0;
   $kr_2      = 0.0; 
   if($tmp_0==$tmp_1){
     $kr_1 = 1.0;
   }
   if($tmp_3==$tmp_4){
     $kr_2 = 1.0;
   }
   $tmp = $kr_1*$kr_2-$kr_1*$Green[$tmp_3][$tmp_4][1]-$kr_2*$Green[$tmp_0][$tmp_1][0]+$tmp_Cor_2;
   $D_2d_1[$sum_i][$site_i][$site_j] += $sign*$tmp_Cor_1;
   $D_2d_2[$sum_i][$site_i][$site_j] += $sign*$tmp;
   $D_2s_1[$sum_i][$site_i][$site_j] += $tmp_Cor_1;
   $D_2s_2[$sum_i][$site_i][$site_j] += $tmp;
 }
