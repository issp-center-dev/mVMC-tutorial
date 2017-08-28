#!/usr/bin/perl -w 
  #$PI=3.14159265358979;
  #input!!
  &input;
  #input!!
  $Sample=5;
  $orb_num=$tmp_orb;
  $L_x=$tmp_Lx;
  $L_y=$tmp_Ly;
  $L=$L_x*$L_y;
  $Ns=$L;
  $All_N=$Ns*$orb_num;
  printf("CHECK ED_Sq.prl $All_N L_x=$L_x L_y=$L_y orb_num=$orb_num \n");

  for($sum_i=1;$sum_i<=$Sample;$sum_i++){
#===============def input====================
    $cnt=0;
    #$file=sprintf("F_Cor.dat");
    $file=sprintf("SC/zvo_cisajs_00%d.dat",$sum_i);
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
    $file=sprintf("SC/zvo_cisajscktalt_00%d.dat",$sum_i);
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

    $orb_i = 0;
    $fname="Aft_SC_$sum_i.dat";
    open($FILE[$orb_i],">$fname");
    
    for($site_i=0;$site_i<$Ns;$site_i+=1){
      $i_x=$site_i%$L_x;
      $i_y=($site_i-$i_x)/$L_x;
      for($site_j=0;$site_j<$Ns;$site_j+=1){
        $j_x=$site_j%$L_x;
        $j_y=($site_j-$j_x)/$L_x;
          
        $D_1s_1[$sum_i][$orb_i][$site_i][$site_j]=0.0;
        $D_1s_2[$sum_i][$orb_i][$site_i][$site_j]=0.0;
        $all_i     = $orb_num*$site_i+$orb_i;
        $all_j     = $orb_num*$site_j+$orb_i;
   #1
        $tmp_0 = $all_i;
        $tmp_1 = $all_j;
        $tmp_2 = 0;
        $tmp_3 = $all_i;
        $tmp_4 = $all_j;
        $tmp_5 = 1;
        &mlt;
        $tmp_1s_1 = $D_1s_1[$sum_i][$orb_i][$site_i][$site_j];
        $tmp_1s_2 = $D_1s_2[$sum_i][$orb_i][$site_i][$site_j];
  
        $diff_x = abs($i_x-$j_x);
        if($diff_x > $L_x/2){
          $diff_x = $diff_x-$L_x;
        }
        $diff_y = abs($i_y-$j_y);
        if($diff_y > $L_y/2){
          $diff_y = $diff_y-$L_y;
        }
        $dis = $diff_x**2+$diff_y**2;
        printf {$FILE[$orb_i]} " $site_i $site_j $dis $tmp_1s_1  $tmp_1s_2  \n";
      }
    }
    close($FILE[$orb_i]);
  }
  for($orb_i=0;$orb_i<$orb_num;$orb_i++){
    $fname="Max_All_SC_Sum_1s_$orb_i.dat";
    open($FILE_max_1s[$orb_i],">$fname");
    $fname="All_SC_Sum_1s_$orb_i.dat";
    open($FILE_1s[$orb_i],">$fname");

    for($site_i=0;$site_i<$Ns;$site_i+=1){
      $i_x=$site_i%$L_x;
      $i_y=($site_i-$i_x)/$L_x;

      printf {$FILE_1s[$orb_i]} ("  \n");
      printf {$FILE_1s[$orb_i]} ("#$site_i  \n");
      printf {$FILE_1s[$orb_i]} ("  \n");

      printf {$FILE_max_1s[$orb_i]} ("  \n");
      printf {$FILE_max_1s[$orb_i]} ("#$site_i  \n");
      printf {$FILE_max_1s[$orb_i]} ("  \n");

      for($tmp_dis=0;$tmp_dis<$Ns**2;$tmp_dis+=1){
        $flag_dis[$tmp_dis] = 0; 
      }
      for($site_j=0;$site_j<$Ns;$site_j+=1){
        $j_x=$site_j%$L_x;
        $j_y=($site_j-$j_x)/$L_x;

        $sum_1s_1  = 0.0;
        $sum_1s_2  = 0.0;
        $sum_1s    = 0.0;
        $err_1s_1  = 0.0;
        $err_1s_2  = 0.0;
        $err_1s    = 0.0;
        for($sum_i=1;$sum_i<=$Sample;$sum_i++){

          $tmp_1s_1    = $D_1s_1[$sum_i][$orb_i][$site_i][$site_j]/(4.0);
          $tmp_1s_2    = $D_1s_2[$sum_i][$orb_i][$site_i][$site_j]/(4.0);

          $sum_1s_1   +=  $tmp_1s_1;
          $sum_1s_2   +=  $tmp_1s_2;
          $sum_1s     +=  $tmp_1s_1+$tmp_1s_2;

          $err_1s_1   +=  $tmp_1s_1**2;
          $err_1s_2   +=  $tmp_1s_2**2;
          $err_1s     +=  ($tmp_1s_1+$tmp_1s_2)**2;
        }  

        $sum_1s_1   =  $sum_1s_1/(1.0*$Sample);
        $sum_1s_2   =  $sum_1s_2/(1.0*$Sample);
        $sum_1s     =  $sum_1s/(1.0*$Sample);

        $err_1s_1   = sqrt($err_1s_1/(1.0*($Sample-1.0))-$Sample/($Sample-1.0)*$sum_1s_1**2);
        $err_1s_2   = sqrt($err_1s_2/(1.0*($Sample-1.0))-$Sample/($Sample-1.0)*$sum_1s_2**2);
        $err_1s     = sqrt($err_1s/(1.0*($Sample-1.0))-$Sample/($Sample-1.0)*$sum_1s**2);

        $diff_x = abs($i_x-$j_x);
        if($diff_x > $L_x/2){
          $diff_x = $diff_x-$L_x;
        }
        $diff_y = abs($i_y-$j_y);
        if($diff_y > $L_y/2){
          $diff_y = $diff_y-$L_y;
        }
        $dis = $diff_x**2+$diff_y**2;
        if($flag_dis[$dis]==0){
          $tmp_Max_sum_1s[$dis] = abs($sum_1s);
          $tmp_Max_err_1s[$dis] = $err_1s;
          $flag_dis[$dis]       = 1;
        }else{
          if(abs($sum_1s) > abs($tmp_Max_sum_1s[$dis]) ){
            $tmp_Max_sum_1s[$dis] = abs($sum_1s);
            $tmp_Max_err_1s[$dis] = $err_1s;
          } 
        }
        printf {$FILE_1s[$orb_i]} ("%5d %5d %5d  %10f  %10f  %10f  %10f  %10f  %10f \n",$site_i,$site_j,$dis,$sum_1s,$err_1s,$sum_1s_1,$err_1s_1,$sum_1s_2,$err_1s_2);
      }
    }  

    for($tmp_dis=0;$tmp_dis<$Ns**2;$tmp_dis+=1){
      if($flag_dis[$tmp_dis]==1){
        printf {$FILE_max_1s[$orb_i]} ("%10f  %10f  %10f  \n",sqrt($tmp_dis),$tmp_Max_sum_1s[$tmp_dis],$tmp_Max_err_1s[$tmp_dis]);
      }
    }
    close($FILE_1s[$orb_i]);
    close($FILE_max_1s[$orb_i]);
  }

  for($orb_i=0;$orb_i<$orb_num;$orb_i++){
    for($vec_i=0;$vec_i<$Ns;$vec_i+=1){
      $vec_x=$vec_i%$L_x;
      $vec_y=($vec_i-$vec_x)/$L_x;
  
      $all_sum_1s_1  = 0.0;
      $all_sum_1s_2  = 0.0;
      $all_sum_1s    = 0.0;
      $all_err_1s_1  = 0.0;
      $all_err_1s_2  = 0.0;
      $all_err_1s    = 0.0;
      for($sum_i=1;$sum_i<=$Sample;$sum_i+=1){
        $sum_1s_1  = 0.0;
        $sum_1s_2  = 0.0;
        $sum_1s    = 0.0;
        $err_1s_1  = 0.0;
        $err_1s_2  = 0.0;
        $err_1s    = 0.0;
        for($ini_i=0;$ini_i<$Ns;$ini_i+=1){
          $ini_x    = $ini_i%$L_x;
          $ini_y    = ($ini_i-$ini_x)/$L_x;
  
          $tmp_x    = ($vec_x+$ini_x)%$L_x;
          $tmp_y    = ($vec_y+$ini_y)%$L_y;
          $tmp_i    = $tmp_y*$L_x+$tmp_x;
  
          #printf ("$sum_i $ini_x $ini_y $tmp_x $tmp_y $tmp_i \n");
  
          $tmp_1s_1    = $D_1s_1[$sum_i][$orb_i][$ini_i][$tmp_i]/(4.0);
          $tmp_1s_2    = $D_1s_2[$sum_i][$orb_i][$ini_i][$tmp_i]/(4.0);
  
          $sum_1s_1   +=  $tmp_1s_1;
          $sum_1s_2   +=  $tmp_1s_2;
          $sum_1s     +=  $tmp_1s_1+$tmp_1s_2;
        }
        $all_sum_1s_1   +=  $sum_1s_1;
        $all_sum_1s_2   +=  $sum_1s_2;
        $all_sum_1s     +=  $sum_1s_1+$sum_1s_2;
  
        $all_err_1s_1   +=  $sum_1s_1**2;
        $all_err_1s_2   +=  $sum_1s_2**2;
        $all_err_1s     +=  ($sum_1s_1+$sum_1s_2)**2;
      }
      $all_sum_1s_1   =  $all_sum_1s_1/$Sample;
      $all_sum_1s_2   =  $all_sum_1s_2/$Sample;
      $all_sum_1s     =  $all_sum_1s/$Sample;
  
      $all_err_1s_1   = sqrt($all_err_1s_1/(1.0*($Sample-1.0))-$Sample/($Sample-1.0)*$all_sum_1s_1**2);
      $all_err_1s_2   = sqrt($all_err_1s_2/(1.0*($Sample-1.0))-$Sample/($Sample-1.0)*$all_sum_1s_2**2);
      $all_err_1s     = sqrt($all_err_1s/(1.0*($Sample-1.0))-$Sample/($Sample-1.0)*$all_sum_1s**2);
  
      $All_sum_1s_1[$orb_i][$vec_i] =  $all_sum_1s_1/$Ns;
      $All_sum_1s_2[$orb_i][$vec_i] =  $all_sum_1s_2/$Ns;;
      $All_sum_1s[$orb_i][$vec_i]   =  $all_sum_1s/$Ns;;
  
      $All_err_1s_1[$orb_i][$vec_i] =  $all_err_1s_1/$Ns;;
      $All_err_1s_2[$orb_i][$vec_i] =  $all_err_1s_2/$Ns;;
      $All_err_1s[$orb_i][$vec_i]   =  $all_err_1s/$Ns;;
    }
  }

  for($orb_i=0;$orb_i<$orb_num;$orb_i++){
    $fname="Ave_SC_Sum_1s_$orb_i.dat";
    open($FILE_1s[$orb_i],">$fname");

    for($vec_i=0;$vec_i<$Ns;$vec_i+=1){
      $vec_x=$vec_i%$L_x;
      $vec_y=($vec_i-$vec_x)/$L_x;

      $diff_x = ($vec_x);
      if($diff_x > $L_x/2){
        $diff_x = $diff_x-$L_x;
      }

      $diff_y = ($vec_y);
      if($diff_y > $L_y/2){
        $diff_y = $diff_y-$L_y;
      }
      $dis = $diff_x**2+$diff_y**2;
      printf {$FILE_1s[$orb_i]} ("%5d  %5d  %10f  %10f  %10f  %10f  %10f  %10f \n",$vec_i,$dis,$All_sum_1s_1[$orb_i][$vec_i],$All_err_1s_1[$orb_i][$vec_i],$All_sum_1s_2[$orb_i][$vec_i],$All_err_1s_2[$orb_i][$vec_i],$All_sum_1s[$orb_i][$vec_i],$All_err_1s[$orb_i][$vec_i]);
    }
    close($FILE_1s[$orb_i]);

    $fname="Ave_Max_SC_Sum_1s_$orb_i.dat";
    open($FILE_1s[$orb_i],">$fname");

    for($tmp_dis=0;$tmp_dis<$Ns**2;$tmp_dis+=1){
      $cnt_dis = 0;
      for($vec_i=0;$vec_i<$Ns;$vec_i+=1){
        $vec_x=$vec_i%$L_x;
        $vec_y=($vec_i-$vec_x)/$L_x;

        $diff_x = ($vec_x);
        if($diff_x > $L_x/2){
          $diff_x = $diff_x-$L_x;
        }
        $diff_y = ($vec_y);
        if($diff_y > $L_y/2){
          $diff_y = $diff_y-$L_y;
        }
        $dis = $diff_x**2+$diff_y**2;
        if($dis==$tmp_dis){
          if($cnt_dis==0){
            $Max_sum_1s = abs($All_sum_1s[$orb_i][$vec_i]);
            $Max_err_1s = $All_err_1s[$orb_i][$vec_i];

            $cnt_dis=1;  
          }else{
            if(abs($All_sum_1s[$orb_i][$vec_i]) > abs($Max_sum_1s)){
              $Max_sum_1s = abs($All_sum_1s[$orb_i][$vec_i]);
              $Max_err_1s = $All_err_1s[$orb_i][$vec_i];
            } 
          } 
        } 
      }
      if($cnt_dis!=0){
        printf("$tmp_dis \n");
        printf {$FILE_1s[$orb_i]} ("%10f %10f  %10f \n",sqrt($tmp_dis),$Max_sum_1s,$Max_err_1s);
      }
    }
    close($FILE_1s[$orb_i]);
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
   #printf(" $tmp_0 $tmp_1 $tmp_2 $tmp_3 $tmp_4 $tmp_5 $tmp_Cor_1 $tmp_Cor_2 \n");

   $kr_1  = 0.0;
   $kr_2  = 0.0; 
   if($tmp_0==$tmp_1){
     $kr_1 = 1.0;
   }
   if($tmp_3==$tmp_4){
     $kr_2 =  1.0;
   }
   $tmp_G = $kr_1*$kr_2-$kr_1*$Green[$tmp_3][$tmp_4][1]-$kr_2*$Green[$tmp_0][$tmp_1][0];

   $D_1s_1[$sum_i][$orb_i][$site_i][$site_j] += $tmp_Cor_1 ;
   $D_1s_2[$sum_i][$orb_i][$site_i][$site_j] += ($tmp_G+$tmp_Cor_2);
 }
