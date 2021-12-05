{ pkgs ? import <nixpkgs> {}}:

with pkgs; mkShell {
  nativeBuildInputs = [
    apacheHttpd
    bazel
    nginx
    python3
    # python38Packages.wheel
  ];
}
