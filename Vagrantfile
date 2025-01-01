# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"

  # Set up the VM settings
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"  # Allocate 2GB of memory
    vb.cpus = 1         
  end

  config.vm.network "private_network", ip: "192.168.33.10"


  # Forward ports for external access
  config.vm.network "forwarded_port", guest: 2181, host: 2181 # Zookeeper
  config.vm.network "forwarded_port", guest: 9092, host: 9092 # Kafka
  config.vm.network "forwarded_port", guest: 5432, host: 5432 #postgress

end
