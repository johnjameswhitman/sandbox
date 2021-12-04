{ pkgs ? import <nixpkgs> {}}:

with pkgs; mkShell {
  nativeBuildInputs = [
    bazel
    python3
    # python38Packages.wheel
  ];
}
