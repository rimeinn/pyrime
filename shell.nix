{
  pkgs ? import <nixpkgs> { },
}:

with pkgs;
mkShell {
  name = "pyrime";
  env = {
    LD_LIBRARY_PATH = lib.makeLibraryPath [
      libclang
    ];
  };
  buildInputs = [
    librime
    libclang

    ninja
    pkg-config
    uv

    (python3.withPackages (
      p: with p; [
        pytest

        meson-python
        cython
      ]
    ))
  ];
}
