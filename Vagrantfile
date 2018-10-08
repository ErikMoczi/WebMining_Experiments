Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-16.04"
  config.vm.synced_folder ".", "/vagrant", id: "vagrant-root", :mount_options => ["dmode=777","fmode=777"]

  config.vm.provider "virtualbox" do |v|
    v.customize ["modifyvm", :id, "--memory", "1024"]
    v.customize ["modifyvm", :id, "--cpus", "4"]
    v.customize ["modifyvm", :id, "--vram", "12"]
    v.customize ["modifyvm", :id, "--ioapic", "on"]
    v.customize ["modifyvm", :id, "--audio", "none"]
    v.name = "python-vagrant-ubuntu"
  end

  config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.vm.provision "ansible_local" do |a|
    a.playbook = "setup.yml"
  end
end
