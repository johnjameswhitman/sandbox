{ pkgs ? import <nixpkgs> {}}:

with pkgs; mkShell {
  nativeBuildInputs = [
    bundix
    ruby_3_1.devEnv
    terraform
    # python38Packages.wheel
  ];
}
