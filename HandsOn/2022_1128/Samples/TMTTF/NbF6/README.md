### License

- Documents: CC BY 4.0
- Source codes: GNU General Public License v3.0 or later

### Usage

Copy or link dir-model of the target compound under this directory.

For example,
 `ln -s ../../data/TMTSF_roomT/AsF6/RESPACK/dir-model`


Then, to generate input files (`*.def` files) for mVMC, execute following commands:
  `python3 MakeInputForQLMS.py input.toml`
  `python3 PHTrans.py input.toml`

By changing parameters `Lx` and `Ly` in `input.toml`, 
one can generate the input files for different system sizes.
