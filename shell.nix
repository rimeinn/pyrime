{
  pkgs ? import <nixpkgs> { },
}:

with pkgs;
mkShell {
  name = "pyrime";
  buildInputs = [
    librime
    libllvm

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
