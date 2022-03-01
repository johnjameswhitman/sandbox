/* Nix-based docker container for Nomad.
 *
 * Build and run this with:
 * podman load < (nix-build nomad.nix) && podman-compose up -d
 *
 * For more info and examples see:
 * - https://nixos.org/manual/nixpkgs/stable/#sec-pkgs-dockerTools
 * - https://github.com/NixOS/nixpkgs/blob/master/pkgs/build-support/docker/examples.nix
 */
{
  pkgs ? import <nixpkgs> { },
  pkgsLinux ? import <nixpkgs> { system = "x86_64-linux"; },
}:

let

  minimalNomadConfig = {
    server = {
      enabled = true;
      bootstrap_expect = 3;
    };
    client.enabled = true;  # really should disable
  };

in

pkgs.dockerTools.buildImage {

  name = "nomad";

  runAsRoot = ''
    #!${pkgsLinux.runtimeShell}
    ${pkgsLinux.dockerTools.shadowSetup}
    groupadd -r nomad
    useradd -r -g nomad nomad
    mkdir -p /etc/nomad/config.d
    mkdir -p /var/lib/nomad
    chown nomad:nomad /var/lib/nomad
  '';

  contents = with pkgs; [
    bash
    busybox
    # coreutils
    # Client mode requires at least the following:
    # https://github.com/NixOS/nixpkgs/blob/nixos-unstable/nixos/modules/services/networking/nomad.nix#L132-L135
    coreutils
    iproute2
    iptables
    (writeTextDir "etc/nomad/config.json" (builtins.toJSON minimalNomadConfig))
  ];

  config = {
    User = "nomad";
    Entrypoint = [
      "${pkgsLinux.nomad}/bin/nomad"
      "agent"
      "-data-dir=/var/lib/nomad"
      "-config=/etc/nomad/config.json"
      "-config=/etc/nomad/config.d"  # use to mount volume with extra configs.
    ];
    Cmd = [
    ];
  };

}
