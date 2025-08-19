{
  pkgs ? import <nixpkgs> { },
}:

with pkgs;
mkShell {
  name = "pyrime";
  buildInputs = [
    librime

    pkg-config

    (python3.withPackages (
      p: with p; [
        uv
        pytest

        meson-python
        cython
        autopxd2
      ]
    ))
  ];
}
