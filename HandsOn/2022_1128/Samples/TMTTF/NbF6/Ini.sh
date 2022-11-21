#ln -s ../../data/TMTSF_roomT/AsF6/RESPACK/dir-model
python3 MakeInputForQLMS.py input.toml
python3 PHTrans.py input.toml
