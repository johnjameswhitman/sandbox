{ pkgs ? import <nixpkgs> {}}:

with pkgs; mkShell {
  nativeBuildInputs = [
    awscli2
    bundix
    ruby_3_1.devEnv
    terraform
    # python38Packages.wheel
  ];
}
