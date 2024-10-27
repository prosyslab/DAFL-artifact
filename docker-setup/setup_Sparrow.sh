cd /
git clone https://github.com/prosyslab/sparrow.git

cd /sparrow
git checkout dafl
export OPAMYES=1

apt-get update
apt-get install -y opam libclang-cpp12-dev libgmp-dev libclang-12-dev llvm-12-dev libmpfr-dev

sed -i '/^opam init/ s/$/ --disable-sandboxing/' build.sh
sed -i 's/opam install apron clangml/opam install conf-libclang.12 apron clangml/' build.sh
sed -i 's|opam pin add cil https://github.com/prosyslab/cil.git -n|opam pin add cil https://github.com/prosyslab/cil.git#8e87fe45 -n|' build.sh
./build.sh
opam install ppx_compare yojson ocamlgraph memtrace lymp clangml conf-libclang.12 batteries apron conf-mpfr cil linenoise claml

eval $(opam env)
make clean
make
