for dir in 1D_Heisenberg 1D_Hubbard 2D_Heisenberg 2D_Hubbard 1D_Kondo
do
echo "$dir " 
  cd ./$dir/
    echo "$pwd"
    #sh X.sh
  cd ..
done
