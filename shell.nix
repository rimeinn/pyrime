{
  pkgs ? import <nixpkgs> { },
}:

with pkgs;
mkShell {
  name = "pyrime";
  buildInputs = [
    librime

    ninja
    pkg-config
    uv

    (python3.withPackages (
      p: with p; [
        pytest

        meson-python
        cython
        autopxd2
      ]
    ))
  ];
}
