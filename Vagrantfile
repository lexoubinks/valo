Vagrant.configure("2") do |config|
  config.vm.box = "debian/bookworm64"
  config.vm.network "private_network", ip: "192.168.1.5", virtualbox__intnet: "intnet"
  config.vm.provision "shell", path: "install.sh"
end
