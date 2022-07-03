{ pkgs ? import <nixpkgs> {}}:

with pkgs; mkShell {
  nativeBuildInputs = [
    apacheHttpd
    python3
    # python38Packages.wheel
  ];
}
